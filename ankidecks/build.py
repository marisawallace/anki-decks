"""Pure construction: parsed records -> genanki objects.

Markdown -> HTML rendering lives here (a pure transform). No file I/O.
"""

from __future__ import annotations

import markdown as md
import genanki

from .models import fields_for, model_for
from .parse import Card, ParsedDeck

# Fields that may be omitted / left blank.
_OPTIONAL_FIELDS = {"extra"}
_MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]


def render_markdown(text: str) -> str:
    """Render a field's Markdown to HTML. Empty in, empty out.

    Anki cloze markers ``{{cN::...}}`` pass through untouched (Markdown treats
    the braces as literal text).
    """
    if not text.strip():
        return ""
    return md.markdown(text, extensions=_MD_EXTENSIONS)


def card_fields_html(card: Card, note_type: str) -> list[str]:
    """Map a card's sections onto the note type's ordered fields, as HTML.

    Validates that required fields are present and that no unknown sections
    leaked in (catches heading typos).
    """
    expected = fields_for(note_type)
    expected_lower = {f.lower(): f for f in expected}

    unknown = set(card.fields) - set(expected_lower)
    if unknown:
        raise ValueError(
            f"card {card.card_id!r} has unknown field section(s) "
            f"{sorted(unknown)}; expected {list(expected)}"
        )

    html: list[str] = []
    for field in expected:
        key = field.lower()
        raw = card.fields.get(key, "")
        if not raw.strip() and key not in _OPTIONAL_FIELDS:
            raise ValueError(
                f"card {card.card_id!r} is missing required field '{field}'"
            )
        html.append(render_markdown(raw))
    return html


def _sanitize_tags(tags: tuple[str, ...]) -> list[str]:
    # Anki tags are space-delimited, so spaces within a tag break them apart.
    return [t.replace(" ", "_") for t in tags if t]


def build_note(card: Card, note_type: str) -> genanki.Note:
    """Build a genanki Note with a stable, content-independent GUID.

    The GUID is the card's ``card_id`` (a globally-unique UUID for tooling-
    generated cards). It is *not* derived from content, so editing a card keeps
    its review history, and it carries no deck_id, so a card can move between
    deck folders without losing history.
    """
    return genanki.Note(
        model=model_for(note_type),
        fields=card_fields_html(card, note_type),
        guid=card.card_id,
        tags=_sanitize_tags(card.tags),
    )


def build_package(parsed: ParsedDeck) -> genanki.Package:
    """Build a genanki Package (one deck) from a parsed deck."""
    meta = parsed.meta
    deck = genanki.Deck(meta.deck_id, meta.name)
    for card in parsed.cards:
        deck.add_note(build_note(card, meta.note_type))
    return genanki.Package(deck)
