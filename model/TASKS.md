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

## Where this stands, 3 Sep

The foundation, the cluster and the model lane are done. The training script,
the submission scripts and the evaluation harness are in the repo and working.
Four models are trained with a fifth control finishing.

What is not done is the other three lanes. Siddaarth's and Krishna's are not
blocked by anything and have not started; the evaluation harness runs but its
empathy and safety columns need a rubric and a human pass before the results
table has anything in it.

### Ashutosh - splits, baseline, cluster, model lane, eval harness - DONE

Everything ticked here was built and run by Ashutosh. Where a lane was assigned
to somebody else and the work was done here anyway, it is recorded here, and only
the outstanding part stays under the original name.

- [x] Conversation-level split, frozen in `splits.json`, 69/15/15 by turns
      (`scripts/make_splits.py`)
- [x] Shared loader `scripts/dataset.py` - import this rather than reading the
      JSON directory, or we end up with four loaders that disagree
- [x] Baseline configuration in `configs/baseline.json`
- [x] Results table in `RESULTS.md`
- [x] CSE server access, environment, and submission scripts - see Hardware below
- [x] Trainer `scripts/train.py`, one config in, checkpoint plus `run.json` out
- [x] Four model runs trained and recorded, plus a matched control
- [x] Evaluation harness `scripts/evaluate.py` - generation, strategy F1,
      physiological grounding, specificity and fluency, plus `evaluate.sbatch`.
      Built 3 Sep because four trained models with no scorer was the only thing
      standing between this project and a results table. Empathy and safety are
      left null by design and belong to the scoring pass below.

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
  (26 groups, not 55). `--group-by file` still exists but is effectively closed:
  every row in `RESULTS.md` was produced against the frozen split, and changing
  it now invalidates all of them.

### Model lane - four models trained, one control running

Validation loss only. These pick checkpoints; they are not harness scores and
they do not go in the results columns.

    smollm2-1.7b   1.882  ep2   1.896 1.882 1.909   flat      +0.01
    smollm3-3b     1.936  ep1   1.936 1.963 2.240   degrades  +0.30
    baseline       2.078  ep1   2.078 2.140 2.360   degrades  +0.28
    llama3.2-1b    2.162  ep1   2.162 2.303 2.499   degrades  +0.34

SmolLM2-1.7B wins and barely overfits. Qwen3-1.7B is the same size to within 10M
parameters and climbs 0.28, so on this corpus the pretraining family matters
more than the parameter count.

**Do not quote "3B is worse than 1.7B" yet.** FSDP forced SmolLM3 onto
`adamw_torch`, because bitsandbytes has no DTensor sharding rule, so it differs
from the single-card SmolLM2 in size *and* optimiser. `smollm2-1.7b-fsdp` runs
SmolLM2 under identical sharding and optimiser and is the only row that makes
the size comparison readable. Near 1.88 means the size effect is real; near 1.94
means we are looking at the optimiser.

Two more things that hold for everyone's runs:

- **Every run peaks at epoch 1 or 2, never 3.** The configs select the best epoch
  on validation loss rather than the last. Before that fix, `save_total_limit`
  was deleting the good checkpoint and keeping the most overtrained one.
- **The noise floor is measured, not assumed.** The same config at the same seed,
  three times across two torch versions, gave 2.076 / 2.083 / 2.078. Nothing
  under 0.007 is a result.

### Nithish - empathy and safety scoring - NOT STARTED

The harness runs and produces generations for every model. What remains is the
half that genuinely needs a person, and none of it has been started.

- [ ] **Write the 1-5 rubric for empathy and safety.** These come out null from
      `evaluate.py` on purpose - a word-list proxy for empathy produces a number
      that looks like a result and is not one. Without an agreed rubric, two
      people scoring the same `generations.jsonl` will not agree with each other,
      and the column is worthless either way.
- [ ] Score `generations.jsonl` against that rubric, by hand or with a judge model
- [ ] Sanity-check against the scores we produced by hand: if the harness
      disagrees wildly with the Google Doc rows for the same responses, the
      harness is wrong and everything downstream inherits that
- [ ] Tighten `physio_grounding` against the rule in
      `evaluation/scripts/render.py` - grounding is supposed to be qualitative,
      so a response that quotes raw values should not score well. The current
      mention-rate metric does not enforce that and needs someone who knows the
      rendering rules to fix it.

### Siddaarth - data formatting - NOT BLOCKED, nothing started

The pipeline exists and the cluster is up, so this is three sbatch commands.
Copy `configs/baseline.json`, change `data.format`, give it a new `run_id`.

- [x] One model training end to end on the baseline configuration - done, and it
      unblocked this lane along with Krishna's
- [ ] Then the three arrangements from the meeting, on the baseline model and
      method: interleaved (case 1, case 2, case 1...), batched (all case 1s then
      all case 2s), randomised
- [ ] Watch for this: the batched arrangement risks the model learning "the
      physiological summary appears in the second half" rather than learning to
      use it. If batched scores oddly high or oddly low, suspect that before
      believing the number

### Krishna - fine-tuning method - NOT BLOCKED, nothing started

`train.py` reads `finetune.method` from the config. Same pattern: copy a config,
change the one field, new `run_id`, sbatch it.

- [ ] Alternatives to LoRA, suited to this data size:
      - full fine-tuning (viable at 1B, and the one most likely to win here)
      - QLoRA, if memory is the binding constraint
      - DoRA, rsLoRA, LoRA+ - variants that behave better on small data
      - IA3 or prefix tuning - far fewer parameters again
- [ ] Report trainable parameter count alongside each score. "Better" that costs
      20x the trainable parameters is a different result from "better" that
      does not

