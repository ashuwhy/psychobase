# Results

One row per run. Add a row the moment a run finishes, including the ones that
went badly - a configuration that failed is a result, and otherwise someone
retries it by accident in a fortnight.

Every row must be produced on the frozen test split in `model/splits.json`,
scored by the shared harness. A row measured any other way is not comparable
with the rest of the table and should say so in **notes**.

## How to fill a row

- **run_id** - short and unique: `baseline`, `qwen3-1.7b-batched`, `smollm3-lora`
- **config** - path to the config file that produced it, so the run can be repeated
- **trainable %** - share of parameters actually updated. "Better" that costs
  20x the trainable parameters is a different result from "better" that does not
- **scores** - mean over the test split, 1-5, from the shared harness
- **notes** - anything that would change how someone reads the row: crashed and
  resumed, ran out of memory at a larger batch, validation loss still falling at
  the last epoch

| run_id | owner | config | model | params | format | ft method | trainable % | empathy | specificity | strategy | physio ground | fluency | safety | train time | peak VRAM | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | Ashutosh | `configs/baseline.json` | Qwen3-1.7B | 1.72B | interleaved | full | 100% | | | | | | | 26 min | ~21GB | trained, not yet scored. eval_loss 2.083/2.144/2.360, **best epoch 1** |
| smollm2-1.7b | Ashutosh | `configs/smollm2-1.7b.json` | SmolLM2-1.7B-Instruct | 1.71B | interleaved | full | 100% | | | | | | | | | trained, not yet scored. eval_loss 1.896/**1.882**/1.909, **best epoch 2**. Beats the baseline by 0.201 and overfits far less |
| smollm3-3b | Ashutosh | `configs/smollm3-3b.json` | SmolLM3-3B | 3.08B | interleaved | full | 100% | | | | | | | 2h00 | ~27GB/card | trained, not scored. eval_loss **1.936**/1.963/2.240, best epoch 1. FSDP over 2 V100s, adamw_torch. Compare only against smollm2-1.7b-fsdp |
| smollm2-1.7b-fsdp | Ashutosh | `configs/smollm2-1.7b-fsdp.json` | SmolLM2-1.7B-Instruct | 1.71B | interleaved | full | 100% | | | | | | | 1h07 | ~19GB/card | trained, not scored. eval_loss 2.074/1.998/**1.989**, best epoch **3 of 3 - did not converge**. Matched control for smollm3-3b |
| smollm2-1.7b-fsdp-e6 | Ashutosh | `configs/smollm2-1.7b-fsdp-e6.json` | SmolLM2-1.7B-Instruct | 1.71B | interleaved | full | 100% | | | | | | | | | queued, 6 epochs. Exists because the 3-epoch run never reached a minimum |
| smollm3-3b-e6 | Ashutosh | `configs/smollm3-3b-e6.json` | SmolLM3-3B | 3.08B | interleaved | full | 100% | | | | | | | | | queued, 6 epochs. Matched partner for the above |
| llama3.2-1b | Ashutosh | `configs/llama3.2-1b.json` | Llama-3.2-1B-Instruct | 1.24B | interleaved | full | 100% | | | | | | | | | trained, not yet scored. eval_loss **2.162**/2.303/2.499, best epoch 1. Worst of the three and the fastest to overfit |

## Credit

The **owner** column is whoever actually set up and ran the row, not whoever the
task split pencilled in for it. The five model-lane runs were all configured and
executed by Ashutosh on the CSE cluster, including the Llama one that the
original split had against another name.

The same applies to the evaluation harness. It was assigned to Nithish and
written by Ashutosh on 3 Sep - `scripts/evaluate.py`, generation plus strategy
F1, physiological grounding, specificity and fluency - so it is credited to
Ashutosh. The empathy and safety scoring pass has not been started and stays
with Nithish. An assignment is not a contribution until there is code, and code
counts for whoever wrote it.

## What changes from the baseline, and who owns it

| axis | values to try | owner |
|---|---|---|
| model | Qwen3-1.7B (baseline), SmolLM2-1.7B, SmolLM3-3B, Llama-3.2-1B | Ashutosh |
| format | interleaved (baseline), batched, randomised | Siddaarth |
| fine-tuning | full (baseline), QLoRA, DoRA, rsLoRA, LoRA+, IA3 | Krishna |
| evaluation harness | `scripts/evaluate.py` - **not started** | assigned: Nithish |

