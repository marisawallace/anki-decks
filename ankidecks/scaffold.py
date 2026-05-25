"""Pure helpers for scaffolding decks and cards (text in, text out).

File I/O lives in the top-level scripts (new_deck.py, new_card.py,
add_cards.py); everything here is a pure transform and is unit-tested.
"""

from __future__ import annotations

import re

from .models import fields_for

# Anki cloze markers use {{cN::...}}; nothing here should touch them.


def slugify(text: str) -> str:
    """Lowercase, collapse non-alphanumerics to single hyphens, trim."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "card"


def render_deck_yaml(
    name: str, deck_id: int, note_type: str, tags: tuple[str, ...]
) -> str:
    """Produce the text of a ``deck.yaml`` file."""
    tag_list = ", ".join(tags)
    return (
        f'deck: "{name}"\n'
        f"deck_id: {deck_id}\n"
        f"note_type: {note_type}\n"
        f"tags: [{tag_list}]\n"
    )


def render_card_md(
    note_type: str,
    values: dict[str, str],
    card_id: str,
    tags: tuple[str, ...] = (),
) -> str:
    """Produce the text of one card ``.md`` file.

    ``values`` maps field name -> markdown (case-insensitive). Optional fields
    left blank are omitted. The stable ``card_id`` (a UUID) is written to
    frontmatter so the filename stays a human-readable label that can be renamed
    without changing the card's identity. Per-card ``tags`` also go in
    frontmatter.
    """
    lower = {k.lower(): v for k, v in values.items()}
    # Quote the id so YAML never retypes an all-digit or scientific-looking value.
    fm = [f'id: "{card_id}"']
    if tags:
        fm.append("tags: [" + ", ".join(tags) + "]")
    parts: list[str] = ["---\n" + "\n".join(fm) + "\n---"]
    for field in fields_for(note_type):
        text = (lower.get(field.lower()) or "").strip()
        if text:
            parts.append(f"# {field}\n{text}")
    return "\n\n".join(parts) + "\n"


def tsv_header(text: str, delimiter: str = "\t") -> list[str]:
    """Return the lowercased column names from a TSV's header row (``[]`` if empty)."""
    rows = [ln for ln in text.splitlines() if ln.strip()]
    return [h.strip().lower() for h in rows[0].split(delimiter)] if rows else []


def parse_tsv(text: str, delimiter: str = "\t") -> list[dict[str, str]]:
    """Parse a header-rowed TSV into a list of row dicts (lowercased keys).

    Literal ``\\n`` in a cell becomes a real newline so multi-line fields fit on
    one physical line. Blank lines are skipped. A row with *more* cells than the
    header (almost always an unescaped tab inside a cell) raises ``ValueError``
    rather than silently shifting columns; a row with fewer cells is allowed
    (trailing optional columns like ``tags`` may be omitted).
    """
    rows = [ln for ln in text.splitlines() if ln.strip()]
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0].split(delimiter)]
    out: list[dict[str, str]] = []
    for idx, line in enumerate(rows[1:], start=1):
        cells = line.split(delimiter)
        if len(cells) > len(header):
            raise ValueError(
                f"TSV data row {idx}: {len(cells)} columns but header has "
                f"{len(header)} — a literal tab inside a cell? Use \\n for line "
                "breaks and keep tabs out of cell content."
            )
        record = {
            header[i]: cells[i].replace("\\n", "\n").strip()
            for i in range(min(len(header), len(cells)))
        }
        out.append(record)
    return out


def split_tags(cell: str) -> tuple[str, ...]:
    """Split a tags cell on commas or whitespace."""
    return tuple(t for t in re.split(r"[,\s]+", cell.strip()) if t)
