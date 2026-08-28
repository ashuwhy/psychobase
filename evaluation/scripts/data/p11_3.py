"""Participant 11_3. Model outputs for steps 2-4."""

LABEL = "Participant 11_3"
SOURCE = "output_participantGrouped11_3data_full_data.json"

NOTES = [
    "Every summary opens with the Physiological Signals line; what varies turn to turn is the "
    "order of the channels inside it and the wording, not the position of the opening line.",
    "Summaries are held to 3-4 lines.",
    "The physiological summary is hidden from the user, so no response quotes a value, a unit or "
    "a channel name. Grounding is carried qualitatively, in the register of the worked examples "
    "in the master prompt.",
    "Arousal in this session is lower and steadier than in 11_1 or 11_2 - EDA runs 2.98 to 4.83 "
    "uS and drifts down over the hour while SkinTemp rises 32.23 to 34.29 degC. There is no "
    "dramatic window, so the responses ground themselves in what is actually there: which "
    "channels move, which stay flat, and whether the movement counts explain them.",
    "Turns 6 and 9 carry a stress score of -2 with no stress_level. The value is reported exactly "
    "as recorded rather than clipped to 0, per the no-fabrication rule.",
    "Turn 1 is the one clear disagreement: the stress score reads 5 (Moderate) while pulse, "
    "conductance and movement are all falling. The response follows his words and treats the "
    "strain as the thing that needs explaining, rather than telling him he is calm.",
]

