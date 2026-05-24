# anki-decks — project guide

Build Anki decks from plain-Markdown source. Author cards (often with Claude),
turn them into `.apkg` files with genanki, and drop copies in a syncthing folder
that reaches the phone. The repo-wide conventions in `../CLAUDE.md` apply
(functional core / imperative shell, `uv` for Python, immutability).

The headline use case: **"make me a deck about X"** → Claude scaffolds the deck,
generates the cards, builds it, and it shows up on the phone. The
"Authoring a deck from whole cloth" section below is the workflow for exactly that.

## Quickstart

```bash
py=$HOME/.venvs/global/bin/python          # repo-wide alias is `py`
$py new_deck.py "Spanish::Vocab" --note-type basic-reverse --tags spanish
$py add_cards.py spanish-vocab cards.tsv   # bulk add from a TSV (see below)
$py new_card.py spanish-vocab "la casa" "the house"   # single card
$py generate.py                            # build every deck -> .apkg + sync
$py -m pytest -q                           # pure-core tests, no Anki needed
```

## Pipeline

```
Claude  ──TSV──▶  add_cards.py  ──▶  decks/<slug>/*.md  ──▶  generate.py  ──▶  .apkg
(terse, cheap)    (explode)         (canonical source)      (build+copy)       │
                                                                    ┌──────────┴──────────┐
                                                          output-decks/<slug>-<ts>.apkg   ~/Documents/syncthing/anki-decks/<slug>.apkg
                                                          (timestamped archive)           (stable name → phone)
```

Code layout (pure core vs imperative shell, per repo conventions):
- `ankidecks/parse.py` — pure: source text → records.
- `ankidecks/models.py` — pure: the 3 genanki note types (fixed global IDs).
- `ankidecks/build.py` — pure: records → genanki package (Markdown→HTML here).
- `ankidecks/scaffold.py` — pure: render deck.yaml / card.md, slugify, parse TSV.
- `ankidecks/decks_io.py` — impure: filesystem helpers for the scripts.
- `generate.py`, `new_deck.py`, `add_cards.py`, `new_card.py` — imperative shells.

## Source format

**`decks/<slug>/deck.yaml`** — one per deck folder:
```yaml
deck: "Spanish::Vocab"     # :: builds an Anki subdeck hierarchy
deck_id: 5340401766        # fixed int, assigned once by new_deck.py — NEVER change
note_type: basic-reverse   # basic | basic-reverse | cloze
tags: [spanish, vocab]     # applied to every card in the deck
```

**`decks/<slug>/<id>.md`** — one per card. The `#` (H1) headings are the note's
fields (case-insensitive). Frontmatter is optional, metadata only.
```markdown
---
tags: [irregular]          # optional, merged with deck tags
---
# Front
la casa

# Back
the house  — multi-line **markdown**, lists, `code`, tables all render
```
Cloze cards use fields `Text` / `Extra` and native Anki syntax:
```markdown
# Text
The capital of France is {{c1::Paris}}.

# Extra
Optional hint shown with the answer.
```

### Note types
- `basic` — fields Front, Back. One direction.
- `basic-reverse` — Front, Back; also makes the reverse card. Best for vocab and
  term↔definition pairs.
- `cloze` — Text, Extra. Fill-in-the-blank; best for facts in context.

### IDs and updates (don't break this)
Re-importing a rebuilt `.apkg` *updates* a deck instead of duplicating it only
because identifiers are stable:
- `deck_id` is a fixed literal in `deck.yaml`.
- A note's GUID is `"<deck_id>:<card_id>"`, where `card_id` is the **filename
  stem** (or a frontmatter `id:`). It is set directly on the note and is
  **independent of card content** — so editing a card keeps its review history.
- Renaming a card file = a new card. To rename freely, first pin an `id:` in its
  frontmatter.

## Terse authoring format (TSV) — how Claude should emit cards

When generating cards, **write a header-rowed TSV**, not per-card `.md` files —
it is the most token-efficient robust format and keeps cards parallel and atomic.
Write it with the Write tool (preserves tabs) to e.g. `/tmp/<slug>.tsv`, then run
`add_cards.py`. Columns are named by the header (case-insensitive); use the note
type's field names plus optional `id` and `tags`:

```
front	back	tags
la casa	the house	noun
el perro	the dog	noun animal
correr	to run\n(irregular)	verb
```
- `cloze` decks use `text` / `extra` columns instead of `front` / `back`.
- `id` is optional → defaults to a slug of the first field.
- `tags` (optional) are split on commas/whitespace and merged with deck tags.
- Use literal `\n` in a cell for a line break; reach for per-card `.md` only when
  a card genuinely needs rich multi-line markdown (lists, code blocks).

## Authoring a deck from whole cloth

When asked to create a deck:
1. **Decide and state assumptions** (don't over-ask — take a good stab):
   deck name (use `Parent::Child` for hierarchy), `note_type`
   (`basic-reverse` for vocab/term pairs, `basic` for Q&A/facts, `cloze` for
   facts-in-context), tags, and rough card count/scope.
2. `python new_deck.py "Name" --note-type <t> --tags <...>` → note the slug.
3. Generate the cards as a TSV and Write it to `/tmp/<slug>.tsv`.
4. `python add_cards.py <slug> /tmp/<slug>.tsv`.
5. `python generate.py --deck <slug>` and report: deck name, card count, and that
   the `.apkg` is in `output-decks/` and synced to the phone folder.

### Card-writing principles (make the decks excellent)
- **One fact per card** (minimum-information principle). Split compound facts.
- **Unambiguous cues** — the front should have exactly one good answer. Add
  disambiguating context to the front when needed (e.g. `bank (river)`).
- **No "list all…" / enumeration cards.** If order/sets matter, use several cloze
  deletions or break into atomic cards.
- **Cloze for facts in context**; **basic-reverse for vocab and term↔definition**.
- Keep phrasing concise, concrete, and consistent across the deck.
- Prefer active recall ("Capital of France?" → "Paris") over yes/no prompts.

## Gotchas
- `deck_id` and the model IDs in `models.py` are permanent; changing them orphans
  existing reviews. `new_deck.py` assigns each deck's `deck_id` once.
- genanki writes `collection.anki2` inside the `.apkg`; that's expected and
  imports fine on desktop, AnkiDroid, and AnkiMobile.
- Tabs matter in the TSV — write it with the Write tool, not via shell echo.
- Loading on phone: the synced `<slug>.apkg` can be tapped → "Open in" Anki for a
  one-off. For progress that survives rebuilds, import once on desktop → AnkiWeb
  sync → sync the phone; thereafter re-imports update cards in place.
```
