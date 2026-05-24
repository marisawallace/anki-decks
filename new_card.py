#!/usr/bin/env python3
"""Add a single card to a deck (quick one-off; for bulk use add_cards.py).

    python new_card.py spanish-vocab "la casa" "the house" --tags noun
    python new_card.py france-facts "The capital is {{c1::Paris}}." "on the Seine"

The two positional fields map to the deck's note type: Front/Back for
basic decks, Text/Extra for cloze decks. The id defaults to a slug of the first
field; override with --id.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ankidecks.decks_io import read_note_type, resolve_deck, write_card
from ankidecks.models import fields_for
from ankidecks.scaffold import slugify

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("deck", help="deck folder name (or deck name)")
    ap.add_argument("field1", help="Front (basic) or Text (cloze)")
    ap.add_argument("field2", nargs="?", default="", help="Back or Extra (optional)")
    ap.add_argument("--id", help="card id (default: slug of field1)")
    ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--decks-dir", type=Path, default=DECKS_DIR)
    ap.add_argument("--force", action="store_true", help="overwrite if it exists")
    args = ap.parse_args()

    folder = resolve_deck(args.decks_dir, args.deck)
    note_type = read_note_type(folder)
    fields = fields_for(note_type)

    values = {fields[0]: args.field1, fields[1]: args.field2}
    card_id = args.id or slugify(args.field1)
    path = write_card(folder, note_type, card_id, values, tuple(args.tags), args.force)
    if path is None:
        raise SystemExit(f"card {card_id!r} already exists — use --force or --id")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
