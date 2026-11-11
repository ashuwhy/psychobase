"""Write the deck's TikZ charts from the run table, the scored generations and the multi-turn data,
so every number on a chart comes from a file, not from a slide.

Usage: python3 docs/final-deck/make_charts.py
Reads counts only from the stage2_mt files; no row text reaches a chart.
"""
import csv
import gzip
import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent.parent
OUT = HERE / 'charts'
OUT.mkdir(exist_ok=True)
DOWNLOADS = Path.home() / 'Downloads'

RESULTS = (REPO / 'model' / 'RESULTS.md').read_text()
SCORED = [json.loads(l) for l in open(REPO / 'model' / 'results' / 'smollm2-1.7b' / 'generations_scored.jsonl')]
SPLITS = {s: [json.loads(l) for l in gzip.open(DOWNLOADS / f'stage2_mt_{s}.jsonl.gz', 'rt')] for s in ('train', 'val', 'test')}

# run_id -> label on the chart; the order is the order on the slide
RUNS = [('smollm2-1.7b', 'SmolLM2-1.7B, lr 1e-5 (final)', 'saffron'),
        ('smollm2-1.7b-1gpu-lr2e5', 'SmolLM2-1.7B, lr 2e-5', 'iris'),
        ('smollm3-3b-lr2e6', 'SmolLM3-3B, lr 2e-6', 'iris'),
        ('baseline', 'Qwen3-1.7B interleaved', 'muted'),
        ('baseline-randomised', 'Qwen3-1.7B randomised', 'muted'),
        ('llama3.2-1b', 'Llama-3.2-1B', 'muted'),
        ('baseline-batched', 'Qwen3-1.7B batched', 'muted')]


def first_float(cell):
    m = re.search(r'\d+\.\d+|\d+', cell)
    return float(m.group()) if m else None


def run_table():
    head = None
    rows = {}
    for line in RESULTS.splitlines():
        if not line.startswith('|') or line.startswith('|---'):
            continue
        cells = [c.strip().strip('*`').strip() for c in line.strip('|').split('|')]
        if cells[0] == 'run_id':
            head = cells
        elif head and len(cells) == len(head):
            rows[cells[0]] = dict(zip(head, cells))
    return rows


def write(name, lines):
    (OUT / f'{name}.tex').write_text('\n'.join(lines) + '\n')


def val_loss():
    # Dot plot, not bars: the runs sit between 1.87 and 2.20, and bars from zero would all look the same height
    rows = run_table()
    lo, hi, w, rh = 1.85, 2.20, 5.6, 0.42
    sx = w / (hi - lo)
    out = []
    for t in (1.9, 2.0, 2.1, 2.2):
        x = (t - lo) * sx
        out.append(f'\\draw[rule] ({x:.3f},0.25) -- ({x:.3f},{-(len(RUNS) - 1) * rh - 0.25:.3f});')
        out.append(f'\\node[font=\\tiny,text=muted,anchor=north] at ({x:.3f},{-(len(RUNS) - 1) * rh - 0.25:.3f}) {{{t:.1f}}};')
    for i, (rid, label, col) in enumerate(RUNS):
        v = first_float(rows[rid]['eval_loss'])
        x, y = (v - lo) * sx, -i * rh
        out.append(f'\\draw[rule,line width=.6pt] (0,{y:.3f}) -- ({x:.3f},{y:.3f});')
        out.append(f'\\fill[{col}] ({x:.3f},{y:.3f}) circle (1.1mm);')
        out.append(f'\\node[anchor=east,font=\\scriptsize] at (-0.1,{y:.3f}) {{{label}}};')
        out.append(f'\\node[anchor=west,font=\\tiny,text=muted] at ({x + 0.14:.3f},{y:.3f}) {{{v:.3f}}};')
    out.append(f'\\node[anchor=north,font=\\tiny,text=muted] at ({w / 2:.3f},{-(len(RUNS) - 1) * rh - 0.6:.3f}) {{validation loss at the best epoch, lower is better}};')
    write('val_loss', out)


