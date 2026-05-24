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
from datetime import datetime
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


def discover_decks(decks_dir: Path, only: str | None) -> list[Path]:
    folders = sorted(p for p in decks_dir.iterdir() if (p / "deck.yaml").is_file())
    if only is not None:
        folders = [p for p in folders if p.name == only]
        if not folders:
            raise SystemExit(f"no deck folder named {only!r} under {decks_dir}")
    return folders


def build_deck(folder: Path, output_dir: Path, sync_dir: Path | None) -> None:
    """Build one deck: write a timestamped archive and (optionally) sync a copy."""
    parsed = read_deck(folder)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{folder.name}-{stamp}.apkg"
    build_package(parsed).write_to_file(str(archive))

    synced = None
    if sync_dir is not None:
        sync_dir.mkdir(parents=True, exist_ok=True)
        synced = sync_dir / f"{folder.name}.apkg"
        shutil.copyfile(archive, synced)

    detail = f"-> {archive}" + (f"  +  {synced}" if synced else "")
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
    folders = discover_decks(args.decks_dir, args.deck)
    print(f"Building {len(folders)} deck(s):")
    for folder in folders:
        build_deck(folder, args.output_dir, sync_dir)


if __name__ == "__main__":
    main()
