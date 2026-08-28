"""Participant 20. Model outputs for steps 2-4."""

LABEL = "Participant 20"
SOURCE = "output_participantGrouped20data_full_data.json"

NOTES = [
    "Summary wording and line order are varied turn to turn rather than following one template.",
    "This session is practical rather than confessional - an internship cutoff missed by 0.12 of "
    "a CGPA point and an exam the next day. The master prompt still applies, so the responses "
    "stay warm, but the user's words are the source of truth and he is asking for concrete help, "
    "which is what turns 7 to 9 give him.",
    "Turns 4 and 5 are the physiologically interesting pair: PR climbs 93 -> 100 -> 97 bpm while "
    "ACCEL falls to 0.005 g and the activity count drops from 40.0 to 8.0. That is arousal with "
    "the movement going the other way, and it lands exactly where he asks to be heard out and "
    "then reveals the CGPA drop.",
    "EDA is stable around 2.0-2.4 uS throughout with no meaningful excursion, so the reading rests "
    "on PR and the activity counts.",
    "Turn 8 is a correction from the user - the earlier plan assumed knowledge he does not have. "
    "The new response accepts that without defensiveness and replans, which is what lifts its "
    "strategy faithfulness score.",
]

PHYSIO_SHORT = {
1: "Physiological Signals: Pulse holds around 90 bpm through the opening minute while motion jumps late and the count runs 35.0 down to 5.0 and back to 53.0; walking throughout with conductance steady and temperature easing.\nEDA: steady near 2.35 uS, flat, first minute.\nPR: 91.0 -> 93.0 bpm, flat, first minute.\nACCEL: 0.014 -> 0.074 g, increasing, first minute.\nStress score: 2 (Mild stress).<EOS>",
2: "PR: 88.0 -> 87.0 bpm, flat with a mid-window peak at 94.0, past 3 minutes.\nEDA: 2.22 -> 2.24 uS, flat, past 3 minutes.\nACCEL: 0.018 -> 0.009 g, decreasing, past 3 minutes.\nStress score: 1 (qualitative label not reported).\nPhysiological Signals: A brief pulse bump in the middle of the window, otherwise steady, while motion falls and the count drops 34.0 to 14.0 as walking turns generic; temperature continues its slow decline.<EOS>",
3: "Stress score: 4 (Moderate stress).\nPhysiological Signals: Pulse climbs six beats while motion triples off a very low base and the count rises 8.0 to 40.0 under sustained walking; conductance is flat and temperature unchanged, so part of this is movement.\nEDA: 2.36 -> 2.37 uS, flat, these 6 minutes.\nACCEL: 0.005 -> 0.015 g, increasing, these 6 minutes.\nPR: 89.0 -> 95.0 bpm, increasing, these 6 minutes.<EOS>",
4: "Physiological Signals: Pulse reaches 100.0 bpm while motion falls and generic gives way to still, conductance easing and temperature flat; the count of 46.0 does not account for a pulse that high on a settling body.\nPR: 93.0 -> 100.0 bpm, increasing, this 6-minute window.\nStress score: 2 (Mild stress).\nEDA: 2.39 -> 2.16 uS, decreasing, this 6-minute window.\nACCEL: 0.025 -> 0.014 g, decreasing, this 6-minute window.<EOS>",
5: "PR: 94.0 -> 97.0 bpm, increasing, over the last 6 minutes.\nACCEL: 0.023 -> 0.005 g, decreasing, over the last 6 minutes.\nEDA: 2.12 -> 2.07 uS, flat, over the last 6 minutes.\nPhysiological Signals: Pulse keeps rising while motion drops to almost nothing and the count collapses 40.0 to 8.0 as walking turns still; with temperature flat, this arousal is clearly not explained by movement.\nStress score: 3 (Mild stress).<EOS>",
6: "Physiological Signals: Pulse comes down six beats and motion falls further to 0.003 g with the count at 5.0, still activity throughout; conductance edges up slightly and temperature declines, so the peak has passed.\nStress score: 1 (qualitative label not reported).\nACCEL: 0.01 -> 0.003 g, decreasing, this 6-minute stretch.\nEDA: 2.06 -> 2.17 uS, flat, this 6-minute stretch.\nPR: 95.0 -> 89.0 bpm, decreasing, this 6-minute stretch.<EOS>",
7: "EDA: 2.21 -> 2.27 uS, flat, during these 6 minutes.\nPR: 94.0 -> 90.0 bpm, decreasing, during these 6 minutes.\nStress score: 4 (Moderate stress).\nACCEL: 0.013 -> 0.014 g, flat with a mid-window peak at 0.02, during these 6 minutes.\nPhysiological Signals: The count spikes to 79.0 mid-window before settling back to 21.0 as still turns to walking, while pulse eases and conductance holds; temperature rises slightly and the moderate stress score sits above what the movement would explain.<EOS>",
8: "Physiological Signals: Four readings across this window show conductance drifting down and pulse hovering around 90 bpm, with motion low and the count steady near 21.0 under still activity; temperature continues to ease.\nStress score: 2 (Mild stress).\nEDA: 2.17 -> 2.02 uS, decreasing, preceding 6 minutes.\nACCEL: 0.01 -> 0.013 g, flat, preceding 6 minutes.\nPR: 89.0 -> 90.0 bpm, flat, preceding 6 minutes.<EOS>",
9: "PR: steady near 90.0 bpm, flat, final 6 minutes.\nEDA: steady near 2.0 uS, flat, final 6 minutes.\nACCEL: steady near 0.005 g, flat, final 6 minutes.\nStress score: 3 (Mild stress).\nPhysiological Signals: The closing window carries single aggregated values only, every channel flat, with still activity and a low count of 9.0; the mild stress score stands without any movement behind it.<EOS>",
}