def strategy_f1():
    # The majority answer, "Emotional Validation" on every turn, scores 0.161 on the same 155 turns
    rows = run_table()
    sx, rh, base = 22.0, 0.42, 0.161
    out = []
    bottom = -(len(RUNS) - 1) * rh - 0.25
    out.append(f'\\draw[ink,dashed,line width=.7pt] ({base * sx:.3f},0.3) -- ({base * sx:.3f},{bottom:.3f});')
    for i, (rid, label, col) in enumerate(RUNS):
        f1 = rows[rid]['strategy F1']
        y = -i * rh
        out.append(f'\\node[anchor=east,font=\\scriptsize] at (-0.1,{y:.3f}) {{{label}}};')
        if not f1 or f1 == '-':
            out.append(f'\\node[anchor=west,font=\\tiny,text=muted] at (0.05,{y:.3f}) {{not scored}};')
            continue
        v = float(f1)
        out.append(f'\\fill[{col}] (0,{y - 0.13:.3f}) rectangle ({v * sx:.3f},{y + 0.13:.3f});')
        out.append(f'\\node[anchor=west,font=\\tiny,text=muted,fill=bg] at ({v * sx + 0.05:.3f},{y:.3f}) {{{v:.3f}}};')
    out.append(f'\\node[anchor=north,font=\\tiny\\bfseries,text=ink,align=center] at ({base * sx:.3f},{bottom:.3f}) {{always Emotional\\\\Validation: {base}}};')
    write('strategy_f1', out)


def lr_sweep():
    pts = [(m.group(1), float(m.group(2))) for m in re.finditer(r'^\s+(\de-\d)\s+(\d\.\d+)', RESULTS, re.M)]
    lo, hi, w, h = 1.87, 1.91, 4.2, 2.0
    sy = h / (hi - lo)
    xs = [i * w / (len(pts) - 1) for i in range(len(pts))]
    out = []
    for t in (1.87, 1.88, 1.89, 1.90, 1.91):
        y = (t - lo) * sy
        out.append(f'\\draw[rule] (-0.1,{y:.3f}) -- ({w + 0.1:.3f},{y:.3f}); \\node[anchor=east,font=\\tiny,text=muted] at (-0.15,{y:.3f}) {{{t:.2f}}};')
    out.append('\\draw[iris,line width=1pt] ' + ' -- '.join(f'({x:.3f},{(v - lo) * sy:.3f})' for x, (_, v) in zip(xs, pts)) + ';')
    for x, (lr, v) in zip(xs, pts):
        col = 'saffron' if lr == '1e-5' else 'iris'
        out.append(f'\\fill[{col}] ({x:.3f},{(v - lo) * sy:.3f}) circle (1.1mm);')
        out.append(f'\\node[anchor=south,font=\\tiny,text=muted] at ({x:.3f},{(v - lo) * sy + 0.08:.3f}) {{{v:.3f}}};')
        out.append(f'\\node[anchor=north,font=\\scriptsize] at ({x:.3f},-0.1) {{{lr}}};')
    write('lr_sweep', out)


def score_bars():
    # Both rubrics are 1-5. Empathy never reached 5 on any of the 155 turns, so the empty bar stays on the chart
    rh, sx = 0.34, 0.032
    out = []
    for col, (key, title, colour) in enumerate([('empathy', 'Empathy', 'iris'), ('safety', 'Safety', 'saffron')]):
        cnt = Counter(r[key] for r in SCORED)
        mean = sum(k * v for k, v in cnt.items()) / len(SCORED)
        x0 = col * 7.3
        out.append(f'\\node[anchor=south west,font=\\scriptsize\\bfseries,inner sep=0] at ({x0 - 0.35:.3f},0.3) {{{title}, mean {mean:.2f} of 5}};')
        for i, s in enumerate(range(5, 0, -1)):
            n, y = cnt.get(s, 0), -i * rh
            out.append(f'\\node[anchor=east,font=\\scriptsize] at ({x0 - 0.08:.3f},{y:.3f}) {{{s}}};')
            if n:
                out.append(f'\\fill[{colour}] ({x0:.3f},{y - 0.12:.3f}) rectangle ({x0 + n * sx:.3f},{y + 0.12:.3f});')
            out.append(f'\\node[anchor=west,font=\\tiny,text=muted] at ({x0 + n * sx + 0.05:.3f},{y:.3f}) {{{n}}};')
    write('score_bars', out)


def sources():
    names = {'stage2': 'Stage 2 conversations', 'stage1_replay': 'Stage 1 replay (ExTES)',
             'new_referral': 'new: referral', 'new_direct': 'new: direct answer', 'new_disengage': 'new: disengaging user',
             'new_repair': 'new: repair after a miss', 'new_norepeat': 'new: no repetition'}
    cnt = Counter(r['source'] for r in SPLITS['train'])
    sx, rh = 4.4 / max(cnt.values()), 0.36
    out = []
    for i, (k, v) in enumerate(cnt.most_common()):
        y = -i * rh
        col = 'saffron' if k.startswith('new_') else ('iris' if k == 'stage2' else 'muted')
        out.append(f'\\fill[{col}] (0,{y - 0.13:.3f}) rectangle ({v * sx:.3f},{y + 0.13:.3f});')
        out.append(f'\\node[anchor=east,font=\\scriptsize] at (-0.08,{y:.3f}) {{{names[k]}}};')
        out.append(f'\\node[anchor=west,font=\\tiny,text=muted] at ({v * sx + 0.05:.3f},{y:.3f}) {{{v}}};')
    write('sources', out)


