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
| baseline | Ashutosh | `configs/baseline.json` | Qwen3-1.7B | 1.72B | interleaved | full | 100% | | | | | | | 26 min | ~21GB | trained, not yet scored. eval_loss 2.083/2.144/2.360 over 3 epochs - **best is epoch 1**, weights in `runs/baseline/final` |
| smollm2-1.7b | Ashutosh | `configs/smollm2-1.7b.json` | SmolLM2-1.7B-Instruct | 1.71B | interleaved | full | 100% | | | | | | | | | running |
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
