# Data directory

Nothing in here is committed except this file. The datasets come from Stiti and
the build output is generated, so both are gitignored.

```
public/data/
  raw_csv/   <- unzip dataGrouped.zip here      (participantGrouped<ID>data.csv)
  json/      <- unzip Modified_JSON.zip here    (output_participantGrouped<ID>data_full_data.json)
  build/     <- generated, do not edit by hand
```

## Setup

Drop the two folders in as above, then:

```bash
npm run data      # or: python3 scripts/build_data.py
```

That writes `build/index.json` plus one `<context_id>.json` per context, which
is what the app fetches at runtime. Re-run it whenever Stiti sends new files.

A context only builds if it has **both** a CSV and a matching JSON. The script
prints what it skipped - as of the last run, 23, 23_1, 24 and 25 have a CSV but
no JSON yet.
