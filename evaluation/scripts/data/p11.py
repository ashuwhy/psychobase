"""Participant 11. Model outputs for steps 2-4."""

LABEL = "Participant 11"
SOURCE = "output_participantGrouped11data_full_data.json"

NOTES = [
    "Every summary opens with the Physiological Signals line; what varies turn to turn is the "
    "order of the channels inside it and the wording, not the position of the opening line.",
    "Summaries are held to 3-4 lines.",
    "The physiological summary is hidden from the user, so no response quotes a value, a unit or "
    "a channel name. Grounding is carried qualitatively, in the register of the worked examples "
    "in the master prompt.",
    "EDA climbs steadily from 0.77 to 11.6 uS across turns 1-11 and then falls back, while "
    "activity count drops to 11-18 over turns 7-10. That arousal is not explained by movement, "
    "so those turns take the branch where physiology agrees with the distress in the words.",
    "Turns 6, 7 and 11 recall the past (the earlier friendship, time spent together, the class "
    "representative role). The master prompt allows a recalling-a-past-experience reference in "
    "that mode, so those responses note whether he stays level or tenses as he revisits it.",
    "Turns 13 to 16 report a stress score of 0 with no stress_level while activity count rises to "
    "143-168. The summaries record the score as given and attribute the rise to movement.",
]

