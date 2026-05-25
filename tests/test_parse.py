"""Tests for the pure core: parsing and building (no Anki runtime needed)."""

import pytest

from ankidecks.build import build_note, card_fields_html, render_markdown
from ankidecks.parse import (
    parse_card,
    parse_deck_meta,
    split_frontmatter,
    split_sections,
)


def test_split_frontmatter_present():
    meta, body = split_frontmatter("---\ntags: [a, b]\n---\n# Front\nhi\n")
    assert meta == {"tags": ["a", "b"]}
    assert body.strip() == "# Front\nhi"


def test_split_frontmatter_empty_block():
    meta, body = split_frontmatter("---\n---\n# Text\nx\n")
    assert meta == {}
    assert "# Text" in body


def test_split_frontmatter_absent():
    meta, body = split_frontmatter("# Front\nhi")
    assert meta == {}
    assert body == "# Front\nhi"


def test_split_sections():
    sections = split_sections("# Front\nla casa\n\n# Back\nthe house\n")
    assert sections == {"front": "la casa", "back": "the house"}


def test_split_sections_ignores_hash_in_fenced_code():
    body = "# Front\nname a comment\n\n# Back\n```python\n# not a heading\nx = 1\n```\n"
    sections = split_sections(body)
    assert set(sections) == {"front", "back"}
    assert "# not a heading" in sections["back"]


def test_parse_card_requires_id():
    with pytest.raises(ValueError, match="no 'id' in frontmatter"):
        parse_card("# Front\na\n\n# Back\nb\n", "casa")


def test_parse_card_id_and_tag_merge():
    text = "---\nid: custom\ntags: [extra]\n---\n# Front\na\n\n# Back\nb\n"
    card = parse_card(text, "ignored", deck_tags=("deck",))
    assert card.card_id == "custom"
    assert card.tags == ("deck", "extra")
    assert card.fields == {"front": "a", "back": "b"}


def test_parse_card_no_sections_errors():
    with pytest.raises(ValueError, match="no '# Heading'"):
        parse_card("---\nid: x\n---\njust prose, no headings", "x")


def test_parse_deck_meta_ok():
    meta = parse_deck_meta(
        "deck: D\ndeck_id: 123\nnote_type: basic\ntags: [t]\n"
    )
    assert (meta.name, meta.deck_id, meta.note_type, meta.tags) == (
        "D", 123, "basic", ("t",)
    )


def test_parse_deck_meta_bad_note_type():
    with pytest.raises(ValueError, match="note_type"):
        parse_deck_meta("deck: D\ndeck_id: 1\nnote_type: nope\n")


def test_parse_deck_meta_non_int_id():
    with pytest.raises(ValueError, match="deck_id must be an integer"):
        parse_deck_meta("deck: D\ndeck_id: abc\nnote_type: basic\n")


def test_render_markdown_passes_cloze_through():
    html = render_markdown("The capital is {{c1::Paris}}.")
    assert "{{c1::Paris}}" in html


def test_card_fields_html_unknown_section_errors():
    card = parse_card("---\nid: x\n---\n# Front\na\n\n# Middle\nb\n", "x")
    with pytest.raises(ValueError, match="unknown field section"):
        card_fields_html(card, "basic")


def test_card_fields_html_missing_required_errors():
    card = parse_card("---\nid: x\n---\n# Front\na\n", "x")
    with pytest.raises(ValueError, match="missing required field 'Back'"):
        card_fields_html(card, "basic")


def test_card_fields_html_optional_extra_ok():
    card = parse_card("---\nid: x\n---\n# Text\n{{c1::a}}\n", "x")
    html = card_fields_html(card, "cloze")
    assert "{{c1::a}}" in html[0]
    assert html[1] == ""


def test_build_note_guid_is_stable_and_content_independent():
    card1 = parse_card("---\nid: casa\n---\n# Front\na\n\n# Back\nb\n", "casa")
    card2 = parse_card(
        "---\nid: casa\n---\n# Front\nDIFFERENT\n\n# Back\nALSO DIFFERENT\n", "casa"
    )
    n1 = build_note(card1, "basic")
    n2 = build_note(card2, "basic")
    assert n1.guid == "casa"  # the card_id, with no deck_id prefix
    assert n1.guid == n2.guid  # edits don't change the GUID


def test_build_note_guid_uses_frontmatter_id():
    card = parse_card("---\nid: abc123\n---\n# Front\na\n\n# Back\nb\n", "casa")
    assert build_note(card, "basic").guid == "abc123"
