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

from ankidecks.decks_io import read_note_type, resolve_deck, write_card
from ankidecks.models import fields_for
from ankidecks.scaffold import parse_tsv, slugify, split_tags

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"


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
    fields = fields_for(note_type)

    text = sys.stdin.read() if args.tsv == "-" else Path(args.tsv).read_text("utf-8")
    rows = parse_tsv(text)

    written = 0
    for row in rows:
        values = {f: row.get(f.lower(), "") for f in fields}
        first = values[fields[0]]
        if not first.strip():
            raise SystemExit(f"row missing required '{fields[0]}' field: {row}")
        card_id = row.get("id") or uuid.uuid4().hex
        tags = split_tags(row.get("tags", ""))
        write_card(folder, note_type, card_id, slugify(first), values, tags)
        written += 1

    msg = f"{folder.name}: wrote {written} card(s)"
    if args.tsv != "-":
        msg += f"; archived TSV -> {archive_tsv(folder, Path(args.tsv))}"
    print(msg)


if __name__ == "__main__":
    main()
