"""Participant 14. Model outputs for steps 2-4."""

LABEL = "Participant 14"
SOURCE = "output_participantGrouped14data_full_data.json"

NOTES = [
    "Summary wording and line order are varied turn to turn rather than following one template.",
    "The fire happened the day before this session, so turns 1 to 9 are a past memory. The master "
    "prompt says to use physiology only for current situations and ignore it for past events, so "
    "those responses answer the emotional meaning of the recollection. Turn 3 uses the "
    "recalling-a-past-experience wording, which is the one physiological reference the prompt "
    "permits in that mode.",
    "Turns 10 and 11 shift to the present (going to work that morning, unable to concentrate), so "
    "physiology comes back into play. Turn 10 is the useful window: EDA rises 3.6 -> 4.13 uS "
    "while activity count falls from 48.0 to 25.0.",
    "PR sits between 91 and 107 bpm for the whole session against walking or generic activity, so "
    "it is treated as activity-related rather than read as distress.",
    "Turn 1 was re-generated after the first evaluation pass flagged it as thin; the improved "
    "version opens the conversation properly rather than only granting permission to speak.",
]

PHYSIO_SHORT = {
1: "EDA: 3.27 -> 3.93 uS, increasing, first minute.\nPR: 102.0 -> 98.0 bpm, decreasing, first minute.\nACCEL: 0.025 -> 0.036 g, increasing, first minute.\nStress score: 4 (Moderate stress).\nPhysiological Signals: Conductance rises then levels off while pulse eases and temperature and motion stay put; walking throughout with counts around 30.0 to 67.0 makes the overall picture broadly activity-related.<EOS>",
2: "Physiological Signals: Conductance jumps late in this two-minute window while pulse drops six beats and motion eases, temperature ticking up; the class turns walking to generic with the count down at 41.0, so that conductance rise is not movement.\nStress score: 4 (Moderate stress).\nPR: 100.0 -> 94.0 bpm, decreasing, past 2 minutes.\nEDA: 3.6 -> 4.39 uS, increasing, past 2 minutes.\nACCEL: 0.043 -> 0.028 g, decreasing, past 2 minutes.<EOS>",
3: "Stress score: 2 (Mild stress).\nEDA: 3.7 -> 3.2 uS, decreasing, these 5 minutes.\nPR: 107.0 -> 104.0 bpm, decreasing, these 5 minutes.\nACCEL: 0.037 -> 0.033 g, flat, these 5 minutes.\nPhysiological Signals: Five minutes of steady readings - conductance declining, pulse parked near 100 bpm, temperature drifting up and motion unchanged; walking activity with counts in the 30s and 40s gives a settled rather than a reactive picture.<EOS>",
4: "Physiological Signals: Conductance and motion both ease while pulse comes down and temperature edges up; generic turns to walking as the count climbs 43.0 to 75.0, so arousal is falling even while movement increases.\nACCEL: 0.054 -> 0.031 g, decreasing, this 6-minute window.\nEDA: 3.02 -> 2.93 uS, decreasing, this 6-minute window.\nStress score: 2 (Mild stress).\nPR: 102.0 -> 99.0 bpm, decreasing, this 6-minute window.<EOS>",
5: "PR: 102.0 -> 100.0 bpm, flat, over the last 6 minutes.\nEDA: 2.73 -> 2.59 uS, decreasing, over the last 6 minutes.\nACCEL: 0.036 -> 0.032 g, flat, over the last 6 minutes.\nStress score: 2 (Mild stress).\nPhysiological Signals: The slow conductance decline continues with pulse holding near 100 bpm and temperature at its session high; sustained walking and counts around 35.0 to 79.0 mean nothing here separates from ordinary activity.<EOS>",
6: "Physiological Signals: Motion doubles and the count peaks at 110.0 before falling back to 72.0 as walking gives way to generic, while conductance holds flat and temperature is steady; the mid-window pulse bump tracks that movement.\nEDA: 2.62 -> 2.61 uS, flat, this 6-minute stretch.\nStress score: 2 (Mild stress).\nACCEL: 0.032 -> 0.064 g, increasing, this 6-minute stretch.\nPR: 100.0 -> 102.0 bpm, flat with a mid-window peak at 107.0, this 6-minute stretch.<EOS>",
7: "ACCEL: 0.03 -> 0.093 g, increasing, during these 6 minutes.\nEDA: 2.76 -> 2.9 uS, increasing, during these 6 minutes.\nPR: 97.0 -> 99.0 bpm, flat, during these 6 minutes.\nPhysiological Signals: Motion triples and conductance creeps up while pulse holds and temperature eases; walking is sustained and the count doubles to 64.0, so a good share of the rise is activity.\nStress score: 4 (Moderate stress).<EOS>",
8: "Stress score: 2 (Mild stress).\nPhysiological Signals: Motion keeps climbing and conductance edges up while pulse eases and temperature falls; generic activity with the count moving 76.0 to 96.0 makes this largely a movement story.\nPR: 101.0 -> 98.0 bpm, decreasing, preceding 6 minutes.\nACCEL: 0.09 -> 0.123 g, increasing, preceding 6 minutes.\nEDA: 2.95 -> 3.04 uS, increasing, preceding 6 minutes.<EOS>",
9: "Physiological Signals: Conductance continues upward while pulse eases, motion stays high and temperature drops; walking turns generic and the count runs 54.0 to 114.0, which accounts for most of what is visible here.\nEDA: 3.15 -> 3.43 uS, increasing, in this 6-minute span.\nACCEL: 0.073 -> 0.07 g, flat, in this 6-minute span.\nPR: 102.0 -> 99.0 bpm, decreasing, in this 6-minute span.\nStress score: 2 (Mild stress).<EOS>",
10: "EDA: 4.02 -> 3.94 uS, flat with a mid-window peak at 4.13, through the past 6 minutes.\nPR: 98.0 -> 94.0 bpm, decreasing, through the past 6 minutes.\nStress score: 4 (Moderate stress).\nACCEL: 0.035 -> 0.011 g, decreasing, through the past 6 minutes.\nPhysiological Signals: Conductance reaches its session high just as motion drops to almost nothing and pulse falls; generic activity with the count halving from 48.0 to 25.0 leaves this arousal without any movement explanation.<EOS>",
11: "Physiological Signals: Conductance and pulse both ease while motion stays low and temperature edges up; generic turns to walking on a low-to-moderate count of 33.0 to 37.0, so the raised stress score sits without a movement explanation behind it.\nStress score: 4 (Moderate stress).\nACCEL: 0.033 -> 0.024 g, decreasing, over these 6 minutes.\nPR: 98.0 -> 96.0 bpm, decreasing, over these 6 minutes.\nEDA: 3.6 -> 3.43 uS, decreasing, over these 6 minutes.<EOS>",
12: "PR: steady near 94.0 bpm, flat, final 6 minutes.\nEDA: steady near 3.37 uS, flat, final 6 minutes.\nACCEL: steady near 0.05 g, flat, final 6 minutes.\nPhysiological Signals: The closing window carries only single aggregated values, every channel flat including temperature; generic activity with a moderate count of 59.0 describes a settled state.\nStress score: 2 (Mild stress).<EOS>",
}

