# Data directory

```
public/data/
  raw_csv/   participantGrouped<ID>data.csv                    versioned
  json/      output_participantGrouped<ID>data_full_data.json  versioned
  build/     generated - not versioned, do not edit by hand
```

The source datasets are committed so everyone works from the same version. The
repo is private and limited to the team plus Stiti; **do not fork it, make it
public, or copy these files elsewhere** - they are participant conversations and
physiological recordings.

## After cloning

```bash
npm run data      # or: python3 scripts/build_data.py
```

That reads the two source folders and writes `build/index.json` plus one
`<context_id>.json` per context, which is what the app fetches at runtime.
Nothing beyond the Python standard library is needed.

## When Stiti sends new files

Replace the contents of `raw_csv/` and `json/`, re-run `npm run data`, and
commit the source files so the rest of the team picks them up.

A context only builds if it has **both** a CSV and a matching JSON. The script
prints what it skipped - currently 23, 23_1, 24 and 25 have a CSV but no JSON,
which Stiti confirmed we skip for now.

## Context names

`context_names.json` (optional, not yet supplied) maps context_id to a scenario
name for the selection screen:

```json
{ "11_1": "Family issue", "8": "Academic stress" }
```

Stiti is sharing the names in a Google doc. Until that file exists the cards
fall back to the participant id.
