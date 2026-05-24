#!/usr/bin/env python3
"""Scaffold a new deck folder (decks/<slug>/deck.yaml) with a fresh deck_id.

    python new_deck.py "Spanish::Vocab" --note-type basic-reverse --tags spanish vocab
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from ankidecks.parse import VALID_NOTE_TYPES
from ankidecks.scaffold import render_deck_yaml, slugify

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"


def new_deck_id() -> int:
    """A fresh, stable 10-digit id (assigned once, never regenerated)."""
    return random.randrange(1_000_000_000, 9_999_999_999)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", help='deck name, e.g. "Spanish::Vocab" (:: = subdeck)')
    ap.add_argument(
        "--note-type", default="basic-reverse", choices=VALID_NOTE_TYPES
    )
    ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--decks-dir", type=Path, default=DECKS_DIR)
    args = ap.parse_args()

    folder = args.decks_dir / slugify(args.name)
    if folder.exists():
        raise SystemExit(f"deck folder already exists: {folder}")

    folder.mkdir(parents=True)
    yaml_text = render_deck_yaml(
        args.name, new_deck_id(), args.note_type, tuple(args.tags)
    )
    (folder / "deck.yaml").write_text(yaml_text, encoding="utf-8")
    print(f"created {folder}/deck.yaml ({args.note_type})")
    print(f"  add cards: python add_cards.py {folder.name} cards.tsv")


if __name__ == "__main__":
    main()
