# anki-decks

Author Anki decks as plain Markdown (one file per card), build them into
importable `.apkg` files with [genanki](https://github.com/kerrickstaley/genanki),
and drop a copy into the syncthing folder for the phone.

## Layout

```
decks/<deck>/deck.yaml     # deck-level metadata
decks/<deck>/<id>.md       # one card per file; filename stem = card id
ankidecks/                 # pure core: parse.py, models.py, build.py
generate.py                # imperative shell: build + archive + sync
output-decks/              # timestamped .apkg archives
```

`parse.py`, `models.py`, `build.py` are pure (text/data in, data out);
`generate.py` does all the file I/O.

## Source format

### `deck.yaml`

```yaml
deck: "Spanish::Vocab"     # :: makes an Anki subdeck hierarchy
deck_id: 1700000100003     # fixed int literal — assign once, NEVER change it
note_type: basic-reverse   # basic | basic-reverse | cloze
tags: [spanish, vocab]     # applied to every card in the deck
```

### Card file `<id>.md`

The body's `#` (H1) headings are the note's fields. Heading match is
case-insensitive. Frontmatter is optional and holds metadata only.

**basic / basic-reverse** — fields `Front`, `Back` (`basic-reverse` also makes the
reverse card):

```markdown
---
tags: [irregular]          # optional, merged with deck tags
# id: override-id          # optional; default id = filename stem
---
# Front
la casa

# Back
the house (multi-line **markdown**, lists, `code`, tables all work)
```

**cloze** — fields `Text`, `Extra` (optional). Use native Anki cloze syntax:

```markdown
# Text
The capital of France is {{c1::Paris}}.

# Extra
Optional hint shown on the answer side.
```

## IDs and updating decks (important)

Re-importing an `.apkg` *updates* an existing deck only if its identifiers are
stable, so this repo keeps them stable on purpose:

- **`deck_id`** is a fixed literal in `deck.yaml`. Don't change it.
- **Each note's GUID is `"<deck_id>:<card_id>"`**, where `card_id` is the
  frontmatter `id` or, by default, the **filename stem**. It is set directly on
  the note — *not* derived from the card's content — so editing a card's text
  keeps its review history. (genanki's default content-hash GUID is bypassed.)
- Renaming a card file changes its id (= a new card). To rename freely, pin an
  explicit `id:` in the card's frontmatter first.
- Model IDs are fixed constants in `ankidecks/models.py`.

## Authoring cards

```bash
python new_deck.py "Spanish::Vocab" --note-type basic-reverse --tags spanish
python add_cards.py spanish-vocab cards.tsv     # bulk add from a header-rowed TSV
python new_card.py spanish-vocab "la casa" "the house"   # single card
```

`add_cards.py` is the efficient bulk path: a TSV whose header names the columns
(`front`/`back` or `text`/`extra`, plus optional `id`/`tags`). See `CLAUDE.md` for
the format and the "deck from whole cloth" workflow.

## Build

```bash
python generate.py                 # build every deck
python generate.py --deck example  # just one deck (folder name)
python generate.py --no-sync       # skip the syncthing copy
python generate.py --sync-dir PATH # override the destination
```

Each build writes `output-decks/<deck>-<timestamp>.apkg` (archive) and overwrites
`~/Documents/syncthing/anki-decks/<deck>.apkg` (stable name for the phone).

## Loading on the phone

The stable-named `.apkg` lands in syncthing → it appears on the phone. Then either:

- **One-off:** tap the `.apkg` and "Open in" AnkiDroid/AnkiMobile to import.
- **With progress sync (recommended for ongoing decks):** import the `.apkg` once
  into desktop Anki, Sync to your AnkiWeb account, and Sync on the phone. After
  that, rebuilding + re-importing the same `.apkg` updates cards in place and
  scheduling/streaks are preserved.

## Dev

```bash
pytest          # pure-core tests (no Anki runtime needed)
```
