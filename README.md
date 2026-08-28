# psychobase

A multi-modal emotional support chatbot that reads the user's words **and** their
physiological signals. A wearable streams EDA, pulse rate, skin temperature and
movement; a stress detector watches that stream; when it fires, the user is
offered a conversation with a chatbot that can see both what they typed and what
their body is doing.

This repository holds everything: the data, the response-generation and scoring
work, the visualisation site, and the model training that comes next.

```
psychobase/
├── docs/          the brief, the architecture deck, source documents
├── evaluation/    generating AI responses and scoring them on six parameters
├── model/         phase 2 - replacing Llama 7B with a smaller model
└── website/       the visualisation site (deployed)
```

---

## docs/

The task brief, the architecture deck (`ppt/`), and the source chat-data
document. Start with the deck for how the pieces fit together.

## evaluation/

Takes a participant's conversation JSON, shortens the physiological summary for
each turn, generates a new AI response under the master prompt, and scores the
new response against the original on six parameters - empathy, specificity,
strategy faithfulness, physiological grounding, fluency and safety.

```bash
cd evaluation
python3 scripts/extract.py <participant.json> -o out   # JSON -> working CSVs
python3 scripts/render.py P11                          # -> CSVs, markdown, HTML, docx
```

`scripts/render.py` enforces the rules agreed with Stiti, and fails the build
rather than shipping a report that breaks them:

- the physiological summary is 3-4 lines and always opens with
  `Physiological Signals:`
- wording and channel order vary from turn to turn, never one template
- responses never quote a value, a unit or a channel name - the summary is
  hidden from the user, so grounding is qualitative
- physiological grounding scores at least 3 on every new response

`scripts/step5_replace.py` writes verified summaries, strategies and responses
back into `training_string_case2` in the source JSON, which is what feeds model
training.

## website/

Select a conversation, read it turn by turn, and see the physiological signals
recorded alongside it. Clicking a turn highlights the time window that turn's
summary describes, on all five graphs at once.

```bash
cd website
python3 scripts/build_data.py   # or npm run data - CSV + JSON -> what the site fetches
npm install && npm run dev
```

Details, including two things about the source data that are easy to get wrong,
are in [website/README.md](website/README.md).

Deployed from this repository. The Vercel project builds from the repo root, so
the root `vercel.json` points the install and build commands into `website/`.

## model/

Phase 2, agreed 28 Aug: Llama 7B is too large for ~1,000 training pairs, so we
move to a smaller model and experiment with how the data is arranged and how we
fine-tune. Who is doing what, and the rules that keep the results comparable,
are in [model/TASKS.md](model/TASKS.md).

---

## The data

Participant conversations and physiological recordings, supplied by Stiti. They
live in `website/public/data/` (`json/` and `raw_csv/`) and are versioned so
everyone works from the same copy.

**This is human participant data** - real conversations about relationships,
family, health and work. The repository is private and limited to the team. Do
not fork it, make it public, or copy the datasets elsewhere.
