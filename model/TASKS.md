# Phase 2 - smaller model, better fit to the data

Agreed in the 28 Aug meeting. Llama 7B is too large for ~1,000 training pairs
(~2,000 strings), so we replace it with a smaller model and experiment with how
the data is arranged and how we fine-tune it.

**Monday 31 Aug:** each lane has 1-2 configurations trained and scored.
**Tuesday:** review meeting.

---

## Read this first - it decides whether Monday's numbers mean anything

There are three axes here: the model, the data format, and the fine-tuning
method. Four people changing different axes at once produces four results that
cannot be compared. If two of us report "better", we will not know whether the
gain came from the model, the arrangement, or the method - and with ~2,000
samples the run-to-run noise is large enough to swamp a real effect, so this is
a practical problem rather than a purist one.

Three rules make the table meaningful:

1. **One axis at a time, everything else pinned** to an agreed baseline. Every
   run is a diff against that baseline, not against another experiment.
2. **One frozen test split, made once, used by all four of us.** Never trained
   on. If we each split separately, the numbers are not comparable.
3. **One scripted judge.** The six parameters were scored by hand for the
   Google Doc. That does not scale to dozens of runs and two people will not
   score identically. Same prompt, same scale, same judge, every run.

**Split by conversation, not by turn.** Turns within a conversation share a
participant and a physiological session; splitting mid-conversation leaks the
test set into training and every model looks better than it is.

---

## Day 1 - two pairs working in parallel

Nothing can be measured until the foundation exists, and nothing can be trained
until there is a training script. Both pairs work at once so neither waits.

### Ashutosh - splits, baseline, results table - DONE, waiting on server

- [x] Conversation-level split, frozen in `splits.json`, 69/15/15 by turns
      (`scripts/make_splits.py`)
- [x] Shared loader `scripts/dataset.py` - import this rather than reading the
      JSON directory, or we end up with four loaders that disagree
- [x] Baseline configuration in `configs/baseline.json`
- [x] Results table in `RESULTS.md`
- [ ] Chase CSE server access - it sets the ceiling on model size for everyone,
      so it blocks model selection more than anything else

Three things the split work turned up, all worth knowing before you train:

- **`person_id` is useless for grouping.** It reads 2753 on 43 of the 55 files,
  so it is a device or batch identifier, not a person. Grouping is by
  participant number instead.
- **Participant 1 had two modified generations.** Stiti chose `_modified_phyS`
  on 28 Aug, so the older `_modified` file is excluded in `make_splits.py`.
  That is why the totals are 54 conversations and 993 turns rather than 55 and
  1023.
- **11, 11_1, 11_2 and 11_3 are one participant across four sessions**, so they
  travel together. That is the conservative choice; it costs split granularity
  (26 groups, not 55) and the alternative is available behind
  `--group-by file` if we decide the finer split is worth the leakage risk.

### Nithish - evaluation harness

- [ ] Takes a model's generated responses on the test split, returns the six
      parameters, reproducible between people and across days
- [ ] Reuse the rules already encoded in `evaluation/scripts/render.py` -
      particularly that physiological grounding must be qualitative, since a
      response that quotes values should not score well on it
- [ ] Sanity-check it against the scores we produced by hand: if the harness
      disagrees wildly with the Google Doc rows for the same responses, the
      harness is wrong and everything downstream inherits that

### Siddaarth - training pipeline and data formatting

- [ ] Get one model training end to end on the baseline configuration first -
      this unblocks Krishna as much as yourself
- [ ] Then the three arrangements from the meeting, on the baseline model and
      method: interleaved (case 1, case 2, case 1...), batched (all case 1s then
      all case 2s), randomised
- [ ] Watch for this: the batched arrangement risks the model learning "the
      physiological summary appears in the second half" rather than learning to
      use it. If batched scores oddly high or oddly low, suspect that before
      believing the number

### Krishna - fine-tuning method

- [ ] Alternatives to LoRA, suited to this data size:
      - full fine-tuning (viable at 1B, and the one most likely to win here)
      - QLoRA, if memory is the binding constraint
      - DoRA, rsLoRA, LoRA+ - variants that behave better on small data
      - IA3 or prefix tuning - far fewer parameters again
- [ ] Report trainable parameter count alongside each score. "Better" that costs
      20x the trainable parameters is a different result from "better" that
      does not

---

## Once the foundation lands - model selection

Split between Ashutosh and Nithish, 1-2 models each, all on the baseline
format and method so the model is the only thing that changed. Verify what is
current before committing - this list moves quickly:

- Qwen2.5 1.5B / 3B Instruct
- Llama 3.2 1B / 3B Instruct
- SmolLM3-3B (reported to beat Llama-3.2-3B and Qwen2.5-3B at that size)
- Phi-3.5-mini (3.8B)
- Gemma 2 2B

