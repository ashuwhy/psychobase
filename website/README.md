# Physiological Conversation Visualisation

Select a conversation context, read it turn by turn, and see the physiological
signals recorded alongside it. Clicking a turn highlights the time interval that
turn's physiological summary describes, on all five graphs at once.

## Setup

```bash
# 1. Put the supplied data in place (not committed - see .gitignore)
#    public/data/raw_csv/   <- dataGrouped.zip
#    public/data/json/      <- Modified_JSON.zip

# 2. Build the frontend-ready JSON (standard library only, no pip install)
python3 scripts/build_data.py

# 3. Run
npm install
npm run dev
```

`npm run data` re-runs step 2 after Stiti sends updated files.

## How the data actually works

Worth reading before writing any chart code - the CSV is not what it first looks
like.

**The CSV is one row per conversation turn, not a stream of samples.** Its
`timestamp` column is a *range* joined by an en-dash:

```
2026-05-04T19:33:00–2026-05-04T19:34:00
```

and each signal column holds a short array of samples taken inside that range:

```
EDA = "[4.13, 3.99]"    PR = "[101.0, 92.0]"    ACT_CLASS = "['generic', 'still']"
```

`build_data.py` flattens those arrays onto a real time axis, spacing a row's
samples evenly inside its own window, to produce one continuous series per
signal for the whole conversation.

**The highlight interval looks backwards, and it grows.** A turn's interval is
not its own row window. Turn 4 sits at 19:38 and its summary says "over the past
5 minutes", so the band runs 19:33-19:38 and covers several earlier turns. That
look-back grows through the conversation - 1, 2, 3 minutes - then holds at 6.
This is why the intervals must be dynamic: they are the input to the highlight.

The pipeline reads the minutes out of each summary, converts them to a real
start/end pair, and hands the UI a ready-made interval. **Do not re-derive
intervals in the frontend**; read `turn.interval`.

## Output

`scripts/build_data.py` writes to `public/data/build/`:

- `index.json` - one row per participant/context, for the selection screen.
  A context with a modified rewrite carries both as `variants` on the same
  row rather than appearing twice.
- `<variant_id>.json` - `signals`, `domain`, `series`, `turns` for one
  variant (`8`, `8-modified`, ...)

Shapes are declared in `src/types.ts`. That file and the script change together.

## Data notes

- 54 contexts build: 44 originals and 10 modified variants. Participants 23,
  23_1, 24 and 25 previously had a CSV but no JSON; the 21 Aug drop supplied
  theirs, so nothing is skipped any more.
- **Modified variants.** Stiti sends better-written versions of some
  conversations, named `..._modified_phyS[_context]`. Same participant, same
  timestamps and same scenario, but the dialogue is rephrased - "I've been
  struggling to perform well in athletics" becomes "My regional trials are in
  three days and I can't stop shaking". They are additions, not replacements, so
  each variant gets its own build output (`8-modified.json`), but the
  selection screen shows one card per context - `index.json` groups the
  original and modified variant together (`variants: [...]`) rather than
  listing them as two separate contexts. Pairing is by *exact* suffix (CSV
  `_modified_phyS.csv` only matches JSON `_modified_phyS_full_data.json`, not
  a same-participant file with a different suffix), so a mismatched pair is
  reported as skipped instead of silently guessed at. A new variant needs no
  code change.
- The five charted signals are EDA, PR, SkinTemp, ACCEL and ACT_COUNT. The brief
  named ACT_CLASS as the fifth, but it holds category strings rather than
  numbers, and Stiti confirmed ACT_COUNT instead. ACT_CLASS still ships inside
  `series` for anyone who wants to annotate with it.
- Context display names come from `public/data/context_names.json`, which covers
  all 40 contexts. The source is CHAT_DATA_WITH_PHYSIOLOGICAL_SIGNAL(EMBRACE_PLUS).docx,
  where the label appears variously as "Context:", "Scenario:" or
  "Context (2 words):"; a few names in the file are shortened from the long
  descriptions that document carries. Cards fall back to the participant id for
  any context missing from the file.
- All 749 turns yield an interval from their summary text.
- Some turns state a look-back that doesn't follow the 1-2-3-...-6 scheme. Per
  Stiti we highlight exactly what the summary text says; `interval_mismatches`
  lists them per context as a diagnostic only.
- `nan` in the source becomes `null`, so charts can break the line instead of
  plotting zero.

## Who is doing what

See [TASKS.md](TASKS.md).
