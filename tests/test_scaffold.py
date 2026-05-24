"""Tests for the pure scaffolding helpers."""

from ankidecks.parse import parse_card, parse_deck_meta
from ankidecks.scaffold import (
    parse_tsv,
    render_card_md,
    render_deck_yaml,
    slugify,
    split_tags,
)


def test_slugify():
    assert slugify("Spanish::Vocab") == "spanish-vocab"
    assert slugify("  Hello, World! ") == "hello-world"
    assert slugify("???") == "card"


def test_render_deck_yaml_roundtrips_through_parser():
    text = render_deck_yaml("Spanish::Vocab", 123, "basic-reverse", ("a", "b"))
    meta = parse_deck_meta(text)
    assert meta.name == "Spanish::Vocab"
    assert meta.deck_id == 123
    assert meta.note_type == "basic-reverse"
    assert meta.tags == ("a", "b")


def test_render_card_md_roundtrips_through_parser():
    text = render_card_md("basic", {"Front": "la casa", "Back": "the house"}, ("noun",))
    card = parse_card(text, "la-casa", deck_tags=("deck",))
    assert card.fields == {"front": "la casa", "back": "the house"}
    assert card.tags == ("deck", "noun")


def test_render_card_md_omits_empty_optional_field():
    text = render_card_md("cloze", {"Text": "{{c1::x}}", "Extra": ""})
    assert "# Extra" not in text
    assert "{{c1::x}}" in text


def test_render_card_md_no_tags_has_no_frontmatter():
    text = render_card_md("basic", {"Front": "a", "Back": "b"})
    assert not text.startswith("---")


def test_parse_tsv_with_newline_escape():
    rows = parse_tsv("front\tback\ttags\nla casa\tthe house\\nmore\tnoun\n")
    assert rows == [{"front": "la casa", "back": "the house\nmore", "tags": "noun"}]


def test_parse_tsv_empty():
    assert parse_tsv("") == []


def test_split_tags():
    assert split_tags("a, b  c") == ("a", "b", "c")
    assert split_tags("") == ()