Record VRAM, training time and inference latency per model. A model we cannot
run on the hardware we have is not a candidate however well it scores.

**The reasoning behind the phase:** at ~2,000 samples, LoRA on a 7B model
updates very few parameters relative to how far this task sits from
pretraining, which is why it learns so little. A smaller model fully fine-tuned
gets far more of its weights moved by the same data. We are not asked to prove
that against 7B, but it is worth keeping in mind when reading the table - if the
smallest model with the most trainable parameters wins, that is the effect
showing up.

---

## Results table - one row per run

| run_id | owner | model | params | format | ft_method | trainable % | empathy | specificity | strategy | physio_ground | fluency | safety | train time | VRAM | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Fill in the failures too. A configuration that did not work is a result, and
otherwise someone retries it by accident in a fortnight.

---

## Settled with Stiti, 28 Aug

- **Training data: the `Modified_JSON` folder only** - the same set the website
  is built from, which is already in this repository at
  `website/public/data/json/`. Nothing else, so we are not training on a mix of
  old and re-verified text.
- **No Llama 7B versus new comparison is required.** The task is to find a
  replacement for 7B because it is too large, not to prove an improvement over
  it. So we compare candidates against each other and against our own baseline
  configuration - the 7B numbers are not needed, which saves a slow run.

## Decided since, and worth reading before you train

- **Participant 1 uses `_modified_phyS`** (Stiti, 28 Aug). Excluded file is
  handled in `make_splits.py`; totals are 54 conversations, 993 turns, 1986
  strings.
- **Loss is masked to the completion** - from `### Response:` to `<EOS>`, prompt
  tokens excluded. Not a style preference: the completion is 43% of a case1
  string but 22% of a case2 string, so unmasked loss weights the two cases
  differently by construction and confounds the formatting experiment before it
  starts. A fixed 417-character instruction header also repeats on all 993
  turns, and there is no reason to spend gradient on reproducing it.
- **No card on the CSE cluster does bfloat16.** Compute capability tops out at
  7.0 (V100). Every run is fp16 with fp32 master weights, about 12 bytes/param.
  `torch.cuda.is_bf16_supported()` returns True on a V100 anyway - it counts
  emulated bf16 - so train.py checks compute capability instead.

## The training script

`model/scripts/train.py` runs one config and writes `model/runs/<run_id>/run.json`.

    python3 model/scripts/train.py model/configs/baseline.json --smoke   # no GPU
    python3 model/scripts/train.py model/configs/baseline.json

`--smoke` tokenises everything, prints where the loss mask starts and stops, and
exits before loading weights. Run it after every config change. Twenty seconds on
a laptop, and the only cheap way to catch a masking bug.

Do not edit train.py to get a different experiment. Copy a config, give it a new
`run_id`, change the one field. If an experiment cannot be written as a config,
raise it on the group rather than forking the script.

Three defects found while writing it, each of which would have cost server time:

- **The baseline pointed at a model that does not exist.** `Qwen/Qwen3-1.7B-Instruct`
  is not on the Hub - Qwen3 ships one instruct repo per size with no suffix. Now
  `Qwen/Qwen3-1.7B`.
- **HF Trainer shuffles the training dataloader by default.** The formatting lane
  is entirely about example order, so a shuffling sampler collapses interleaved,
  batched and randomised into one experiment and yields three identical rows for
  no visible reason. train.py forces a sequential sampler and disables
  `group_by_length` for the same reason. Anyone writing their own loop needs both.
- **27% of turns carried mojibake** - 271 of 993, 974 occurrences, an apostrophe
  stored as 'Itâ\x80\x99s' - almost all inside `ai_text`, which is the
  span the loss is computed on, so the model would have learned to emit the broken
  bytes. Repaired in `dataset.py` so every lane gets it. The generator that writes
  `website/public/data/json` still emits it and needs the same fix at source.

Measured rather than assumed: the longest tokenised string is 661 tokens against
a 2048 window, so nothing truncates today. Supervised tokens are 23% of the
total, which is the case1/case2 asymmetry the masking decision was about.

## Still open

- **Hardware: settled.** SLURM cluster, login node 10.5.18.100, submit with
  `sbatch model/scripts/train.sbatch <config>`. Everything targets
  `gpupart_v100` (gnode1, 2x V100-32GB) because the other partitions are 16GB
  and 8GB. Environment lives at `~/.venv/psychobase`, built by
  `model/scripts/server_setup.sh`.
- **Is there a stage 1?** Siddaarth asked where the stage-1 data is. Nothing in
  the brief or the architecture deck describes two-stage fine-tuning, and case1
  and case2 are two views of the same turn rather than two stages. If two-stage
  means general emotional-support pretraining before our physiological data,
  then no stage-1 corpus was supplied and we would have to source one - a
  question for Stiti rather than an assumption to make.
