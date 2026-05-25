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


def _unique_path(folder: Path, base: str) -> Path:
    """A non-existing ``folder/<base>.md``, appending ``-2``, ``-3`` … if taken.

    The filename is only a human-readable label (identity lives in the card's
    frontmatter ``id``), so a clash means a genuinely different card: we never
    overwrite, we disambiguate.
    """
    path = folder / f"{base}.md"
    n = 2
    while path.exists():
        path = folder / f"{base}-{n}.md"
        n += 1
    return path


def write_card(
    folder: Path,
    note_type: str,
    card_id: str,
    filename_base: str,
    values: dict[str, str],
    tags: tuple[str, ...],
) -> Path:
    """Write one card file to a fresh, unique path. Returns its path.

    ``card_id`` is the stable identity (written to frontmatter); ``filename_base``
    is the human-readable filename stem (disambiguated if it already exists).
    """
    path = _unique_path(folder, filename_base)
    path.write_text(render_card_md(note_type, values, card_id, tags), encoding="utf-8")
    return path