PHYSIO_SHORT = {
1: "Physiological Signals: The opening minute has conductance flat while pulse falls eleven beats and motion collapses from 0.099 g, temperature edging up, with still activity and the count sliding 90.0 to 16.0 - a body coming to rest even as the stress score reads moderate.\nStress score: 5 (Moderate stress). PR: 101.0 -> 90.0 bpm, decreasing, first minute.\nACCEL: 0.099 -> 0.013 g, decreasing, first minute.\nEDA: 4.13 -> 4.24 uS, flat, first minute.<EOS>",
2: "Physiological Signals: Conductance slips a little while pulse holds, temperature keeps rising and motion falls further, the class staying still with the count down at 9.0 - the level that remains is not activity-related.\nEDA: 4.51 -> 4.16 uS, decreasing, past 2 minutes. ACCEL: 0.028 -> 0.014 g, decreasing, past 2 minutes.\nPR: 89.0 -> 88.0 bpm, flat, past 2 minutes.\nStress score: 3 (Mild stress).<EOS>",
3: "Physiological Signals: Across five minutes conductance drifts up while pulse eases and temperature climbs, with motion spiking mid-window as the count jumps to 101.0 before settling to 30.0 - that burst of movement carried no arousal with it.\nACCEL: 0.024 -> 0.012 g, decreasing with a mid-window peak at 0.037, these 5 minutes.\nStress score: 2 (Mild stress). EDA: 4.08 -> 4.38 uS, increasing, these 5 minutes.\nPR: 92.0 -> 89.0 bpm, decreasing, these 5 minutes.<EOS>",
4: "Physiological Signals: Pulse lifts and motion doubles off a very low base while conductance holds and temperature rises, still turning generic as the count goes 33.0 to 44.0 - part of the cardiac change is simply the movement.\nPR: 89.0 -> 94.0 bpm, increasing, this 6-minute window. EDA: 4.0 -> 4.06 uS, flat, this 6-minute window.\nACCEL: 0.01 -> 0.02 g, increasing, this 6-minute window.\nStress score: 2 (Mild stress).<EOS>",
5: "Physiological Signals: Conductance falls steadily even as motion rises and the count climbs 36.0 to 56.0 under generic activity, temperature near its session high - arousal easing while movement increases.\nStress score: 2 (Mild stress). ACCEL: 0.046 -> 0.069 g, increasing, over the last 6 minutes.\nEDA: 3.96 -> 3.28 uS, decreasing, over the last 6 minutes.\nPR: 88.0 -> 91.0 bpm, increasing, over the last 6 minutes.<EOS>",
6: "Physiological Signals: Conductance lifts late in the window while pulse drops eight beats and motion doubles, temperature flat, with generic activity and the count rising 46.0 to 94.0 accounting for most of what moved.\nEDA: 2.98 -> 3.53 uS, increasing, this 6-minute stretch.\nPR: 91.0 -> 83.0 bpm, decreasing, this 6-minute stretch. ACCEL: 0.032 -> 0.065 g, increasing, this 6-minute stretch.\nStress score: -2 (qualitative label not reported).<EOS>",
7: "Physiological Signals: Both conductance and pulse come down while motion sits at the floor and temperature rises, generic giving way to still as the count eases 34.0 to 25.0 - settling rather than distress.\nPR: 89.0 -> 80.0 bpm, decreasing, during these 6 minutes. Stress score: 2 (Mild stress).\nACCEL: 0.011 -> 0.01 g, flat, during these 6 minutes.\nEDA: 4.83 -> 4.42 uS, decreasing, during these 6 minutes.<EOS>",
8: "Physiological Signals: Conductance edges up as pulse drops eleven beats and motion increases, temperature at its session peak, with generic activity and the count climbing 63.0 to 85.0 placing the small rise alongside more movement.\nACCEL: 0.039 -> 0.047 g, increasing, preceding 6 minutes.\nEDA: 3.67 -> 4.02 uS, increasing, preceding 6 minutes. Stress score: 2 (Mild stress).\nPR: 91.0 -> 80.0 bpm, decreasing, preceding 6 minutes.<EOS>",
9: "Physiological Signals: Motion climbs sharply late in the window as the count runs 37.0 to 98.0 and still turns generic, while conductance and pulse both ease - largely an activity-driven change.\nStress score: -2 (qualitative label not reported). ACCEL: 0.03 -> 0.076 g, increasing, in this 6-minute span.\nEDA: 4.31 -> 3.97 uS, decreasing, in this 6-minute span.\nPR: 94.0 -> 89.0 bpm, decreasing, in this 6-minute span.<EOS>",
10: "Physiological Signals: Pulse rises into the low hundreds and motion increases while conductance eases and temperature holds, generic activity with the count easing 135.0 to 101.0 - a settling body, so the cardiac lift is not fully explained by movement.\nPR: 93.0 -> 101.0 bpm, increasing, through the past 6 minutes.\nEDA: 3.55 -> 3.38 uS, decreasing, through the past 6 minutes. ACCEL: 0.052 -> 0.072 g, increasing, through the past 6 minutes.\nStress score: 0 (qualitative label not reported).<EOS>",
11: "Physiological Signals: The closing window offers only single aggregated values so each channel reads flat, with generic activity and a moderate count of 55.0 showing nothing shifting markedly either way.\nEDA: steady near 3.75 uS, flat, final 6 minutes. Stress score: 2 (Mild stress).\nACCEL: steady near 0.031 g, flat, final 6 minutes.\nPR: steady near 94.0 bpm, flat, final 6 minutes.<EOS>",
}

