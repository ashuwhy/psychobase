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

### Ashutosh - splits, baseline, results table

- [ ] Conversation-level train / validation / test split, written to disk as a
      list of which conversation ids are in which split, and committed
- [ ] Baseline configuration: one model, one format, one method, fixed seed,
      fixed hyperparameters - the thing every experiment is a diff against
- [ ] Results table with the schema below, one row per run
- [ ] Confirm what hardware we actually have (see Open questions) - it sets the
      ceiling on model size for everyone

### Siddaarth - evaluation harness

- [ ] Takes a model's generated responses on the test split, returns the six
      parameters, reproducible between people and across days
- [ ] Reuse the rules already encoded in `evaluation/scripts/render.py` -
      particularly that physiological grounding must be qualitative, since a
      response that quotes values should not score well on it
- [ ] Sanity-check it against the scores we produced by hand: if the harness
      disagrees wildly with the Google Doc rows for the same responses, the
      harness is wrong and everything downstream inherits that

### Nithish - training pipeline and data formatting

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

Split between Ashutosh and Siddaarth, 1-2 models each, all on the baseline
format and method so the model is the only thing that changed. Verify what is
current before committing - this list moves quickly:

- Qwen2.5 1.5B / 3B Instruct
- Llama 3.2 1B / 3B Instruct
- SmolLM3-3B (reported to beat Llama-3.2-3B and Qwen2.5-3B at that size)
- Phi-3.5-mini (3.8B)
- Gemma 2 2B

Record VRAM, training time and inference latency per model. A model we cannot
run on the hardware we have is not a candidate however well it scores.

**The hypothesis worth testing directly:** at ~2,000 samples a fully fine-tuned
1B model will likely beat a LoRA-adapted 7B, because LoRA updates very few
parameters relative to how far this task sits from pretraining. That is the
reasoning behind this whole phase, so it deserves a measurement rather than an
assumption.

---

## Results table - one row per run

| run_id | owner | model | params | format | ft_method | trainable % | empathy | specificity | strategy | physio_ground | fluency | safety | train time | VRAM | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Fill in the failures too. A configuration that did not work is a result, and
otherwise someone retries it by accident in a fortnight.

---

## Open questions - worth settling before Monday

- **Hardware.** What are we training on - Colab, a lab machine, personal GPUs?
  This decides whether 3B full fine-tuning is even reachable, and everyone needs
  the same answer before picking models.
- **Is the training data the updated JSON?** Task 5 wrote our verified summaries
  and responses into `training_string_case2` for some participants but not all.
  Training on a mix of old and new text would confound every result in the
  table. Confirm with Stiti which files are the training set.
- **Does the baseline get re-run?** For the comparison to include "what we had
  before", Llama 7B + LoRA needs scoring through the same harness on the same
  split. Without it we can show which new configuration is best, but not that
  any of them beat what we started with.
