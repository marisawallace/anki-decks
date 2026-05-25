# anki-decks

Author Anki decks as plain Markdown (one file per card), build them into
importable `.apkg` files with [genanki](https://github.com/kerrickstaley/genanki),
and drop a copy into the syncthing folder for the phone.

## Layout

```
decks/<deck>/deck.yaml     # deck-level metadata
decks/<deck>/<label>.md    # one card per file; filename is a human label, id is in frontmatter
decks/<deck>/_sources/     # consumed TSVs, archived for provenance
ankidecks/                 # pure core: parse.py, models.py, build.py
generate.py                # imperative shell: build + sync
output-decks/              # local .apkg builds (stable names, overwritten, gitignored)
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

### Card file `<label>.md`

The filename is a human-readable label; the card's identity is the frontmatter
`id`. The body's `#` (H1) headings are the note's fields (case-insensitive).
Don't start a content line with `# ` (single hash) — it would be read as a field
heading; `#` inside fenced code blocks is fine.

**basic / basic-reverse** — fields `Front`, `Back` (`basic-reverse` also makes the
reverse card):

```markdown
---
id: a1f3c9d24e8b4f7a9c2e6b1d8f0a3c57   # stable UUID; the tooling mints this
tags: [irregular]                      # optional, merged with deck tags
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

- **`deck_id`** is a fixed literal in `deck.yaml`, unique per deck. Don't change
  it, and don't copy a deck folder (that duplicates the id — `generate.py` will
  refuse to build until it's fixed).
- **Each note's GUID is its `card_id`** — the frontmatter `id` (a UUID), or the
  filename stem if absent. It's set directly on the note and is independent of
  card content *and* deck, so editing text, renaming the file, or moving the file
  to another deck all keep review history. (genanki's content-hash GUID is bypassed.)
- Model IDs are fixed constants in `ankidecks/models.py`.

**Editing vs. deleting.** Edit a card by changing its `.md` in place. Note that
deleting a `.md` does *not* remove the card from a device already synced — `.apkg`
import only adds/updates, never deletes; retire such cards inside Anki.

## Authoring cards

```bash
python new_deck.py "Spanish::Vocab" --note-type basic-reverse --tags spanish
python add_cards.py spanish-vocab cards.tsv     # bulk add from a header-rowed TSV
python new_card.py spanish-vocab "la casa" "the house"   # single card
```

`add_cards.py` is the efficient bulk path: a TSV whose header names the columns
(`front`/`back` or `text`/`extra`, plus optional `tags`). It is **add-only and
meant to be run once per TSV** — each row becomes a new card with a minted UUID,
and the TSV is archived into `decks/<deck>/_sources/`. Edit cards by changing
their `.md`; add more later with a fresh TSV. See `CLAUDE.md` for details.

## Build

```bash
python generate.py                 # build every deck
python generate.py --deck example  # just one deck (folder name)
python generate.py --no-sync       # skip the syncthing copy
python generate.py --sync-dir PATH # override the destination
```

Each build writes `output-decks/<deck>.apkg` (stable name, overwritten) and copies
it to `~/Documents/syncthing/anki-decks/<deck>.apkg` for the phone. Before building,
`generate.py` checks that all `deck_id`s and card ids are unique and aborts if not.

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