NEW_RESPONSE = {
1: ("Emotional Validation",
    "That's a quietly painful thing to notice about someone you care for - that you seem to matter most when there's a gap to fill. Wondering where you actually stand in someone's life is exhausting, and it isn't a petty thing to want an answer to. Your body has been settling this last minute, with your movement dropping right off, yet there are still clear signs of strain sitting underneath it. Something is staying switched on while the rest of you winds down."),
2: ("Clarification",
    "So the pattern has a shape to it: something goes wrong for them, and you're who they turn to. That would deepen anyone's attachment, because being trusted in someone's worst moments feels like closeness. The tension has eased slightly as you've explained it, though it's still holding at a level your stillness doesn't account for - you've barely moved in the last couple of minutes. What are those calls usually like for you afterwards?"),
3: ("Empathetic Statements",
    "And then the calls stop when things are good, which is the part that really stings. Being needed in the bad times and unnecessary in the good ones tells you something about the shape of the connection, even if nobody has said it out loud. I notice the tension drifted up while you told me that, and it wasn't the moving about - your movement rose in the middle of that stretch and came back down without the tension following it. The words did that, not the walking."),
4: ("Affirmation",
    "Not wanting someone to feel alone is a genuinely good instinct, and it says something real about you. I'd only gently note that the same instinct currently runs in one direction. There's a small lift in your signals as you said it, though that mostly tracks you starting to move again rather than the sentiment itself. Being kind doesn't have to mean being permanently available - the care still counts if it has limits."),
5: ("Provide Different Perspectives",
    "Being told you're the only one who understands them is a powerful thing to hear, and I understand why it stays with you. Another way to read it is that it describes what you provide, rather than what they intend to offer back. Interestingly, the tension has been falling steadily while you described it, even though you've been moving more - that phrase seems to soothe you. Which is exactly why it's worth holding it and the reality apart: both can be true at once."),
6: ("Reframe Negative Thoughts",
    "It's easy to read that as proof of something special, and in a sense it is - but I'd be careful about what it proves. Telling you what they don't tell their partner says a lot about where they feel safe, and very little about what they plan to do. Your body actually settled over these minutes even as you moved about more, so nothing here is alarming you physically; the difficulty is in what the fact means, not in how it feels to say. Being someone's safest place is real closeness - it just isn't the same as being chosen."),
7: ("Clarification",
    "That's a fair question to sit with, and I don't think you're being cynical for asking it. Your signals have come down as you've said it, with the tension easing and almost no movement behind the change, so this reads as something you've turned over for a while rather than a fresh wound. The way to an answer is usually the pattern rather than any single conversation. Over the last few months, how often have they reached out when nothing was wrong?"),
8: ("Reflective Statements",
    "So the flow is almost entirely one way - you hold their difficulties, and yours stay unspoken. That imbalance is easy to miss while it's happening, because each individual conversation feels normal; it's only when you add them up that the shape shows. Your body eased noticeably while you described it, even with your movement picking up. You've made peace with the arrangement more than you've questioned it, and that's part of what keeps it in place."),
9: ("Emotional Validation",
    "That fear is understandable, and it's telling in itself. If you're worried they'd leave once you stopped being useful, some part of you has already read the balance of this relationship. Being scared of that isn't weakness - it's you noticing something painful to notice. Your signals eased while you said it, with the moving about explaining what did change, so this seems like a settled belief you've held for a while rather than a passing worry. You deserve to be kept around for who you are, not for what you absorb."),
10: ("Normalize Experiences",
    "A lot of people find themselves in exactly this role, and they describe it the way you just did: less like a friend, more like a support function. It tends to happen gradually to whoever is best at listening, so it isn't a sign you did something wrong. One thing I notice is that your signals have lifted while your movement has actually come down - so that isn't the walking. Naming this out loud is doing something to you, which usually means it's close to the truth."),
11: ("Share Information",
    "There's a fairly reliable test, and it's worth applying honestly. Watch four things over the next month: who starts the conversation when nothing is wrong; whether they ask about your life without you raising it; whether they stay once they feel better; and whether they remember what you told them last time. If the answer to most is no, that's your answer - not because they're a bad person, but because it tells you what this will reliably give you. Your readings are completely level as we finish, everything flat, which is a good state to be in for deciding something rather than reacting to it."),
}

SCORES = {
1:  {"orig": [4, 3, 5, 1, 5, 5], "new": [5, 4, 5, 5, 5, 5]},
2:  {"orig": [4, 3, 4, 1, 5, 5], "new": [4, 4, 5, 4, 5, 5]},
3:  {"orig": [5, 3, 5, 1, 5, 5], "new": [5, 5, 5, 5, 5, 5]},
4:  {"orig": [4, 3, 5, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
5:  {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 5, 5, 5]},
6:  {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 4, 5, 5]},
7:  {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 5, 5, 5]},
8:  {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 5, 5, 5, 5, 5]},
9:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 5, 5, 5]},
10: {"orig": [4, 4, 5, 1, 5, 5], "new": [4, 4, 5, 5, 5, 5]},
11: {"orig": [4, 5, 4, 1, 5, 5], "new": [4, 5, 5, 4, 5, 5]},
}