NEW_RESPONSE = {
1: ("Clarification",
    "Of course - I'd like to hear it. Something that stays with you overnight and is still there the next evening usually mattered more than people give it credit for. Start wherever it makes sense to you: what happened, and where were you when it did?"),
2: ("Emotional Validation",
    "A fire that close to home is genuinely frightening, and you don't have to have been inside it for that to shake you. Something like that changes how safe your own street feels for a while. I'm glad you're talking about it rather than sitting with it alone."),
3: ("Reflective Statements",
    "Only a few buildings away - so it was near enough that it could very easily have been your house. That proximity is often the part that lingers, more than the event itself. As you talk me through it, your physical state seems fairly steady, which suggests you've had a little time to absorb it since yesterday."),
4: ("Empathetic Statements",
    "Watching it spread with the whole neighbourhood standing outside must have been a tense, helpless kind of feeling. Everyone is there, and there is very little any one person can actually do. That image tends to stay with people for a while."),
5: ("Reframe Negative Thoughts",
    "Everyone getting out is genuinely the thing that matters most here, and it's worth letting that land before the rest. The belongings are a real loss and it's fair to grieve them - but possessions can be replaced over time in a way that people cannot. Holding both at once is the honest position: relieved about the family, and sorry for what they've lost."),
6: ("Emotional Validation",
    "Oh, that makes it much harder. They were in the middle of preparing for something joyful, and the timing of it feels almost unfair in a way that has nothing to do with logic. It's completely understandable that the engagement detail is the part that got to you."),
7: ("Empathetic Statements",
    "Seeing a mother cry like that is hard to shake off. You were watching someone in real distress with nothing you could do to fix it, and that helplessness stays with you longer than people expect. It says something kind about you that her grief affected you this much."),
8: ("Affirmation",
    "Staying there until the firefighters were done was a genuinely good thing to do, and not everyone does it. In a crisis, most people want to go back inside and close the door - you and your parents stayed. Presence like that often matters more to a family than anything practical anyone can offer."),
9: ("Reflective Statements",
    "One thirty in the morning, after all of that - so you gave up your whole night as well as your evening. That's a long stretch of being alert and worried, and the tiredness afterwards is physical as much as emotional. It makes sense if the next day felt heavy before it even started."),
10: ("Promote Self-Care Practices",
    "Going in after a night like that takes real effort, and it's no small thing that you managed it. I'd gently push you to protect some recovery now, though - an earlier night, a proper meal, and less on yourself this evening than you'd normally take on. I'm also noticing signs that you haven't fully come down from it yet, even while you've been sitting fairly still. Being tired and unsettled at the same time is worth resting for."),
11: ("Normalize Experiences",
    "That's a very common reaction, and it isn't a failure of concentration. After witnessing something distressing, the mind keeps returning to it for a few days while it processes - most people find their focus is patchy for a while afterwards. Your signals suggest you're still carrying some of that tension today. Expect a couple more days like this before it eases, and don't take it as a sign that something is wrong with you."),
12: ("Offer Hope",
    "I hope so too, and families do rebuild from this - usually more quickly than seems possible in the first week, because neighbours and relatives tend to close in around them. What you and your parents already did is part of exactly that. Keep an eye out for the practical moments where you can help, and let yourself believe this gets better for them."),
}

SCORES = {
1:  {"orig": [3, 3, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
2:  {"orig": [4, 3, 5, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
3:  {"orig": [4, 3, 4, 1, 5, 5], "new": [4, 4, 5, 4, 5, 5]},
4:  {"orig": [4, 3, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
5:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
6:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
7:  {"orig": [5, 3, 5, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
8:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
9:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
10: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 5, 5, 5]},
11: {"orig": [4, 3, 4, 1, 5, 5], "new": [4, 5, 5, 4, 5, 5]},
12: {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
}