PHYSIO_SHORT = {
1: "Physiological Signals: Conductance more than doubles inside the opening minute while pulse drops steeply and both temperature and motion stay put, the class holding generic with counts easing 106.0 to 99.0 - movement does not account for it.\nEDA: 0.77 -> 2.09 uS, increasing, first minute.\nPR: 123.0 -> 94.0 bpm, decreasing, first minute. ACCEL: 0.032 -> 0.031 g, flat, first minute.\nStress score: 2 (Mild stress).<EOS>",
2: "Physiological Signals: Only coarse single-point readings exist for this minute so every channel reads flat, with generic activity and a count of 114.0 making what movement there is look ordinary.\nStress score: 2 (Mild stress). EDA: steady near 1.74 uS, flat, past 1 minute.\nACCEL: steady near 0.159 g, flat, past 1 minute.\nPR: steady near 100.0 bpm, flat, past 1 minute.<EOS>",
3: "Physiological Signals: Two minutes in, conductance sits far above where the session opened while pulse, temperature and motion stay level, activity generic and movement minimal - the elevation has no physical explanation.\nPR: steady near 94.0 bpm, flat, across these 2 minutes. Stress score: 4 (Moderate stress).\nEDA: steady near 2.94 uS, flat, across these 2 minutes.\nACCEL: steady near 0.032 g, flat, across these 2 minutes.<EOS>",
4: "Physiological Signals: Conductance keeps climbing while pulse settles and temperature slips, and the count actually falls 115.0 to 64.0 under a generic class - the arousal runs against the movement rather than with it.\nEDA: 4.01 -> 5.18 uS, increasing, through the last 4 minutes.\nACCEL: 0.025 -> 0.046 g, increasing, through the last 4 minutes. Stress score: 2 (Mild stress).\nPR: 95.0 -> 89.0 bpm, decreasing, through the last 4 minutes.<EOS>",
5: "Physiological Signals: Five minutes in, conductance has risen again while pulse, temperature and motion sit still, the class generic with the count down to 43.0 - this continued climb is not something movement explains.\nACCEL: steady near 0.016 g, flat, over these 5 minutes.\nStress score: 2 (Mild stress). EDA: steady near 6.3 uS, flat, over these 5 minutes.\nPR: steady near 89.0 bpm, flat, over these 5 minutes.<EOS>",
6: "Physiological Signals: Conductance is higher still across this stretch while pulse and motion hold and temperature barely shifts, the class moving generic to still with the count down at 31.0 - no part of this is activity-driven.\nEDA: steady near 7.45 uS, flat, this 6-minute stretch.\nPR: steady near 89.0 bpm, flat, this 6-minute stretch. ACCEL: steady near 0.018 g, flat, this 6-minute stretch.\nStress score: 2 (Mild stress).<EOS>",
7: "Physiological Signals: Conductance rises as pulse eases and temperature holds, with the class shifting generic to still and counts down at 18.0 then 16.0 - arousal arriving without any movement behind it.\nStress score: 5 (Moderate stress). PR: 95.0 -> 92.0 bpm, decreasing, during the past 6 minutes.\nEDA: 7.24 -> 7.79 uS, increasing, during the past 6 minutes.\nACCEL: 0.007 -> 0.012 g, increasing, during the past 6 minutes.<EOS>",
8: "Physiological Signals: A fresh conductance high for the session with pulse, temperature and motion all flat beneath it, the class gone generic to still on a count of 11.0 - no physical driver for the change.\nACCEL: steady near 0.006 g, flat, in the last 6 minutes. EDA: steady near 9.28 uS, flat, in the last 6 minutes.\nPR: steady near 92.0 bpm, flat, in the last 6 minutes.\nStress score: 5 (Moderate stress).<EOS>",
9: "Physiological Signals: Conductance has pushed past ten while pulse holds and temperature edges up, still activity on a count of 14.0 meaning nothing physical is producing this.\nStress score: 5 (Moderate stress).\nEDA: steady near 10.85 uS, flat, across this 6-minute window. ACCEL: steady near 0.007 g, flat, across this 6-minute window.\nPR: steady near 91.0 bpm, flat, across this 6-minute window.<EOS>",
10: "Physiological Signals: Conductance and temperature drift up together over these six minutes while pulse is unchanged and motion falls, the class staying still with the count near 34.0 - the elevation is not movement-related.\nPR: 92.0 -> 93.0 bpm, flat, over these 6 minutes.\nACCEL: 0.009 -> 0.007 g, decreasing, over these 6 minutes. Stress score: 4 (Moderate stress).\nEDA: 10.71 -> 10.97 uS, increasing, over these 6 minutes.<EOS>",
11: "Physiological Signals: The session peak for conductance, with pulse, temperature and motion all lifted alongside it as the class turns still to generic and the count returns to 99.0 - part of this rise is genuinely activity-related.\nEDA: steady near 11.6 uS, flat, last 6 minutes. Stress score: 2 (Mild stress).\nACCEL: steady near 0.096 g, flat, last 6 minutes.\nPR: steady near 101.0 bpm, flat, last 6 minutes.<EOS>",
12: "Physiological Signals: Conductance comes off its peak while pulse climbs and motion increases, the class moving still to generic on a high count of 142.0 - the cardiac rise is mostly the walking rather than the topic.\nACCEL: steady near 0.112 g, flat, six-minute window.\nEDA: steady near 9.93 uS, flat, six-minute window. Stress score: 2 (Mild stress).\nPR: steady near 109.0 bpm, flat, six-minute window.<EOS>",
13: "Physiological Signals: Every channel comes down together, temperature included, as the class runs still to generic and the count eases 143.0 to 114.0 - a body settling after movement.\nEDA: 9.36 -> 7.17 uS, decreasing, over the preceding 6 minutes.\nStress score: 0 (qualitative label not reported). ACCEL: 0.122 -> 0.045 g, decreasing, over the preceding 6 minutes.\nPR: 98.0 -> 96.0 bpm, decreasing, over the preceding 6 minutes.<EOS>",
14: "Physiological Signals: Conductance keeps falling while pulse lifts and temperature drops, the class moving still to generic on a high count of 150.0 - the cardiac rise looks activity-driven rather than emotional.\nPR: steady near 104.0 bpm, flat, in this 6-minute span. ACCEL: steady near 0.06 g, flat, in this 6-minute span.\nEDA: steady near 6.88 uS, flat, in this 6-minute span.\nStress score: 0 (qualitative label not reported).<EOS>",
15: "Physiological Signals: Conductance eases further while pulse stays up and motion rises, with still turning generic and the count at 168.0, the highest of the session - sustained movement accounts for the elevated pulse.\nStress score: 0 (qualitative label not reported).\nACCEL: steady near 0.104 g, flat, through these 6 minutes. PR: steady near 104.0 bpm, flat, through these 6 minutes.\nEDA: steady near 6.1 uS, flat, through these 6 minutes.<EOS>",
16: "Physiological Signals: The closing window has conductance still settling, pulse and motion level and temperature drifting down, generic activity near a count of 151.0 placing the readings within what the movement would produce.\nEDA: steady near 5.48 uS, flat, final 6 minutes.\nACCEL: steady near 0.111 g, flat, final 6 minutes. Stress score: 0 (qualitative label not reported).\nPR: steady near 104.0 bpm, flat, final 6 minutes.<EOS>",
}

