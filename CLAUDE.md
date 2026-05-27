# anki-decks — project guide

Created so Marisa and Claude can collaboratively manage and create Anki decks.

The core idea is support for two "upstream" representations optimized for card creation -- TSV for Claude, and Markdown for Marisa and Claude.

The pipeline is TSV -> Markdown -> apkg -> syncthing to Marisa's phone -> Marisa does a manual import of the updated deck into AnkiDroid.

genanki is used internally for creating the apkgs from Markdown. Anki renders HTML + CSS so we convert Markdown to those at build time.

## TSV

Claude is the only one directly creating cards at the TSV stage. We chose TSV to optimize tokens and thinking quality. The workflow looks like:

1. Marisa sends prompt to Claude: "if you'd like, please create a deck for [topic]"
2. Claude generates a `.tsv` (where?)
3. Marisa spot-checks or edits, runs `new_deck.py` (if needed), then `add_cards.py deck-slug file.tsv` to create `.md` files in the deck based on the `.tsv`

Claude's generated TSVs do/should not contain IDs. `add_cards.py` autogenerates stable, filename/slug-independent UUIDs so we can update a card's markdown and have the update propagate correctly into Anki. `add_cards.py` should only be run once on a given TSV. We do not support re-generating or editing cards at the TSV stage. Edit the Markdown.


## Markdown

- Looks like `decks/<slug>/*.md` -- the canonical source/representation of the decks we create together.

- Marisa may run `new_card.py spanish-vocab "la casa" "the house"` to add new cards one-off. These cards aren't difficult to create by hand; this is just a generator for convenience.

- Run `generate.py` which builds `.apkg` files for every deck and overwrites them in the syncthing directory and `output-decks/`.


## Quickstart

Requires Python 3.10+. First-time setup:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'                    # 'dev' adds pytest
```

Then:

```bash
python new_deck.py "Spanish::Vocab" --note-type basic-reverse --tags spanish
python add_cards.py spanish-vocab cards.tsv   # bulk add from a TSV (see below)
python new_card.py spanish-vocab "la casa" "the house"   # single card
python generate.py                            # build every deck -> .apkg + sync
python -m pytest -q                           # pure-core tests, no Anki needed
```

## Code structure

Code layout (pure core vs imperative shell, per repo conventions):
- `ankidecks/parse.py` — pure: source text → records.
- `ankidecks/models.py` — pure: the 3 genanki note types (fixed global IDs).
- `ankidecks/build.py` — pure: records → genanki package (Markdown→HTML here).
- `ankidecks/scaffold.py` — pure: render deck.yaml / card.md, slugify, parse TSV.
- `ankidecks/decks_io.py` — impure: filesystem helpers for the scripts.
- `generate.py`, `new_deck.py`, `add_cards.py`, `new_card.py` — imperative shells.

### Building
```bash
python generate.py                 # build every deck
python generate.py --deck example  # just one deck (folder name)
python generate.py --no-sync       # skip the optional 2nd-destination copy
python generate.py --sync-dir PATH # override the 2nd-destination path
```
Each build writes `output-decks/<slug>.apkg` (stable name, overwritten, gitignored). If `SYNC_DIR` is set in `.env` (see `.env.example`) — typically a Syncthing folder that mirrors to your phone — the `.apkg` is also copied there. Before building, `generate.py` checks that all `deck_id`s and card ids are unique and aborts if not.

## Source format

**`decks/<slug>/deck.yaml`** — one per deck folder:
```yaml
deck: "Spanish::Vocab"     # :: builds an Anki subdeck hierarchy
deck_id: 5340401766        # fixed int, assigned once by new_deck.py — NEVER change
note_type: basic-reverse   # basic | basic-reverse | cloze
tags: [spanish, vocab]     # applied to every card in the deck
```

**`decks/<slug>/<label>.md`** — one per card. The filename is a human-readable label (slug of the first field); identity lives in the frontmatter `id`. The `#` (H1) headings are the note's fields (case-insensitive).

```markdown
---
id: "a1f3c9d24e8b4f7a9c2e6b1d8f0a3c57"  # stable UUID = the note's identity (required, quoted)
tags: [irregular]                       # optional, merged with deck tags
---
# Front
la casa

# Back
the house  — multi-line **markdown**, lists, `code`, tables all render
```

Because the H1 `#` at the start of a line delimits fields, **don't begin a line of card content with `# ` (single hash + space)** — use `##`+ for in-card headings. `#` lines inside fenced code blocks (```` ``` ````/`~~~`) are safe; they're treated as content, so code comments render fine.

Cloze cards use fields `Text` / `Extra` and native Anki syntax:

```markdown
# Text
The capital of France is {{c1::Paris}}.

# Extra
Optional hint shown with the answer.
```

