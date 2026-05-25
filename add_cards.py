#!/usr/bin/env python3
"""Bulk-add cards to a deck from a header-rowed TSV (the efficient path).

    python add_cards.py spanish-vocab cards.tsv
    python add_cards.py spanish-vocab -        # read TSV from stdin

TSV columns are named by the header row (case-insensitive). Use the note type's
field names plus optional ``id`` and ``tags``:

    basic / basic-reverse:   front <TAB> back <TAB> tags
    cloze:                   text  <TAB> extra <TAB> tags

This is ADD-ONLY and meant to be run ONCE per TSV: each row becomes a new card
with a freshly-minted UUID identity (written to its frontmatter), and the source
TSV is copied into ``decks/<slug>/_sources/`` for provenance. To *edit* existing
cards, edit their ``.md`` files in place — re-running a TSV would duplicate them,
not update them. A later TSV may add *more* cards; it will never touch existing
ones. Provide an explicit ``id`` column only to override the minted UUID.

Use literal ``\\n`` inside a cell for a line break. ``tags`` split on commas/space.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path

from dataclasses import dataclass

from ankidecks.build import card_fields_html
from ankidecks.decks_io import read_note_type, resolve_deck, write_card
from ankidecks.models import fields_for
from ankidecks.parse import Card
from ankidecks.scaffold import parse_tsv, slugify, split_tags, tsv_header

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"


@dataclass(frozen=True)
class PlannedCard:
    """A validated, ready-to-write card (no I/O has happened yet)."""

    card_id: str
    filename_base: str
    values: dict[str, str]
    tags: tuple[str, ...]


def plan_cards(
    rows: list[dict[str, str]], header: list[str], note_type: str
) -> list[PlannedCard]:
    """Validate every TSV row and mint ids — *before* anything is written.

    Raises ``SystemExit`` on the first problem (unknown column, missing/empty
    required field, unknown field section) so a bad TSV writes **zero** cards
    instead of leaving the deck half-applied. ids are minted here, but that is the
    only impurity; everything else is a pure check reusing ``card_fields_html``.
    """
    fields = fields_for(note_type)
    allowed = {f.lower() for f in fields} | {"id", "tags"}
    unknown_cols = [c for c in header if c and c not in allowed]
    if unknown_cols:
        raise SystemExit(
            f"TSV has unknown column(s) {unknown_cols}; "
            f"allowed for a {note_type!r} deck: {sorted(allowed)}"
        )

    planned: list[PlannedCard] = []
    for idx, row in enumerate(rows, start=1):
        values = {f: row.get(f.lower(), "") for f in fields}
        first = values[fields[0]]
        if not first.strip():
            raise SystemExit(f"TSV data row {idx}: missing required '{fields[0]}'")
        card_id = row.get("id") or uuid.uuid4().hex
        tags = split_tags(row.get("tags", ""))
        # Dry-run the field mapping/render to catch missing-required/unknown early.
        probe = Card(
            card_id=card_id,
            fields={f.lower(): v for f, v in values.items()},
            tags=tags,
        )
        try:
            card_fields_html(probe, note_type)
        except ValueError as exc:
            raise SystemExit(f"TSV data row {idx}: {exc}")
        planned.append(PlannedCard(card_id, slugify(first), values, tags))
    return planned


def archive_tsv(folder: Path, src: Path) -> Path:
    """Copy a consumed TSV into ``<deck>/_sources/`` so its provenance is kept."""
    sources = folder / "_sources"
    sources.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = sources / f"{stamp}-{src.name}"
    shutil.copyfile(src, dest)
    return dest


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("deck", help="deck folder name (or deck name)")
    ap.add_argument("tsv", help="path to TSV file, or - for stdin")
    ap.add_argument("--decks-dir", type=Path, default=DECKS_DIR)
    args = ap.parse_args()

    folder = resolve_deck(args.decks_dir, args.deck)
    note_type = read_note_type(folder)

    text = sys.stdin.read() if args.tsv == "-" else Path(args.tsv).read_text("utf-8")
    # Validate the whole TSV up front; only then touch the filesystem (atomic-ish).
    try:
        planned = plan_cards(parse_tsv(text), tsv_header(text), note_type)
    except ValueError as exc:  # malformed TSV from the pure parser
        raise SystemExit(f"{args.tsv}: {exc}")
    for card in planned:
        write_card(
            folder, note_type, card.card_id, card.filename_base, card.values, card.tags
        )

    msg = f"{folder.name}: wrote {len(planned)} card(s)"
    if args.tsv != "-":
        msg += f"; archived TSV -> {archive_tsv(folder, Path(args.tsv))}"
    print(msg)


if __name__ == "__main__":
    main()