NEW_RESPONSE = {
1: ("Clarification",
    "I'm good, thanks for asking. You've caught me at a good moment - what's going on with you today?"),
2: ("Affirmation",
    "That's a genuinely good position to be in, and worth being pleased about. A stipend above what you expected usually means the company is serious about the people they take. Do you know much about the role yet, or is it still early?"),
3: ("Reflective Statements",
    "Per month changes the picture entirely - that's a substantially better offer than it first sounded. No wonder this one has your attention."),
4: ("Clarification",
    "Understood - go ahead, I'm listening. Take it in whatever order you need to."),
5: ("Emotional Validation",
    "Oh, that's a brutal margin. Missing by 0.12 when you were above the line last semester is genuinely hard to sit with, because it's close enough to feel like it shouldn't count. I can see it in your signals too - your pulse has been climbing over the last few minutes even though you've gone still, which tells me this is landing harder than you're letting on. A cutoff is an administrative line, not a measure of what you can do. Is there any route through your placement cell, or is the portal the only door?"),
6: ("Offer Hope",
    "That's a frustrating way to be told no - a portal that won't even let you try. Worth holding onto two things, though: cutoffs like this are usually specific to the company rather than the industry, and plenty of strong offers don't carry a hard CGPA wall at all. One semester moved you 0.16; another can move you back. This closes one door on one day, and it doesn't decide the year."),
7: ("Collaborative Planning",
    "Then the exam is the thing that matters today, and we should give it the remaining hours rather than the CGPA. Before I suggest anything specific - how much ground do you already have under you in this subject, and what's the format tomorrow? Your readings suggest the stress is running a bit above where the movement would put it, so let's make the plan small and concrete rather than ambitious."),
8: ("Avoid Judgment and Criticism",
    "That's a fair correction, and my mistake for assuming - it changes the plan completely. If you're starting from zero today, the goal is not mastery, it's recognition: being able to look at a question tomorrow and know which shape it is, even if the code isn't perfect. That is genuinely achievable in an afternoon, and it's a different task from learning DSA properly, which takes months. Let's aim only at that."),
9: ("Share Information",
    "Here are the patterns worth knowing by tonight, with the tell for each one. Sliding window: the question mentions a contiguous subarray or substring with some constraint - longest, smallest, at most k. Two pointers: the array is sorted and you're asked for a pair or triplet summing to a target. Hash map counting: anything about frequency, duplicates, or 'has this appeared before'. Stack: 'next greater element', matching brackets, or anything where you need the most recent unresolved item. Binary search: sorted input and the phrase 'minimum possible' or 'maximum possible'. Learn to spot those five and you'll recognise most of what appears. Want me to walk through one worked example of each?"),
}

SCORES = {
1: {"orig": [3, 3, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
2: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
3: {"orig": [4, 3, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
4: {"orig": [3, 3, 5, 1, 5, 5], "new": [4, 3, 5, 1, 5, 5]},
5: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 5, 5, 5, 5, 5]},
6: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 5, 5, 1, 5, 5]},
7: {"orig": [3, 4, 3, 1, 5, 4], "new": [4, 5, 5, 4, 5, 5]},
8: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 5, 5, 1, 5, 5]},
9: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
}