### Note types
- `basic` — fields Front, Back. One direction.
- `basic-reverse` — Front, Back; also makes the reverse card. Best for vocab and term↔definition pairs.
- `cloze` — Text, Extra. Fill-in-the-blank; best for facts in context.

### IDs and updates (don't break this)

Re-importing a rebuilt `.apkg` *updates* a deck instead of duplicating it only because identifiers are stable:

- `deck_id` is a fixed literal in `deck.yaml`, unique per deck.

- A note's GUID is its **`card_id`** — the frontmatter `id`, a UUID minted by the tooling. It is **required** on every card (parsing fails loudly if missing — no filename-stem fallback) and is quoted in YAML so an all-digit value is never retyped to an int. It is set directly on the note and is **independent of both card content and deck**, so:
  - editing a card's text keeps its review history;
  - **renaming the `.md` file keeps its history** (identity is in the frontmatter);
  - **moving a card's `.md` to another deck folder keeps its history** (no `deck_id` is baked into the GUID).

- `new_card.py` / `add_cards.py` mint the `id` for you. To hand-author a card, copy an existing one and replace the `id` with a fresh UUID (e.g. `python -c "import uuid;print(uuid.uuid4().hex)"`). `generate.py` fails loudly on any duplicate `card_id` or `deck_id`.

## Terse authoring format (TSV) — how Claude should emit cards

When generating cards, **write a header-rowed TSV**, not per-card `.md` files — it is the most token-efficient robust format and keeps cards parallel and atomic. Write it with the Write tool (preserves tabs) to e.g. `tsvs/<slug>.tsv`. Marisa will then confirm the output and run `add_cards.py` if all looks good. Columns are named by the header (case-insensitive); use the note type's field names plus optional `id` and `tags`:

```
front	back	tags
la casa	the house	noun
el perro	the dog	noun animal
correr	to run\n(irregular)	verb
```
- `cloze` decks use `text` / `extra` columns instead of `front` / `back`.

- **Don't emit an `id` column** — `add_cards.py` mints a UUID per card (writing UUIDs in the TSV just burns tokens). Only set `id` to deliberately override. - `tags` (optional) are split on commas/whitespace and merged with deck tags.

- Use literal `\n` in a cell for a line break; reach for per-card `.md` only when a card genuinely needs rich multi-line markdown (lists, code blocks). Keep literal tabs out of cell content — a row with more columns than the header is rejected (it's almost always a stray tab).

- `add_cards.py` validates the **whole** TSV before writing anything (unknown columns, empty/missing required fields, ragged rows) and aborts writing **zero** cards on any problem — so a rejected TSV never leaves a deck half-applied. Fix the reported row and re-run.

**Run each TSV once.** `add_cards.py` is add-only: every row becomes a *new* card and the TSV is archived to `decks/<slug>/_sources/`. It does **not** update or de-duplicate, so re-running a TSV duplicates its cards.

- To **edit** existing cards: change their `.md` files directly (identity is the frontmatter `id`, so edits and even renames keep review history).

- To **add more** cards later: write a *new* TSV containing only the new cards and run `add_cards.py` again.


### Card-writing principles (make the decks excellent)

- **One fact per card** (minimum-information principle). Split compound facts.

- **Unambiguous cues** — the front should have exactly one good answer. Add disambiguating context to the front when needed (e.g. `bank (river)`).

- **No "list all…" / enumeration cards.** If order/sets matter, use several cloze deletions or break into atomic cards.

- **Cloze for facts in context**; **basic-reverse for vocab and term↔definition**. - Keep phrasing concise, concrete, and consistent across the deck.

- Prefer active recall ("Capital of France?" → "Paris") over yes/no prompts.


## Gotchas

- `deck_id` and the model IDs in `models.py` are permanent; changing them orphans existing reviews. `new_deck.py` assigns each deck's `deck_id` once. **Never copy a deck folder to start a new deck** — you'd duplicate its `deck_id` (Anki merges the decks on import). `generate.py` catches this, but `new_deck.py` is the right way to start one.

- **Deleting a card `.md` does not remove it from the phone.** `.apkg` import only adds/updates notes; it never deletes. To retire a card, delete it in Anki itself (desktop/AnkiDroid). Decks built here only grow on-device.

- genanki writes `collection.anki2` inside the `.apkg`; that's expected and imports fine on desktop, AnkiDroid, and AnkiMobile.

- Tabs matter in the TSV — write it with the Write tool, not via shell echo.

- Loading on phone: the synced `<slug>.apkg` can be tapped → "Open in" Anki for a one-off. For progress that survives rebuilds, import once on desktop → AnkiWeb sync → sync the phone; thereafter re-imports update cards in place.
```
