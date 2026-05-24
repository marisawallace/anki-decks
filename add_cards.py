#!/usr/bin/env python3
"""Bulk-add cards to a deck from a header-rowed TSV (the efficient path).

    python add_cards.py spanish-vocab cards.tsv
    python add_cards.py spanish-vocab -        # read TSV from stdin

TSV columns are named by the header row (case-insensitive). Use the note type's
field names plus optional ``id`` and ``tags``:

    basic / basic-reverse:   front <TAB> back <TAB> tags
    cloze:                   text  <TAB> extra <TAB> tags

If ``id`` is omitted, it defaults to a slug of the first field. Use literal
``\\n`` inside a cell for a line break. ``tags`` are split on commas/whitespace.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ankidecks.decks_io import read_note_type, resolve_deck, write_card
from ankidecks.models import fields_for
from ankidecks.scaffold import parse_tsv, slugify, split_tags

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("deck", help="deck folder name (or deck name)")
    ap.add_argument("tsv", help="path to TSV file, or - for stdin")
    ap.add_argument("--decks-dir", type=Path, default=DECKS_DIR)
    ap.add_argument("--force", action="store_true", help="overwrite existing cards")
    args = ap.parse_args()

    folder = resolve_deck(args.decks_dir, args.deck)
    note_type = read_note_type(folder)
    fields = fields_for(note_type)

    text = sys.stdin.read() if args.tsv == "-" else Path(args.tsv).read_text("utf-8")
    rows = parse_tsv(text)

    written, skipped = 0, []
    for row in rows:
        values = {f: row.get(f.lower(), "") for f in fields}
        first = values[fields[0]]
        if not first.strip():
            raise SystemExit(f"row missing required '{fields[0]}' field: {row}")
        card_id = row.get("id") or slugify(first)
        tags = split_tags(row.get("tags", ""))
        path = write_card(folder, note_type, card_id, values, tags, args.force)
        if path is None:
            skipped.append(card_id)
        else:
            written += 1

    print(f"{folder.name}: wrote {written} card(s)" + (f", skipped {len(skipped)} existing ({', '.join(skipped)}) — use --force" if skipped else ""))


if __name__ == "__main__":
    main()
