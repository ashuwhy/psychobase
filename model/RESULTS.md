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
| smollm3-3b | Ashutosh | `configs/smollm3-3b.json` | SmolLM3-3B | 3.08B | interleaved | full | 100% | | | | | | | | | blocked - 37GB fp16 exceeds one 32GB V100, needs both GPUs on gnode1 |
| llama3.2-1b | Nithish | `configs/llama3.2-1b.json` | Llama-3.2-1B-Instruct | 1.24B | interleaved | full | 100% | | | | | | | | | blocked - gated repo, needs the Llama 3.2 licence accepted on huggingface.co |

## What changes from the baseline, and who owns it

| axis | values to try | owner |
|---|---|---|
| model | Qwen3-1.7B (baseline), SmolLM2-1.7B, SmolLM3-3B, Llama-3.2-1B | Ashutosh, Nithish |
| format | interleaved (baseline), batched, randomised | Siddaarth |
| fine-tuning | full (baseline), QLoRA, DoRA, rsLoRA, LoRA+, IA3 | Krishna |

Change one of these per run. Two changes in one row cannot be attributed and
the row is wasted work.

## What the first two runs already say

Both are trained but neither is scored yet - the numbers below are validation
loss, which picks checkpoints, not the harness scores that fill the table.

SmolLM2-1.7B beats Qwen3-1.7B by 0.201 in validation loss at nearly identical
parameter count, 1.71B against 1.72B. That is 29x the measured noise floor, so
it is a real difference rather than run-to-run variation.

The more useful difference is the shape of the curves:

    baseline  2.083  2.144  2.360     best epoch 1, degrades hard
    smollm2   1.896  1.882  1.909     best epoch 2, nearly flat

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
