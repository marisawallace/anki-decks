"""Impure filesystem helpers shared by the card-authoring scripts.

Kept separate from the pure ``scaffold``/``parse``/``build`` modules.
"""

from __future__ import annotations

from pathlib import Path

from .parse import parse_deck_meta
from .scaffold import render_card_md, slugify


def resolve_deck(decks_dir: Path, name: str) -> Path:
    """Find a deck folder by exact folder name or by slug of ``name``."""
    for candidate in (decks_dir / name, decks_dir / slugify(name)):
        if (candidate / "deck.yaml").is_file():
            return candidate
    raise SystemExit(f"no deck folder for {name!r} under {decks_dir}")


def read_note_type(folder: Path) -> str:
    return parse_deck_meta((folder / "deck.yaml").read_text(encoding="utf-8")).note_type


def write_card(
    folder: Path,
    note_type: str,
    card_id: str,
    values: dict[str, str],
    tags: tuple[str, ...],
    force: bool,
) -> Path | None:
    """Write one card file. Returns its path, or None if it existed and not forced."""
    path = folder / f"{card_id}.md"
    if path.exists() and not force:
        return None
    path.write_text(render_card_md(note_type, values, tags), encoding="utf-8")
    return path