def split_table():
    rows = []
    for s, rr in SPLITS.items():
        st2 = [r for r in rr if r['source'] == 'stage2']
        convs = len({r['dialogue_id'] for r in st2 if r['case'] == 1})
        people = len({r['person'] for r in rr if 'person' in r})
        rows.append(f'{s} & {len(rr)} & {convs} & {people} & {max(r["turn_index"] for r in rr)} \\\\')
    write('split_table', ['\\begin{tabular}{@{}lrrrr@{}}', '\\toprule',
                          'split & turns & conversations & people & longest \\\\', '\\midrule', *rows, '\\bottomrule', '\\end{tabular}'])


def conversation_lengths():
    # One bar per length bin; each Stage 2 conversation counted once (its case-1 copy), all three splits
    lengths = Counter()
    for rr in SPLITS.values():
        lengths.update(r['dialogue_id'] for r in rr if r['source'] == 'stage2' and r['case'] == 1)
    bins = [(1, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 50)]
    counts = [sum(1 for n in lengths.values() if a <= n <= b) for a, b in bins]
    bw, gap, sy = 0.62, 0.22, 0.17
    out = []
    for i, ((a, b), n) in enumerate(zip(bins, counts)):
        x = i * (bw + gap)
        out.append(f'\\fill[iris] ({x:.3f},0) rectangle ({x + bw:.3f},{n * sy:.3f});')
        out.append(f'\\node[anchor=south,font=\\tiny,text=muted] at ({x + bw / 2:.3f},{n * sy:.3f}) {{{n}}};')
        out.append(f'\\node[anchor=north,font=\\tiny] at ({x + bw / 2:.3f},-0.03) {{{"$\\le$10" if a == 1 else f"{a}-{b}"}}};')
    out.append(f'\\draw[ink] (-0.1,0) -- ({len(bins) * (bw + gap) - gap + 0.1:.3f},0);')
    out.append(f'\\node[anchor=north,font=\\tiny,text=muted] at ({(len(bins) * (bw + gap) - gap) / 2:.3f},-0.35) {{turns per conversation, {len(lengths)} conversations}};')
    write('conversation_lengths', out)


def physio_ranges():
    # The severity table in ref/physio_ranges.txt: severity label, then EDA range, PR range, skin temperature
    text = (HERE / 'ref' / 'physio_ranges.txt').read_text().replace('–', '-')
    sev = re.findall(r'^(mild|moderate|severe) \((\d-\d)\)\n([\d.]+)-([\d.]+)\n(\d+)-(\d+)', text, re.M)
    colours = {'mild': 'iris!45', 'moderate': 'iris', 'severe': 'saffron'}
    # The doc writes severe as 5-6, which overlaps its own moderate 4-5; the simulator and the 0-6 scale call only 6 severe
    scores = {'severe': '6'}
    panels = [('EDA, $\\mu$S', 0.0, 0.8, (0.0, 0.2, 0.4, 0.6, 0.8), 2, 3), ('Pulse rate, bpm', 50, 120, (50, 70, 90, 110), 4, 5)]
    w, rh = 5.0, 0.36
    out = []
    for p, (title, lo, hi, ticks, a, b) in enumerate(panels):
        x0, sx = p * 6.6, w / (hi - lo)
        out.append(f'\\node[anchor=south west,font=\\scriptsize\\bfseries,inner sep=0] at ({x0:.3f},0.3) {{{title}}};')
        for t in ticks:
            x = x0 + (t - lo) * sx
            out.append(f'\\draw[rule] ({x:.3f},0.2) -- ({x:.3f},{-2 * rh - 0.2:.3f}); \\node[anchor=north,font=\\tiny,text=muted] at ({x:.3f},{-2 * rh - 0.2:.3f}) {{{t:g}}};')
        for i, row in enumerate(sev):
            y, v0, v1 = -i * rh, float(row[a]), float(row[b])
            out.append(f'\\fill[{colours[row[0]]},rounded corners=1pt] ({x0 + (v0 - lo) * sx:.3f},{y - 0.12:.3f}) rectangle ({x0 + (v1 - lo) * sx:.3f},{y + 0.12:.3f});')
            if p == 0:
                out.append(f'\\node[anchor=east,font=\\scriptsize] at ({x0 - 0.08:.3f},{y:.3f}) {{{row[0]} ({scores.get(row[0], row[1])})}};')
            out.append(f'\\node[anchor=west,font=\\tiny,text=muted,fill=bg] at ({x0 + (v1 - lo) * sx + 0.05:.3f},{y:.3f}) {{{row[a]}-{row[b]}}};')
    write('physio_ranges', out)


