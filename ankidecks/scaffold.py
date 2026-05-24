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
    note_type: str, values: dict[str, str], tags: tuple[str, ...] = ()
) -> str:
    """Produce the text of one card ``.md`` file.

    ``values`` maps field name -> markdown (case-insensitive). Optional fields
    left blank are omitted. Per-card ``tags`` go in frontmatter; the card id is
    carried by the filename, never duplicated here.
    """
    lower = {k.lower(): v for k, v in values.items()}
    parts: list[str] = []
    if tags:
        parts.append("---\ntags: [" + ", ".join(tags) + "]\n---")
    for field in fields_for(note_type):
        text = (lower.get(field.lower()) or "").strip()
        if text:
            parts.append(f"# {field}\n{text}")
    return "\n\n".join(parts) + "\n"


def parse_tsv(text: str, delimiter: str = "\t") -> list[dict[str, str]]:
    """Parse a header-rowed TSV into a list of row dicts (lowercased keys).

    Literal ``\\n`` in a cell becomes a real newline so multi-line fields fit on
    one physical line. Blank lines are skipped.
    """
    rows = [ln for ln in text.splitlines() if ln.strip()]
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0].split(delimiter)]
    out: list[dict[str, str]] = []
    for line in rows[1:]:
        cells = line.split(delimiter)
        record = {
            header[i]: cells[i].replace("\\n", "\n").strip()
            for i in range(min(len(header), len(cells)))
        }
        out.append(record)
    return out


def split_tags(cell: str) -> tuple[str, ...]:
    """Split a tags cell on commas or whitespace."""
    return tuple(t for t in re.split(r"[,\s]+", cell.strip()) if t)
