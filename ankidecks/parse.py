"""Pure parsing: Markdown source text -> structured records.

No genanki, no markdown rendering, no file I/O here. This is the functional
core; ``generate.py`` does the reading and ``build.py`` does the rendering and
genanki construction.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import yaml

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n?---\s*\n?(.*)$", re.DOTALL)
_H1_RE = re.compile(r"^#\s+(.+?)\s*$")

VALID_NOTE_TYPES = ("basic", "basic-reverse", "cloze")


@dataclass(frozen=True)
class DeckMeta:
    name: str
    deck_id: int
    note_type: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class Card:
    card_id: str
    fields: dict[str, str]  # lowercased section heading -> raw markdown
    tags: tuple[str, ...]


@dataclass(frozen=True)
class ParsedDeck:
    meta: DeckMeta
    cards: tuple[Card, ...]


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split leading ``---`` YAML frontmatter from the body.

    Returns ``(meta_dict, body)``. Frontmatter is optional and may be empty.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.group(1), match.group(2)
    meta = yaml.safe_load(raw) if raw.strip() else {}
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise ValueError(f"frontmatter must be a mapping, got {type(meta).__name__}")
    return meta, body


def split_sections(body: str) -> dict[str, str]:
    """Split a card body into ``# Heading`` sections.

    Heading text is lowercased to form the key; section content has surrounding
    blank lines stripped. Text before the first heading is ignored.
    """
    sections: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []

    def flush() -> None:
        if current is not None:
            sections[current] = "\n".join(lines).strip("\n")

    for line in body.splitlines():
        heading = _H1_RE.match(line)
        if heading:
            flush()
            current = heading.group(1).strip().lower()
            lines = []
        elif current is not None:
            lines.append(line)
    flush()
    return sections


def parse_deck_meta(yaml_text: str) -> DeckMeta:
    """Parse a ``deck.yaml`` file's text into a :class:`DeckMeta`."""
    data = yaml.safe_load(yaml_text) or {}
    if not isinstance(data, dict):
        raise ValueError("deck.yaml must be a mapping")

    missing = [k for k in ("deck", "deck_id", "note_type") if k not in data]
    if missing:
        raise ValueError(f"deck.yaml missing required key(s): {', '.join(missing)}")

    note_type = str(data["note_type"])
    if note_type not in VALID_NOTE_TYPES:
        raise ValueError(
            f"note_type {note_type!r} not one of {VALID_NOTE_TYPES}"
        )
    if not isinstance(data["deck_id"], int):
        raise ValueError("deck_id must be an integer literal")

    tags = data.get("tags") or []
    return DeckMeta(
        name=str(data["deck"]),
        deck_id=int(data["deck_id"]),
        note_type=note_type,
        tags=tuple(str(t) for t in tags),
    )


def parse_card(text: str, stem: str, deck_tags: tuple[str, ...] = ()) -> Card:
    """Parse one card file's text into a :class:`Card`.

    ``stem`` is the filename without extension; it is the default card id.
    ``deck_tags`` are merged ahead of any per-card ``tags``.
    """
    meta, body = split_frontmatter(text)
    card_id = str(meta.get("id") or stem)
    card_tags = tuple(str(t) for t in (meta.get("tags") or []))
    fields = split_sections(body)
    if not fields:
        raise ValueError(f"card {stem!r} has no '# Heading' field sections")
    return Card(card_id=card_id, fields=fields, tags=deck_tags + card_tags)
