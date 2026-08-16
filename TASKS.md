# Work split - four people

Target: a basic working version for the **Monday update meeting**.

Everything meets at one contract, `src/types.ts`. Agree any change to that file
in the group before making it, and B/C/D can then build in parallel without
waiting on each other.

The data pipeline (task A) is already done and committed, so B, C and D have
real JSON to work against from the first commit rather than mocking it.

---

## Task A - Data pipeline and contract (Ashutosh)

`scripts/build_data.py`, `src/types.ts`

- [x] Flatten the per-turn CSV arrays onto a real time axis
- [x] Read each turn's highlight interval out of its physiological summary
- [x] Emit `public/data/build/index.json` + one `<context_id>.json` per context
- [x] Report intervals that disagree with the 1-2-3-...-6 scheme
- [x] Fifth graph switched to ACT_COUNT per Stiti, 15 Aug
- [x] Support `public/data/context_names.json` for scenario names
- [x] Context names in place for all 40 contexts (context_names.json)
- [ ] Re-run `npm run data` whenever Stiti sends updated JSON

Run it with `npm run data` (or `python3 scripts/build_data.py`). No dependencies
beyond the standard library.

## Task B - Data loading and context selection (Siddaarth)

`src/lib/data.ts`, `src/pages/ContextList.tsx`

Screen 1, plus the loading layer everyone else uses.

- [x] Fetch and render `index.json` as cards - **nothing hard-coded**, the brief
      is explicit that contexts come from the file
- [x] Each card: context name (`name`, falls back to participant id until
      Stiti's mapping arrives), context id, turn count, date/duration
- [x] Click routes to `/context/:contextId`
- [x] Loading and error states (a missing context file must not blank the page)

Done when: adding a new participant JSON and re-running `npm run data` makes a
new card appear with no code change.

## Task C - The five graphs (Krishna)

`src/components/SignalChart.tsx`, `src/lib/time.ts`

The heart of the app. One chart per entry in `ContextData.signals` - EDA, PR,
SkinTemp, ACCEL, ACT_COUNT. Stiti confirmed ACT_COUNT as the fifth graph, not
ACT_CLASS.

- [ ] Line chart per signal over the **whole** conversation
- [ ] Every chart uses the same X domain from `ContextData.domain`, so the five
      stay vertically aligned
- [ ] X axis timestamps, Y axis value + unit from `SignalMeta`
- [ ] Hover tooltip with exact timestamp and value
- [ ] **Translucent band** for the selected turn's interval, full chart height,
      identical range on all five
- [ ] `v: null` breaks the line - it must not plot as zero

Done when: clicking any turn moves the band on all five charts to the same range
in one render.

## Task D - Conversation panel, shell and state (Nithish)

`src/pages/ConversationView.tsx`, `src/components/TurnList.tsx`, `src/styles.css`

- [ ] Two-column layout, roughly 38% conversation / 62% graphs
- [ ] Each turn shows turn number, speaker id, user message, AI strategy, AI
      response and the physiological summary
- [ ] Selected turn has a clear active state and stays identifiable while scrolling
- [ ] Conversation panel scrolls independently of the graphs
- [ ] Holds the `selectedTurn` state and passes `turns[selected].interval` to the
      charts - this is the only shared state in the app
- [ ] Back link to the context list
- [ ] Readable on a laptop; degrades to stacked columns on narrow screens

Done when: selecting a turn highlights it in the list and drives the graphs.

---

## Integration order

1. B lands `loadContext` -> C and D both have real data on screen
2. D lands the shell with `selectedTurn` -> C drops charts into it
3. Wire the interval through and check all five bands move together

## Watch out for

- **Turn 1's interval.** Its summary says "the first minute" and looks back from
  the very start of the recording, so the raw band falls before any data. The
  pipeline slides it forward; don't re-derive intervals in the UI, just read
  `turn.interval`.
- **Intervals off the scheme.** `interval_mismatches` lists turns whose stated
  look-back is not `min(turn, 6)` minutes. Settled: highlight what the summary
  text says. The list stays as a diagnostic only.
- **Few points per signal.** Some contexts have only ~20 samples across an hour.
  Show the markers, not just the line, or the charts look empty.
- **Categorical NaN.** Some rows carry `nan` inside the arrays; the pipeline
  converts them to `null`.
