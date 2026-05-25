"""Tests for the impure shell: unique filenames and the id-uniqueness preflight."""

from pathlib import Path

import pytest

from ankidecks.decks_io import write_card
from ankidecks.parse import Card, DeckMeta, ParsedDeck
from generate import check_ids_unique


def _deck(name: str, deck_id: int, *card_ids: str) -> tuple[Path, ParsedDeck]:
    meta = DeckMeta(name=name, deck_id=deck_id, note_type="basic", tags=())
    cards = tuple(Card(card_id=cid, fields={}, tags=()) for cid in card_ids)
    return Path(name), ParsedDeck(meta=meta, cards=cards)


def test_write_card_disambiguates_filename(tmp_path):
    vals = {"Front": "la casa", "Back": "the house"}
    p1 = write_card(tmp_path, "basic", "id-1", "casa", vals, ())
    p2 = write_card(tmp_path, "basic", "id-2", "casa", vals, ())
    assert p1.name == "casa.md"
    assert p2.name == "casa-2.md"  # clash -> disambiguated, never overwritten


def test_check_ids_unique_passes_when_distinct():
    check_ids_unique([_deck("a", 1, "x"), _deck("b", 2, "y")])


def test_check_ids_unique_rejects_duplicate_deck_id():
    with pytest.raises(SystemExit, match="duplicate deck_id 1"):
        check_ids_unique([_deck("a", 1, "x"), _deck("b", 1, "y")])


def test_check_ids_unique_rejects_duplicate_card_id():
    with pytest.raises(SystemExit, match="duplicate card id"):
        check_ids_unique([_deck("a", 1, "dup"), _deck("b", 2, "dup")])
