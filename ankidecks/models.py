"""genanki note-type (Model) definitions.

Pure: importing this module constructs three fixed Models and exposes a mapping
from a deck's ``note_type`` string to the Model + its ordered field names.

Model IDs are GLOBAL in Anki (shared across every deck), so they are fixed
literals here and must never change once decks have been imported.
"""

from __future__ import annotations

import genanki

# --- fixed, never-change model IDs -------------------------------------------
BASIC_MODEL_ID = 1700000000001
BASIC_REVERSE_MODEL_ID = 1700000000002
CLOZE_MODEL_ID = 1700000000003

_CSS = """
.card {
  font-family: -apple-system, system-ui, Arial, sans-serif;
  font-size: 20px;
  text-align: center;
  color: #1a1a1a;
  background: #ffffff;
}
hr#answer { margin: 1em 0; }
.cloze { font-weight: bold; color: #0a64c2; }
pre { text-align: left; }
"""

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    "anki-decks Basic",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        }
    ],
    css=_CSS,
)

BASIC_REVERSE_MODEL = genanki.Model(
    BASIC_REVERSE_MODEL_ID,
    "anki-decks Basic (and reversed)",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Front}}',
        },
    ],
    css=_CSS,
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    "anki-decks Cloze",
    fields=[{"name": "Text"}, {"name": "Extra"}],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Text}}",
            "afmt": "{{cloze:Text}}<br>{{Extra}}",
        }
    ],
    model_type=genanki.Model.CLOZE,
    css=_CSS,
)

# note_type string -> (Model, ordered field names)
NOTE_TYPES: dict[str, tuple[genanki.Model, tuple[str, ...]]] = {
    "basic": (BASIC_MODEL, ("Front", "Back")),
    "basic-reverse": (BASIC_REVERSE_MODEL, ("Front", "Back")),
    "cloze": (CLOZE_MODEL, ("Text", "Extra")),
}


def model_for(note_type: str) -> genanki.Model:
    """Return the genanki Model for a ``note_type`` string."""
    return NOTE_TYPES[note_type][0]


def fields_for(note_type: str) -> tuple[str, ...]:
    """Return the ordered field names for a ``note_type`` string."""
    return NOTE_TYPES[note_type][1]
