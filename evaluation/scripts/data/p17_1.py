"""Participant 17_1. Model outputs for steps 2-4."""

LABEL = "Participant 17_1"
SOURCE = "output_participantGrouped17_1data_full_data.json"

NOTES = [
    "Summary wording and line order are varied turn to turn rather than following one template.",
    "This session runs while the user is still on the bus, so unlike participant 17 the whole "
    "conversation is a current situation and physiology applies throughout. The catch is that "
    "ACCEL and ACT_COUNT partly register the vehicle rather than the person, which is why "
    "movement is treated as weak evidence here and PR carries more of the reading.",
    "EDA is absent on turns 1 and 3 and otherwise sits between 0.0 and 0.02 uS, at the sensor "
    "floor. Missing windows are reported as not reported; the near-zero values are stated but not "
    "given emotional weight.",
    "Turn 17 is the clearest calm-words-aroused-body window in the whole set: he describes a "
    "pleasant moment with a child, while the stress score reads 6 (High) with PR at 107.0 bpm and "
    "an activity count of 1.0. The response follows the master prompt's branch for that case and "
    "names the gap gently without contradicting what he said.",
    "PR reaches 120-140 bpm on turn 11 and stays in the 100s for most of the session - high for "
    "someone sitting on a bus, and not accounted for by the falling movement counts.",
]

