"""Tests for the impure shell: unique filenames and the id-uniqueness preflight."""

import sys
from pathlib import Path

import pytest

from add_cards import main as add_cards_main, plan_cards
from ankidecks.decks_io import write_card
from ankidecks.parse import Card, DeckMeta, ParsedDeck
from ankidecks.scaffold import parse_tsv, tsv_header
from generate import check_ids_unique


def _plan(text: str, note_type: str = "basic"):
    return plan_cards(parse_tsv(text), tsv_header(text), note_type)


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


# --- plan_cards: all validation happens before any write -----------------------

def test_plan_cards_valid_mints_distinct_ids():
    planned = _plan("front\tback\nla casa\tthe house\nla casa\tthe home\n")
    assert [p.filename_base for p in planned] == ["la-casa", "la-casa"]
    assert planned[0].card_id != planned[1].card_id  # distinct minted ids


def test_plan_cards_rejects_unknown_column():
    with pytest.raises(SystemExit, match="unknown column.*notes"):
        _plan("front\tback\tnotes\na\tb\tc\n")


def test_plan_cards_rejects_empty_first_field():
    with pytest.raises(SystemExit, match="data row 2: missing required 'Front'"):
        _plan("front\tback\ngood\tb1\n\tb2\n")


def test_plan_cards_rejects_missing_required_field():
    with pytest.raises(SystemExit, match="data row 1: .*missing required field 'Back'"):
        _plan("front\tback\nonly front\t\n")


def test_plan_cards_honours_explicit_id():
    planned = _plan("front\tback\tid\na\tb\tfixed-1\n")
    assert planned[0].card_id == "fixed-1"


# --- add_cards.main is atomic: a bad row writes zero cards ----------------------

def _make_deck(folder: Path, note_type: str = "basic") -> None:
    folder.mkdir()
    (folder / "deck.yaml").write_text(
        f'deck: D\ndeck_id: 5\nnote_type: {note_type}\ntags: []\n', encoding="utf-8"
    )


def _run_add_cards(monkeypatch, decks_dir: Path, deck: str, tsv: Path) -> None:
    monkeypatch.setattr(
        sys, "argv", ["add_cards.py", deck, str(tsv), "--decks-dir", str(decks_dir)]
    )
    add_cards_main()


def test_add_cards_atomic_on_bad_row(tmp_path, monkeypatch):
    _make_deck(tmp_path / "d")
    tsv = tmp_path / "c.tsv"
    tsv.write_text("front\tback\ngood1\tb1\n\tb2\ngood3\tb3\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        _run_add_cards(monkeypatch, tmp_path, "d", tsv)
    assert list((tmp_path / "d").glob("*.md")) == []  # nothing written
    assert not (tmp_path / "d" / "_sources").exists()  # not archived


def test_add_cards_writes_all_on_valid(tmp_path, monkeypatch):
    _make_deck(tmp_path / "d")
    tsv = tmp_path / "c.tsv"
    tsv.write_text("front\tback\na\t1\nb\t2\n", encoding="utf-8")
    _run_add_cards(monkeypatch, tmp_path, "d", tsv)
    assert len(list((tmp_path / "d").glob("*.md"))) == 2
    assert (tmp_path / "d" / "_sources").is_dir()