NEW_RESPONSE = {
1: ("Emotional Validation",
    "I'm really glad you said that out loud, even if you don't have the words for it yet. Feeling stuck usually means you've been carrying something heavy on your own for a while, and that takes a toll. I'm also picking up on signs that your body hasn't fully settled either, which fits what you're describing. Take your time and tell me what's been going on."),
2: ("Clarification",
    "It doesn't need a name for it to matter, and you don't have to define it before you talk about it. Plenty of connections sit in that in-between space where the labels just don't fit, and that ambiguity is its own kind of hard. I'm picking up gentle signs that you're holding a bit more tension than usual as you start, which is understandable before saying something out loud for the first time. Tell me what's been happening between you two, and we can look at it together without deciding what it should be called."),
3: ("Avoid Judgment and Criticism",
    "Thank you for trusting me with that. Feelings don't check whether someone is available before they show up, so there's nothing here for you to be ashamed of. What I notice is that your body seems to be holding a fair amount of tension even though you're sitting fairly still, which tells me this has been weighing on you. What's it been like for you, carrying this?"),
4: ("Reflective Statements",
    "So you do try to step back, and then something pulls you right back in - and it isn't really coming from you. That must make it very hard to get any distance, because every time you start to settle, the situation reopens. Your signals suggest that unsettled feeling is showing up physically too, even while you've been sitting quietly. What usually happens when they reach out?"),
5: ("Emotional Validation",
    "That's such a painful position to be in, and I don't think it means you're weak. When someone knows how you feel and still keeps calling, the door never fully closes, and hope is very hard to switch off. I can see some signs that you're still carrying that tension in your body right now, without much movement to explain it. It makes sense that you go back."),
6: ("Normalize Experiences",
    "That makes complete sense. Feelings that grow out of a real friendship tend to run deeper than ones that start with attraction, because there's already trust and history underneath them. As you go back over how it began, your physical response stays fairly level - this part seems to be settled history for you rather than the raw bit. A lot of people find this exact situation the hardest kind to move through, precisely because the friendship was genuine. You're not being dramatic about this."),
7: ("Empathetic Statements",
    "I can hear how much of your life that person occupied. Hours of conversation, the person you told things to first, the one whose name came up in every plan - when someone is woven through your days like that, the closeness stops feeling like a choice and starts feeling like the shape of your life. So what you're grieving isn't only them; it's your own routine, and the version of your days that had them in it. And this one isn't settled history - as you revisit those hours the tension edges up rather than easing, with you sitting almost completely still. That's a real loss, and it's fair to feel it as one."),
8: ("Reflective Statements",
    "So it isn't one confusing moment, it's the same loop coming around again, and that repetition is what's leaving you unsure of what to believe. That confusion is doing something to you physically as well - your body is showing a fair bit of tension even though you've barely moved. Would it help to look at the pattern rather than each individual incident?"),
9: ("Emotional Validation",
    "That's a hard thing to let yourself think, and an even harder one to say. Wondering whether the care you get is real or convenient is exhausting, because it makes you question every kind moment too. Your signals show quite a lot of arousal right now with almost no movement behind it, which fits how heavy this question is. Whatever the answer turns out to be, what you give in a relationship deserves to be met."),
10: ("Provide Different Perspectives",
    "I understand why that stings. One way to look at it is that they may be managing their own comfort rather than making a choice about you at all - which is not a kindness, even if it isn't meant as cruelty. That framing doesn't excuse it, but it may take some of the weight off you, because it means their behaviour is about them, not about your worth. Your body is showing a steady level of tension while we talk through this, so go gently."),
11: ("Affirmation",
    "You showed up for that person consistently, as class representative and as a friend, and that says something real about the kind of person you are. Being reliable and generous like that is not a mistake, even when it isn't returned in the way you hoped. Your signals are running at their highest of this conversation as you look back on it, though you've been moving about too, so I'd hold that lightly - what matters is that recalling it clearly costs you something. Please don't let this situation convince you that caring was the wrong thing to do."),
12: ("Empathetic Statements",
    "That would hurt anyone. Being in the room while they turn to their partner puts you in a position where you're expected to be fine, and you're not fine, and you can't say so. Your signals have been running high through this conversation, so this clearly isn't a small thing you're just imagining. You're allowed to find that unbearable."),
13: ("Collaborative Planning",
    "Let's think about it together rather than me handing you a rule. From everything you've said, this connection is costing you more peace than it gives you, and you can't change their choices - only how much access they have to your time. One option is a defined break, where you don't respond for a set period and see how you feel by the end of it. Your body has started to settle over these last few minutes, which makes this a better moment to decide something than the middle of the conversation was. Would something like that feel possible, or too big a step right now?"),
14: ("Stress Management",
    "You can't switch feelings off, and trying usually makes them louder. What you can manage is what you do while they're there. Three things that tend to work: leave the phone face down and out of reach for an hour after a call, so the urge to reply has to pass on its own; slow your breathing out longer than you breathe in for two minutes when the wave hits; and get moving rather than sitting with it. That last one suits you especially - your readings show your pulse is already up from moving about, and walking a strong feeling off is far easier than thinking it away."),
15: ("Promote Self-Care Practices",
    "That's worth taking seriously, because your studies are the part of this you can still protect. Try short, contained sessions rather than long ones - twenty-five minutes with your phone in another room does more right now than an evening of half-attention. Sleep and food matter more than usual while you're carrying this. Your signals are still running fairly high, though you've been moving about a good deal, so don't read that as a warning sign - just a reason not to sit down to a long study session tonight expecting it to go well. Small consistent progress is genuinely enough at the moment."),
16: ("Offer Hope",
    "Thank you for trusting me with all of that - it wasn't a small thing to say out loud. This won't feel this sharp forever; the intensity does fade, usually before you notice it happening. Your readings have settled quite a bit since we started talking, which is a small sign of that in itself. Be patient with yourself, and hold out for someone who meets your care with the same clarity you give."),
}

SCORES = {
1:  {"orig": [4, 3, 5, 1, 5, 5], "new": [5, 4, 5, 5, 5, 5]},
2:  {"orig": [4, 3, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
3:  {"orig": [4, 3, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
4:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
5:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
6:  {"orig": [5, 4, 5, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
7:  {"orig": [4, 3, 5, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
8:  {"orig": [4, 3, 4, 1, 5, 5], "new": [4, 4, 5, 5, 5, 5]},
9:  {"orig": [4, 4, 4, 1, 5, 5], "new": [5, 4, 5, 5, 5, 5]},
10: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 4, 5, 4, 5, 5]},
11: {"orig": [4, 4, 5, 1, 5, 5], "new": [5, 4, 5, 3, 5, 5]},
12: {"orig": [5, 3, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
13: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 4, 5, 5]},
14: {"orig": [4, 3, 4, 1, 4, 5], "new": [4, 5, 5, 4, 5, 5]},
15: {"orig": [4, 4, 4, 1, 5, 5], "new": [4, 5, 5, 3, 5, 5]},
16: {"orig": [5, 4, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
}