PHYSIO_SHORT = {
1: "Physiological Signals: The opening minute carries only single aggregated values, with pulse at 100.0 bpm and motion at 0.099 g under generic activity and a high count of 139.0; the bus itself contributes to that movement, so little can be separated out.\nEDA: not reported for this window.\nPR: steady near 100.0 bpm, flat, first minute.\nACCEL: steady near 0.099 g, flat, first minute.\nStress score: 0 (qualitative label not reported).<EOS>",
2: "PR: 91.0 -> 100.0 bpm, increasing, past 1 minute.\nEDA: steady near 0.0 uS, flat, past 1 minute.\nACCEL: 0.084 -> 0.027 g, decreasing, past 1 minute.\nStress score: 2 (Mild stress).\nPhysiological Signals: Pulse climbs nine beats while motion drops sharply and the count falls 108.0 to 31.0 under generic activity; with temperature rising and conductance at zero, that rise is not coming from movement.<EOS>",
3: "Stress score: 2 (Mild stress).\nPhysiological Signals: Three minutes of single aggregated readings - pulse at 98.0 bpm, motion at 0.042 g, temperature still climbing - under generic activity with a moderate count of 46.0; conductance was not captured at all for this window.\nEDA: not reported for this window.\nACCEL: steady near 0.042 g, flat, these 3 minutes.\nPR: steady near 98.0 bpm, flat, these 3 minutes.<EOS>",
4: "Physiological Signals: Pulse pushes past 110 bpm while motion falls to a third of its opening value and the count eases 99.0 to 60.0; generic activity with conductance at zero means this cardiac climb has no movement behind it.\nPR: 111.0 -> 116.0 bpm, increasing, these 4 minutes.\nACCEL: 0.044 -> 0.016 g, decreasing, these 4 minutes.\nStress score: 2 (Mild stress).\nEDA: steady near 0.0 uS, flat, these 4 minutes.<EOS>",
5: "EDA: steady near 0.01 uS, flat, this 6-minute window.\nPR: steady near 104.0 bpm, flat, this 6-minute window.\nACCEL: steady near 0.029 g, flat, this 6-minute window.\nPhysiological Signals: Pulse holds in the low hundreds with conductance at the floor, temperature rising and motion light; generic gives way to still on a moderate count of 40.0, so the moderate stress score stands without a movement explanation.\nStress score: 4 (Moderate stress).<EOS>",
6: "Physiological Signals: Pulse eases slightly while motion increases and temperature keeps rising, conductance flat at the floor; generic activity with the count falling 82.0 to 60.0 leaves the moderate stress score unexplained by exertion.\nStress score: 4 (Moderate stress).\nACCEL: 0.025 -> 0.039 g, increasing, this 6-minute stretch.\nPR: 105.0 -> 103.0 bpm, decreasing, this 6-minute stretch.\nEDA: steady near 0.01 uS, flat, this 6-minute stretch.<EOS>",
7: "PR: 109.0 -> 105.0 bpm, decreasing, during these 6 minutes.\nACCEL: 0.041 -> 0.011 g, decreasing, during these 6 minutes.\nEDA: steady near 0.01 uS, flat, during these 6 minutes.\nStress score: 4 (Moderate stress).\nPhysiological Signals: Both pulse and motion come down as generic turns to walking and the count eases 59.0 to 48.0, temperature climbing throughout; pulse nonetheless stays above 100 bpm with almost no movement to justify it.<EOS>",
8: "Physiological Signals: Single aggregated values across this window, pulse at 102.0 bpm and motion at 0.033 g; still turns to walking on a moderate count of 72.0, with temperature at 34.43 degC and conductance at the floor.\nEDA: steady near 0.01 uS, flat, preceding 6 minutes.\nStress score: 2 (Mild stress).\nPR: steady near 102.0 bpm, flat, preceding 6 minutes.\nACCEL: steady near 0.033 g, flat, preceding 6 minutes.<EOS>",
9: "ACCEL: 0.024 -> 0.013 g, decreasing, in this 6-minute span.\nPR: steady near 109.0 bpm, flat, in this 6-minute span.\nEDA: steady near 0.01 uS, flat, in this 6-minute span.\nPhysiological Signals: Motion halves and the count collapses 86.0 to 18.0 while pulse holds near 109.0 bpm; with still becoming walking and temperature at its session high, the sustained pulse is not movement-driven.\nStress score: 3 (Mild stress).<EOS>",
10: "Stress score: 2 (Mild stress).\nPhysiological Signals: Motion drops to 0.009 g, the lowest of the session, as walking gives way to still on a count of 24.0, while pulse stays at 104.0 bpm and temperature peaks; conductance remains at the floor.\nPR: steady near 104.0 bpm, flat, through the past 6 minutes.\nEDA: steady near 0.01 uS, flat, through the past 6 minutes.\nACCEL: steady near 0.009 g, flat, through the past 6 minutes.<EOS>",
11: "Physiological Signals: Pulse reaches 140.0 bpm, by far the session high, while motion falls to a third and the count eases 109.0 to 79.0 as walking turns generic; with conductance at the floor and temperature flat, the movement counts do not account for a rise of this size.\nPR: 120.0 -> 140.0 bpm, increasing, over these 6 minutes.\nStress score: 2 (Mild stress).\nACCEL: 0.083 -> 0.025 g, decreasing, over these 6 minutes.\nEDA: steady near 0.01 uS, flat, over these 6 minutes.<EOS>",
12: "EDA: steady near 0.01 uS, flat, last 6 minutes.\nPR: steady near 118.0 bpm, flat, last 6 minutes.\nStress score: 2 (Mild stress).\nACCEL: steady near 0.046 g, flat, last 6 minutes.\nPhysiological Signals: Pulse stays very high at 118.0 bpm on a single aggregated reading while motion is modest and the count moderate at 72.0; walking turns generic and temperature begins to fall.<EOS>",
13: "Physiological Signals: Motion nearly triples and the count jumps 66.0 to 142.0 into the high band while pulse comes down seven beats; walking is sustained, temperature falls and conductance sits at the floor, so here the movement genuinely leads.\nACCEL: 0.033 -> 0.086 g, increasing, this six-minute window.\nPR: 114.0 -> 107.0 bpm, decreasing, this six-minute window.\nEDA: steady near 0.01 uS, flat, this six-minute window.\nStress score: 0 (qualitative label not reported).<EOS>",
14: "Stress score: 0 (qualitative label not reported).\nPR: 104.0 -> 100.0 bpm, decreasing, past 6 minutes.\nACCEL: 0.115 -> 0.046 g, decreasing, past 6 minutes.\nEDA: steady near 0.0 uS, flat, past 6 minutes.\nPhysiological Signals: Pulse and motion both ease even as the count climbs 110.0 to 134.0 and still turns to walking; temperature continues down and conductance is at zero, a mixed window where movement and pulse disagree.<EOS>",
15: "Physiological Signals: Pulse drops to 92.0 bpm, its lowest since the session opened, while motion holds moderate and the count sits at 120.0 under generic activity; conductance is at the floor and temperature keeps falling.\nEDA: steady near 0.01 uS, flat, these 6 minutes.\nACCEL: steady near 0.066 g, flat, these 6 minutes.\nStress score: 0 (qualitative label not reported).\nPR: steady near 92.0 bpm, flat, these 6 minutes.<EOS>",
16: "PR: 99.0 -> 109.0 bpm, increasing, six-minute window.\nACCEL: 0.051 -> 0.002 g, decreasing, six-minute window.\nEDA: steady near 0.01 uS, flat, six-minute window.\nStress score: 3 (Mild stress).\nPhysiological Signals: Motion falls essentially to zero and the count runs 83.0 down to 0.0 as generic turns to walking, yet pulse climbs ten beats; with temperature flat, that rise is happening without movement.<EOS>",
17: "Physiological Signals: The stress score peaks at its session maximum here while pulse sits at 107.0 bpm and the body is completely still - motion 0.002 g, count 1.0, class walking to still; conductance stays at the floor, so this arousal has no physical explanation at all.\nStress score: 6 (High stress).\nPR: steady near 107.0 bpm, flat, in these 6 minutes.\nEDA: steady near 0.02 uS, flat, in these 6 minutes.\nACCEL: steady near 0.002 g, flat, in these 6 minutes.<EOS>",
18: "EDA: steady near 0.02 uS, flat, over the preceding 6 minutes.\nPR: 111.0 -> 115.0 bpm, increasing, over the preceding 6 minutes.\nStress score: 5 (Moderate stress).\nACCEL: 0.021 -> 0.007 g, decreasing, over the preceding 6 minutes.\nPhysiological Signals: Pulse climbs into the mid-hundred-and-tens while motion falls and the count halves from 32.0 to 16.0; walking is sustained and temperature eases, so once again the cardiac rise runs against the movement.<EOS>",
19: "Stress score: 4 (Moderate stress).\nPhysiological Signals: Pulse holds at 108.0 bpm on a single reading with motion very low at 0.012 g and a count of 27.0, generic turning to walking; conductance is at the floor and temperature flat.\nACCEL: steady near 0.012 g, flat, during this window.\nEDA: steady near 0.02 uS, flat, during this window.\nPR: steady near 108.0 bpm, flat, during this window.<EOS>",
20: "Physiological Signals: The closing window keeps pulse elevated at 112.0 bpm with light motion and a moderate count of 62.0 under sustained walking; conductance remains at the floor and temperature is unchanged, so the moderate stress score is not a movement artefact.\nPR: steady near 112.0 bpm, flat, final 6 minutes.\nStress score: 4 (Moderate stress).\nEDA: steady near 0.02 uS, flat, final 6 minutes.\nACCEL: steady near 0.018 g, flat, final 6 minutes.<EOS>",
}