---

## Model selection - SETTLED, all four run

Chosen so that every pair differs in exactly one thing: Qwen3-1.7B against
SmolLM2-1.7B varies the family at fixed size, SmolLM2 against SmolLM3 varies size
at fixed family, Llama-3.2-1B adds a third family and the cheapest run.

    Qwen/Qwen3-1.7B                      2.03B on the Hub, 1.72B loaded, Apache 2.0
    HuggingFaceTB/SmolLM2-1.7B-Instruct  1.71B, Apache 2.0
    HuggingFaceTB/SmolLM3-3B             3.08B, Apache 2.0, needs both V100s
    meta-llama/Llama-3.2-1B-Instruct     1.24B, gated, licence accepted 3 Sep

Rejected: Llama-3.2-3B (gated, non-OSI licence, will not fit 32GB under full
fine-tuning), gemma-2-2b-it (gated, licence). The original list below is kept
only as a record of what was considered - do not train from it:

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

## Evaluation harness

`model/scripts/evaluate.py` scores one finished run on the frozen test split.

    sbatch model/scripts/evaluate.sbatch model/runs/baseline
    python3 model/scripts/evaluate.py model/runs/baseline --limit 20

Greedy generation, temperature 0, both cases per turn, writing `scores.json` and
`generations.jsonl` beside the checkpoint. Do not add sampling: two evaluations
of one checkpoint must agree exactly, or a gap between two rows might be
sampling noise instead of a difference between models.

Four of the six parameters are computed:

    strategy_faithfulness   F1 over normalised, multi-label strategy sets
    physio_grounding        mention rate, plus whether the physiological summary
                            actually changed the answer versus case1
    specificity             non-filler content ratio, and echo of the user's own words
    fluency                 4-gram repetition and truncation rate

Two are left null on purpose. Empathy and safety need a person or a judge model,
and a word-list proxy would produce a number that looks like a result and is not
one. `generations.jsonl` is written for exactly that scoring pass.

**The strategy labels are messy and the metric had to be built around it.** 206
raw surface forms across 993 turns collapse to 132 once case and spacing are
normalised; seven collisions alone cover 336 turns, including
`Emotional Validation` against `EmotionalValidation` at 135. Exact string
matching would have marked models wrong for whitespace. 173 turns carry two
strategies, so this is multi-label F1, not accuracy. 67 turns have a blank
strategy - all of them in train, none in validation or test, so test scoring is
well defined, but that is luck rather than design.

`physio_changed_answer` is the one to watch. It is the share of test turns where
the case2 response differs from the case1 response at all. If that is near zero,
the model is ignoring the physiological summary, and the premise of the project
is not being tested no matter what the other numbers say.

## Cluster etiquette, learned the hard way

Submit the single-GPU jobs before the two-GPU ones. A `--gres=gpu:2` job sitting
at the head of your queue waits on `(Resources)` whenever anyone else holds one
card on gnode1, and every single-GPU job behind it waits on `(Priority)` even
though a card is free and idle. Three runs sat blocked for over an hour that way.
Cancelling the two-GPU jobs started the next one within fifteen seconds.

gnode1 is shared. Check `squeue -p gpupart_v100` before assuming the node is
yours - it usually is not.

## Model lane - what is measured and what is not

Everything below is Ashutosh's lane and all of it is queued or done.

**Done and scored on clean data:** Qwen3-1.7B, SmolLM2-1.7B, Llama-3.2-1B.
SmolLM2 wins - best loss at 1.883, best specificity at 0.469, repetition 0.0005
against the baseline's 0.014, and it never truncates.

**Running:** two seed replicates and a three-point learning rate sweep on
SmolLM2, then the 6-epoch sharded pair that settles whether SmolLM3-3B beats
SmolLM2-1.7B on clean data.

**The one result that needs saying out loud: strategy prediction does not work.**
Always answering "Emotional Validation" scores 0.1613 on the test split. The
Qwen3 baseline scores 0.1613 - identical, because it emits the majority label on
every turn - and the other two score below it. Collapsing 132 labels to the top
12 moves F1 by 0.006, so this is not label sparsity, and format compliance is
1.0 with zero blanks, so it is not a formatting failure. The models emit a real
strategy every time and it is the same one. 620 training turns over 37 test
strategies is not enough to learn the mapping.

Report it as a negative result. Do not let `strategy_faithfulness` appear in a
summary as if the models can do it.

**Not measured, and honest to say so:** empathy and safety, which need the rubric
and human pass that has not started.

## Still open

- **Hardware: settled.** SLURM cluster, login node 10.5.18.100, submit with
  `sbatch model/scripts/train.sbatch <config>`. Everything targets
  `gpupart_v100` (gnode1, 2x V100-32GB) because the other partitions are 16GB
  and 8GB. Environment lives at `~/.venv/psychobase`, built by
  `model/scripts/server_setup.sh`.
- **Empathy and safety need a scoring pass.** `generations.jsonl` exists for
  every scored run and nothing reads it yet. Either a person scores 1-5 against
  a rubric, or a judge model does with the rubric in the prompt - but the rubric
  has to be written and agreed first, or two people scoring the same file will
  not agree with each other.

- **Is there a stage 1?** Siddaarth asked where the stage-1 data is. Nothing in
  the brief or the architecture deck describes two-stage fine-tuning, and case1
  and case2 are two views of the same turn rather than two stages. If two-stage
  means general emotional-support pretraining before our physiological data,
  then no stage-1 corpus was supplied and we would have to source one - a
  question for Stiti rather than an assumption to make.