Change one of these per run. Two changes in one row cannot be attributed and
the row is wasted work.

## Provenance gap, so nobody trips on it later

The `baseline` and `smollm2-1.7b` rows were produced before `run.json` started
recording `effective_batch` and `world_size`, so those fields read null for them.
Both were single-GPU runs at per-device 2 and accumulation 8, which is an
effective batch of 16, the same as every other row - the numbers are sound, the
manifest is just thinner. Rerun them if a reviewer wants complete manifests
across the table; nothing about the results changes.

## What the runs so far say

Both are trained but neither is scored yet - the numbers below are validation
loss, which picks checkpoints, not the harness scores that fill the table.

SmolLM2-1.7B beats Qwen3-1.7B by 0.20 in validation loss at nearly identical
parameter count, 1.71B against 1.72B, and beats Llama-3.2-1B by 0.28. All three
gaps are far above the measured noise floor.

The more useful difference is the shape of the curves:

    smollm2   1.896  1.882  1.909     best epoch 2, flat        +0.01
    baseline  2.078  2.140  2.360     best epoch 1, degrades    +0.28
    llama     2.162  2.303  2.499     best epoch 1, degrades    +0.34

Overfitting severity tracks the model rather than its size. SmolLM2 at 1.71B is
nearly flat across three epochs while Qwen3 at 1.72B climbs 0.28 - same size,
same data, same hyperparameters. On a corpus this small, how little a model
degrades is a more actionable property than where it lands, because more
participants is not an option and more epochs actively hurts.

Three baseline runs across two torch versions gave 2.076, 2.083 and 2.078, so
the 0.007 floor survived the 2.5.1 to 2.6.0 upgrade.

SmolLM3-3B lands at 1.936, behind SmolLM2-1.7B at 1.882 despite 1.8x the
parameters, and it degrades 0.30 across three epochs where SmolLM2 degrades 0.01.
**The matched control reversed this.** Under identical sharding and optimiser,
SmolLM3-3B reaches 1.9355 and SmolLM2-1.7B reaches 1.9893, so the 3B model wins
by 0.054 and the apparent "bigger is worse" was an artefact of comparing an
FSDP/adamw_torch run against a single-card 8-bit run.

That comparison still has a defect, so do not quote it as final either.
SmolLM2-FSDP peaked at **epoch 3 of 3** with its curve still falling
(2.074, 1.998, 1.989), meaning it had not converged and 1.9893 is an upper bound
rather than its minimum, while SmolLM3 peaked at epoch 1 and was finished. The
honest reading is "3B beats an *unconverged* 1.7B by 0.054". `smollm2-1.7b-fsdp-e6`
and `smollm3-3b-e6` rerun the pair at six epochs so both reach a real minimum.

**The training setup is outweighing model size.** Single-card SmolLM2 with the
8-bit optimiser reached 1.8816; the same model under FSDP with adamw_torch
reached 1.9893. That 0.108 gap is twice the 0.054 size effect. Before anyone
writes that a bigger model helps, note that how the model is trained is moving
these numbers further than how big it is.

Same data, same hyperparameters, same size. Qwen3 overfits 993 turns quickly and
SmolLM2 barely does. Whatever the harness scores end up being, that difference in
robustness to a small corpus is worth reporting, because it is the constraint
this whole project is working under.

It also settles the epochs question empirically: the two models peak at different
epochs, so a fixed epoch count would have read the wrong checkpoint for one of
them. Keep `epochs: 3` and keep letting each run find its own minimum.

## Reading the table

With ~700 training turns, differences of a tenth of a point on a 1-5 scale are
noise, not signal. Before claiming a configuration wins, check that the gap is
larger than the spread from re-running the same configuration.

That spread now has a floor, measured rather than assumed. The baseline was run
twice at the *same* seed and gave eval_loss 2.076 and 2.083 - a gap of 0.007
from GPU nondeterminism alone, since atomics in the backward pass do not
reassociate identically between runs. A different seed will be wider. Treat
0.007 as the absolute floor below which nothing is a result, and measure the
cross-seed spread before publishing any ranking.

Every run also picks its own best epoch on validation loss rather than taking
the last one. The baseline peaks at epoch 1 and degrades monotonically after
(2.083 -> 2.144 -> 2.360), so **best epoch belongs in the table** - a model that
wins only by stopping earlier is a different claim from one that wins outright.