NEW_RESPONSE = {
1: ("Emotional Validation",
    "Long journeys have a way of stretching out, especially when you're not comfortable to begin with. Being partway through and already feeling like this is genuinely wearing. What's making today feel particularly long?"),
2: ("Clarification",
    "Ah - so it isn't only the travel, it's what you're travelling away from. Going back after a few days at home is its own adjustment, and the two things pile onto each other. Which part is sitting heavier at the moment: the leaving, or the journey itself?"),
3: ("Reflective Statements",
    "So you boarded already low, which means the bus has been adding to something rather than starting it. When you begin a journey like that, every ordinary discomfort lands harder than it would on a good day. That's a long way to travel carrying both."),
4: ("Empathetic Statements",
    "Nine or ten hours is a genuinely long stretch to be confined to one seat. There's no way to make that pass comfortably, and knowing how much is left is its own weight. Your pulse is running higher than I'd expect for someone sitting still on a bus, which fits how unsettled this feels."),
5: ("Clarification",
    "An early departure on top of the length makes it a much longer day than the timetable suggests. Were you able to get any real sleep before you left?"),
6: ("Normalize Experiences",
    "That combination catches most people out. If mornings are hard for you anyway and the sleep didn't come, you started this journey with nothing in reserve - and everything since has had to come out of an empty tank. Feeling worn out this early isn't you being delicate, it's arithmetic."),
7: ("Reframe Negative Thoughts",
    "I'd be careful about counting that as a failure on your part. A moving bus with no space isn't a place where research happens - the environment made the decision, not your discipline. Not working in conditions that make work impossible is not the same as wasting the time."),
8: ("Reflective Statements",
    "So the fallback had a limit too. Rationing a battery means you never quite relax into using the phone and never quite put it away, which keeps a low hum of calculation running for hours."),
9: ("Normalize Experiences",
    "It's funny how quickly the absence of that small habit becomes noticeable - and everyone who travels knows this exact frustration. A few reels can swallow an hour without you noticing; without them, every hour announces itself. Completely ordinary, and completely draining."),
10: ("Clarification",
    "Trying to sleep and failing might be the most tiring option of the three. Was it the noise keeping you awake, or just not being able to get comfortable?"),
11: ("Reflective Statements",
    "That explains a great deal. A seat by the door means every stop reaches you - the noise, the movement, the air - so you were never given a long enough stretch to actually drop off. You weren't failing to sleep; you were being interrupted."),
12: ("Empathetic Statements",
    "Being pulled back from the edge of sleep over and over is genuinely exhausting, more so than not sleeping at all. Your body keeps starting the process and never gets to finish it. After several hours of that, of course you're depleted. I can see your pulse is still running high, which is what that kind of broken rest tends to leave behind."),
13: ("Clarification",
    "A quieter bus should have helped, at least. Did having fewer people around make any real difference to how the journey felt?"),
14: ("Provide Different Perspectives",
    "That's a detail I wouldn't have thought of, and it reframes the whole thing. An emptier bus doesn't help if you're in the front row where the turnover is highest - your personal space kept resetting even though the overall crowd was thin. So it wasn't quieter for you in the way it looked from outside."),
15: ("Reflective Statements",
    "Never settled - that's the thread running through all of it. No single disaster, just a long series of small interruptions that never let you arrive anywhere mentally. That accumulation is what wears people down on journeys like this."),
16: ("Clarification",
    "I'm glad something good came out of the day. What happened?"),
17: ("Affirmation",
    "That's a lovely thing to have noticed and held onto in the middle of a difficult journey. Children have a way of changing the atmosphere without trying, and the fact that you let yourself enjoy it says something about you. I will gently mention one thing: your readings are showing quite a lot of arousal right now even though you're sitting completely still, more than the nice part of this suggests. Both can be true - the moment was genuinely good, and your body is still carrying the rest of the day."),
18: ("Emotional Validation",
    "A cheerful child is hard to stay glum around, and a break from your own thoughts was probably exactly what you needed at that point. Those small unexpected moments do real work on a long day. Your pulse is still running high underneath it, so I don't think the lift undid the tiredness - it just gave you a rest from it for a while."),
19: ("Empathetic Statements",
    "And then he was gone, and the quiet came back louder than before. That's the difficult part of a moment like that - it lifts you, and the drop afterwards is steeper for having felt better briefly. Being lonely on a crowded bus is a particular kind of lonely."),
20: ("Offer Hope",
    "That's completely fair, and you're nearly through it. You've been awake since before dawn on almost no sleep, spent hours unable to work, rest, or settle, and carried the goodbye the whole way - wanting it to end is the only sensible response. It does end today. Your readings show you're still running hot, so when you get in, don't ask anything more of yourself than food and sleep."),
}

SCORES = {
1:  {"orig": [3, 3, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
2:  {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
3:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
4:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
5:  {"orig": [3, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
6:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
7:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
8:  {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
9:  {"orig": [3, 3, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
10: {"orig": [3, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
11: {"orig": [4, 5, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
12: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
13: {"orig": [3, 3, 4, 1, 5, 5], "new": [3, 4, 5, 1, 5, 5]},
14: {"orig": [4, 5, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
15: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
16: {"orig": [3, 3, 4, 1, 5, 5], "new": [3, 3, 5, 1, 5, 5]},
17: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 5, 5, 5, 5, 5]},
18: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
19: {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
20: {"orig": [5, 5, 4, 1, 5, 5], "new": [5, 5, 5, 4, 5, 5]},
}
