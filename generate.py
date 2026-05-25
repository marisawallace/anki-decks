#!/usr/bin/env python3
"""Imperative shell: scan decks/, build .apkg files, archive + copy to syncthing.

Usage:
    python generate.py                 # build every deck
    python generate.py --deck NAME     # build one deck (folder name)
    python generate.py --no-sync       # skip the syncthing copy
    python generate.py --sync-dir PATH # override the syncthing destination
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from ankidecks.build import build_package
from ankidecks.parse import ParsedDeck, parse_card, parse_deck_meta

REPO_ROOT = Path(__file__).resolve().parent
DECKS_DIR = REPO_ROOT / "decks"
OUTPUT_DIR = REPO_ROOT / "output-decks"
SYNC_DIR = Path.home() / "Documents" / "syncthing" / "anki-decks"


def read_deck(folder: Path) -> ParsedDeck:
    """Read a deck folder (deck.yaml + *.md cards) into a ParsedDeck."""
    meta = parse_deck_meta((folder / "deck.yaml").read_text(encoding="utf-8"))
    cards = tuple(
        parse_card(path.read_text(encoding="utf-8"), path.stem, meta.tags)
        for path in sorted(folder.glob("*.md"))
    )
    if not cards:
        raise ValueError(f"deck {folder.name!r} has no card .md files")
    return ParsedDeck(meta=meta, cards=cards)


def discover_decks(decks_dir: Path) -> list[Path]:
    """All deck folders (those containing a deck.yaml), sorted by name."""
    return sorted(p for p in decks_dir.iterdir() if (p / "deck.yaml").is_file())


def check_ids_unique(decks: list[tuple[Path, ParsedDeck]]) -> None:
    """Fail loudly on duplicate deck_ids or card GUIDs across all decks.

    A duplicate ``deck_id`` (e.g. from copying a deck folder as a template) makes
    Anki *merge* the decks on import; a duplicate GUID makes one card silently
    overwrite another. Both are catastrophic and silent on-device, so we catch
    them at build time.
    """
    seen_deck: dict[int, str] = {}
    seen_guid: dict[str, str] = {}
    for folder, parsed in decks:
        did = parsed.meta.deck_id
        if did in seen_deck:
            raise SystemExit(
                f"duplicate deck_id {did} in {folder.name!r} and {seen_deck[did]!r} "
                "— each deck.yaml needs its own deck_id (did you copy a folder?)"
            )
        seen_deck[did] = folder.name
        for card in parsed.cards:
            if card.card_id in seen_guid:
                raise SystemExit(
                    f"duplicate card id {card.card_id!r} in {folder.name!r} and "
                    f"{seen_guid[card.card_id]!r} — ids must be globally unique"
                )
            seen_guid[card.card_id] = folder.name


def build_deck(
    folder: Path, parsed: ParsedDeck, output_dir: Path, sync_dir: Path | None
) -> None:
    """Build one deck: write a stable-named .apkg and (optionally) sync a copy."""
    output_dir.mkdir(parents=True, exist_ok=True)
    apkg = output_dir / f"{folder.name}.apkg"
    build_package(parsed).write_to_file(str(apkg))

    synced = None
    if sync_dir is not None:
        sync_dir.mkdir(parents=True, exist_ok=True)
        synced = sync_dir / f"{folder.name}.apkg"
        shutil.copyfile(apkg, synced)

    detail = f"-> {apkg}" + (f"  +  {synced}" if synced else "")
    print(f"  {parsed.meta.name}: {len(parsed.cards)} cards  {detail}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deck", help="build only this deck (folder name)")
    ap.add_argument("--no-sync", action="store_true", help="skip syncthing copy")
    ap.add_argument("--sync-dir", type=Path, default=SYNC_DIR)
    ap.add_argument("--decks-dir", type=Path, default=DECKS_DIR)
    ap.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = ap.parse_args()

    sync_dir = None if args.no_sync else args.sync_dir

    # Read & ID-check ALL decks (so dup deck_ids are caught even for a 1-deck build).
    everything = [(f, read_deck(f)) for f in discover_decks(args.decks_dir)]
    check_ids_unique(everything)

    targets = everything
    if args.deck is not None:
        targets = [(f, p) for f, p in everything if f.name == args.deck]
        if not targets:
            raise SystemExit(f"no deck folder named {args.deck!r} under {args.decks_dir}")

    print(f"Building {len(targets)} deck(s):")
    for folder, parsed in targets:
        build_deck(folder, parsed, args.output_dir, sync_dir)


if __name__ == "__main__":
    main()