def percentile(xs, q):
    # linear interpolation between closest ranks, as numpy.percentile does by default
    xs = sorted(xs)
    k = (len(xs) - 1) * q / 100
    f = math.floor(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)


def channel_ranges():
    # Every minute of every turn window in the 54 website CSVs, one row per channel, each on its own axis.
    # Band = the ranges doc's typical worn range; bar = 1st to 99th percentile; whiskers = min and max; dot = median.
    vals = {}
    for f in (REPO / 'website' / 'public' / 'data' / 'raw_csv').glob('*.csv'):
        for r in csv.DictReader(open(f, encoding='utf-8', errors='replace')):
            for c in ('EDA', 'PR', 'SkinTemp', 'ACCEL', 'MET', 'ACT_COUNT'):
                if r[c]:
                    vals.setdefault(c, []).extend(x for x in json.loads(r[c].replace('nan', 'null')) if x is not None)
    # key, axis lo, hi, log axis, ticks, human worn range, differs from it
    rows = [('EDA', 0.01, 30, True, (0.01, 0.1, 1, 10), (0.05, 20), True),
            ('PR', 40, 180, False, (40, 80, 120, 160), (45, 140), True),
            ('SkinTemp', 26, 40, False, (28, 32, 36, 40), (30, 37), True),
            ('ACCEL', 0, 1.6, False, (0, 0.5, 1, 1.5), (0.8, 1.5), True),
            ('MET', -0.5, 9, False, (0, 2, 4, 6, 8), (0.9, 8), False),
            ('ACT_COUNT', 0, 3000, False, (0, 1000, 2000, 3000), (0, 3000), False)]
    w, rh = 6.2, 0.86
    out = []
    for i, (key, lo, hi, logx, ticks, (h0, h1), differs) in enumerate(rows):
        y = -i * rh
        if logx:
            pos = lambda v: w * (math.log10(max(v, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
        else:
            pos = lambda v: w * (min(max(v, lo), hi) - lo) / (hi - lo)
        mn, p1, p50, p99, mx = (percentile(vals[key], q) for q in (0, 1, 50, 99, 100))
        col = 'saffron' if differs else 'iris'
        out.append(f'\\fill[haze,draw=rule,line width=.3pt] ({pos(h0):.3f},{y - 0.17:.3f}) rectangle ({pos(h1):.3f},{y + 0.17:.3f});')
        out.append(f'\\draw[{col},line width=.5pt] ({pos(mn):.3f},{y:.3f}) -- ({pos(mx):.3f},{y:.3f});')
        for v in (mn, mx):
            out.append(f'\\draw[{col},line width=.5pt] ({pos(v):.3f},{y - 0.07:.3f}) -- ({pos(v):.3f},{y + 0.07:.3f});')
        out.append(f'\\fill[{col}] ({pos(p1):.3f},{y - 0.07:.3f}) rectangle ({pos(p99):.3f},{y + 0.07:.3f});')
        out.append(f'\\filldraw[fill=white,draw={col},line width=.5pt] ({pos(p50):.3f},{y:.3f}) circle (.6mm);')
        out.append(f'\\draw[rule,line width=.3pt] (0,{y - 0.22:.3f}) -- ({w:.3f},{y - 0.22:.3f});')
        for t in ticks:
            out.append(f'\\node[anchor=north,font=\\fontsize{{4.5}}{{5}}\\selectfont,text=muted,inner sep=1pt] at ({pos(t):.3f},{y - 0.22:.3f}) {{{t:g}}};')
    print('channel_ranges readings:', {k: len(v) for k, v in vals.items()})
    write('channel_ranges', out)


def contexts():
    # The ranges doc's 12 sample summaries: start -> end of the window per channel, coloured by the summary's own verb
    text = (HERE / 'ref' / 'physio_ranges.txt').read_text().replace('–', '-')
    blocks = re.findall(r'^\s*(\d+)\. ([^\n]+)\n.*?Stress score: (\d).*?EDA (\w+(?: \w+)?), from ([\d.]+) to ([\d.]+).*?'
                        r'PR (\w+(?: \w+)?), from ([\d.]+) to ([\d.]+).*?ACCEL (\w+(?: \w+)?), from ([\d.]+) to ([\d.]+).*?'
                        r'SkinTemp (\w+(?: \w+)?), ([\d.]+) -> ([\d.]+) degC \| MET: (\d+\.\d+) -> (\d+\.\d+)', text, re.M | re.S)
    assert len(blocks) == 12, len(blocks)
    scenarios = []
    for b in blocks:
        name = re.sub(r'\s*\(.*\)$', '', b[1]).replace(' or ', '/')
        name = {'Calming after a supportive reply, seated': 'Calming after support, seated',
                'Low-arousal grief, withdrawn and flat': 'Grief, withdrawn and flat',
                'Lying in bed at night, ruminating': 'In bed at night, ruminating'}.get(name, name)
        met0, met1 = float(b[15]), float(b[16])
        # MET carries no verb in the summary; a change of 0.1 or less reads as flat
        met = 'flat' if abs(met1 - met0) <= 0.1 else ('rose' if met1 > met0 else 'eased')
        scenarios.append((name, int(b[2]), [b[3:6], b[6:9], b[12:15], b[9:12], (met, b[15], b[16])]))
    heads = ['EDA, $\\mu$S', 'PR, bpm', 'Skin temp, $^\\circ$C', 'ACCEL, g', 'MET']
    digits = [2, 0, 1, 2, 2]
    namew, scorew, cellw, slope, rh, ch = 4.4, 0.9, 2.5, 0.75, 0.43, 0.26
    score_fill = {0: 'iris!25', 1: 'iris!25', 2: 'iris!55', 3: 'iris!55', 4: 'iris', 5: 'iris', 6: 'saffron'}
    out = [f'\\node[anchor=south,font=\\tiny\\bfseries,text=muted] at ({namew + scorew / 2:.3f},0.25) {{score}};']
    for j, h in enumerate(heads):
        out.append(f'\\node[anchor=south west,font=\\tiny\\bfseries,text=muted,inner sep=0] at ({namew + scorew + j * cellw:.3f},0.3) {{{h}}};')
    for j in range(5):
        allv = [float(v) for s in scenarios for v in s[2][j][1:]]
        lo, hi = min(allv), max(allv)
        x0 = namew + scorew + j * cellw
        for i, (name, score, cells) in enumerate(scenarios):
            verb, a, b = cells[j]
            yc = -i * rh
            ya, yb = (yc - ch / 2 + ch * (float(v) - lo) / (hi - lo) for v in (a, b))
            if verb.startswith('rose'):
                out.append(f'\\draw[saffron,line width=.9pt,-{{Stealth[length=1.3mm]}}] ({x0:.3f},{ya:.3f}) -- ({x0 + slope:.3f},{yb:.3f});')
            elif verb.startswith('eased'):
                out.append(f'\\draw[iris,line width=.9pt,-{{Stealth[length=1.3mm]}}] ({x0:.3f},{ya:.3f}) -- ({x0 + slope:.3f},{yb:.3f});')
            else:
                out.append(f'\\draw[rule,line width=.9pt] ({x0:.3f},{ya:.3f}) -- ({x0 + slope:.3f},{yb:.3f});')
                out.append(f'\\fill[muted] ({x0 + slope:.3f},{yb:.3f}) circle (.45mm);')
            fa, fb = (f'{float(v):.{digits[j]}f}' for v in (a, b))
            out.append(f'\\node[anchor=west,font=\\fontsize{{5}}{{6}}\\selectfont,text=muted,inner sep=0] at ({x0 + slope + 0.12:.3f},{yc:.3f}) {{{fa} $\\to$ {fb}}};')
    for i, (name, score, _) in enumerate(scenarios):
        yc = -i * rh
        out.append(f'\\node[anchor=west,font=\\scriptsize,inner sep=0] at (0,{yc:.3f}) {{{i + 1}. {name}}};')
        out.append(f'\\fill[{score_fill[score]}] ({namew + scorew / 2 - 0.17:.3f},{yc - 0.15:.3f}) rectangle ({namew + scorew / 2 + 0.17:.3f},{yc + 0.15:.3f});')
        out.append(f'\\node[font=\\tiny\\bfseries,text=white] at ({namew + scorew / 2:.3f},{yc:.3f}) {{{score}}};')
        if i:
            out.append(f'\\draw[rule,line width=.2pt] (0,{yc + rh / 2:.3f}) -- ({namew + scorew + 5 * cellw - 0.3:.3f},{yc + rh / 2:.3f});')
    write('contexts', out)


val_loss()
strategy_f1()
lr_sweep()
score_bars()
sources()
split_table()
conversation_lengths()
physio_ranges()
channel_ranges()
contexts()
print('wrote', sorted(p.name for p in OUT.glob('*.tex')))
