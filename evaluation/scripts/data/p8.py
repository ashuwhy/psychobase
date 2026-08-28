"""Participant 8 - Ashutosh Sharma. Model outputs for steps 2-4."""

LABEL = "Participant 8"
SOURCE = "output_participantGrouped8data_full_data.json"

NOTES = [
    "Summary wording and line order are varied turn to turn rather than following one template. "
    "This tab was originally produced in the fixed-template style and has been regenerated.",
    "Turn 16 has <code>PR: null</code> in raw_physio, so the summary reports pulse rate as not "
    "reported rather than inventing a value.",
    "Turn 2's training_string_case2 prose says EDA was dropping, but raw_physio shows "
    "0.12 -> 0.13 (rising). The shortened summary follows the raw values.",
    "This conversation is informational rather than emotional - final-year project direction and "
    "career questions - so the master prompt's warmth is applied without inventing distress that "
    "the user never expresses.",
    "Turns 2, 8 and 13 were re-generated after the first evaluation pass scored them low on "
    "specificity or empathy; the scores shown are for the improved versions.",
]

PHYSIO_SHORT = {
1: "Physiological Signals: Conductance eases fractionally in the opening minute while pulse, temperature and motion all rise together and the count climbs 9.0 to 64.0; still activity throughout, so the movement increase carries much of this.\nPR: 67.0 -> 71.0 bpm, increasing, first minute.\nEDA: 0.14 -> 0.13 uS, decreasing, first minute.\nACCEL: 0.006 -> 0.042 g, increasing, first minute.\nStress score: 0 (qualitative label not reported).<EOS>",
2: "EDA: 0.12 -> 0.13 uS, increasing, past 2 minutes.\nPR: 65.0 -> 66.0 bpm, increasing, past 2 minutes.\nACCEL: 0.004 -> 0.006 g, increasing, past 2 minutes.\nStress score: 1 (qualitative label not reported).\nPhysiological Signals: Every channel drifts up by a hair with temperature following, while the class turns still to walking on a low count of 8.0; changes this small are not clearly activity-related either way.<EOS>",
3: "Stress score: 1 (qualitative label not reported).\nPhysiological Signals: Conductance, pulse and temperature all edge upward across four minutes while motion falls away and the count drops 8.0 to 4.0; with still becoming walking, none of this is activity-driven.\nACCEL: 0.014 -> 0.004 g, decreasing, these 4 minutes.\nEDA: 0.12 -> 0.13 uS, increasing, these 4 minutes.\nPR: 66.0 -> 67.0 bpm, increasing, these 4 minutes.<EOS>",
4: "Physiological Signals: Temperature and motion rise while conductance and pulse both ease, the count sliding 27.0 to 20.0 as still turns to walking; the movement change is mild, so the picture is only partly activity-related.\nEDA: 0.13 -> 0.12 uS, decreasing, this 6-minute window.\nStress score: 1 (qualitative label not reported).\nACCEL: 0.015 -> 0.022 g, increasing, this 6-minute window.\nPR: 70.0 -> 68.0 bpm, decreasing, this 6-minute window.<EOS>",
5: "PR: 64.0 -> 80.0 bpm, increasing, over the last 6 minutes.\nEDA: steady near 0.12 uS, flat, over the last 6 minutes.\nACCEL: 0.003 -> 0.006 g, increasing, over the last 6 minutes.\nPhysiological Signals: Pulse jumps sixteen beats while conductance holds flat, temperature eases and motion stays negligible; walking gives way to still on a low count of 16.0, so that rise has no movement behind it.\nStress score: 1 (qualitative label not reported).<EOS>",
6: "Physiological Signals: Conductance and motion tick up from a very low base while pulse is unchanged and temperature falls; walking turns still with the count at 16.0, and nothing here reads as activity-related.\nStress score: 1 (qualitative label not reported).\nEDA: 0.11 -> 0.12 uS, increasing, this 6-minute stretch.\nPR: steady near 65.0 bpm, flat, this 6-minute stretch.\nACCEL: 0.003 -> 0.008 g, increasing, this 6-minute stretch.<EOS>",
7: "ACCEL: steady near 0.003 g, flat, during these 6 minutes.\nPR: 62.0 -> 66.0 bpm, increasing, during these 6 minutes.\nEDA: steady near 0.12 uS, flat, during these 6 minutes.\nStress score: 1 (qualitative label not reported).\nPhysiological Signals: Pulse rises modestly with conductance flat, temperature declining and the activity count at zero; the class moves walking to still, so no movement occurred at all in this window.<EOS>",
8: "Physiological Signals: Pulse drops five beats while conductance stays flat and both temperature and motion decline, the count sitting at zero despite the class changing still to walking; the fall is not activity-related.\nEDA: steady near 0.12 uS, flat, preceding 6 minutes.\nStress score: 1 (qualitative label not reported).\nPR: 67.0 -> 62.0 bpm, decreasing, preceding 6 minutes.\nACCEL: 0.004 -> 0.003 g, decreasing, preceding 6 minutes.<EOS>",
9: "Stress score: 2 (Mild stress).\nPR: 63.0 -> 72.0 bpm, increasing, in this 6-minute span.\nEDA: 0.12 -> 0.13 uS, increasing, in this 6-minute span.\nACCEL: 0.005 -> 0.018 g, increasing, in this 6-minute span.\nPhysiological Signals: Conductance, pulse and motion climb together while temperature eases and the count rises 5.0 to 25.0 as still turns walking; the arousal is at least partly explained by that movement.<EOS>",
10: "Physiological Signals: Everything eases at once - conductance, pulse, temperature and motion - with the count falling 13.0 to 9.0 despite a still-to-walking class change; almost no movement was actually recorded.\nEDA: 0.11 -> 0.1 uS, decreasing, through the past 6 minutes.\nACCEL: 0.006 -> 0.005 g, decreasing, through the past 6 minutes.\nStress score: 1 (qualitative label not reported).\nPR: 69.0 -> 65.0 bpm, decreasing, through the past 6 minutes.<EOS>",
11: "PR: 69.0 -> 92.0 bpm, increasing, over these 6 minutes.\nACCEL: 0.012 -> 0.137 g, increasing, over these 6 minutes.\nEDA: steady near 0.11 uS, flat, over these 6 minutes.\nStress score: 0 (qualitative label not reported).\nPhysiological Signals: Pulse and motion rise sharply together as the count reaches 144.0 with walking sustained throughout, conductance and temperature flat; this is the clearest activity-driven window of the session.<EOS>",
12: "Physiological Signals: Pulse falls twenty-four beats and motion halves as walking turns still and the count drops to 7.0, conductance edging up and temperature flat; the fall tracks the settling movement.\nStress score: 1 (qualitative label not reported).\nEDA: 0.11 -> 0.12 uS, increasing, last 6 minutes.\nACCEL: 0.009 -> 0.005 g, decreasing, last 6 minutes.\nPR: 84.0 -> 60.0 bpm, decreasing, last 6 minutes.<EOS>",
13: "EDA: 0.12 -> 0.11 uS, decreasing, this six-minute window.\nPR: 60.0 -> 57.0 bpm, decreasing, this six-minute window.\nACCEL: 0.031 -> 0.003 g, decreasing, this six-minute window.\nStress score: 1 (qualitative label not reported).\nPhysiological Signals: All four channels decline together as the count falls 42.0 to 0.0 and walking becomes generic; a straightforward picture of activity winding down.<EOS>",
14: "Physiological Signals: Pulse and motion rise while conductance holds flat and temperature falls sharply, the count climbing 23.0 to 42.0 with walking sustained; part of the rise belongs to that movement.\nStress score: 2 (Mild stress).\nACCEL: 0.018 -> 0.023 g, increasing, these 6 minutes.\nEDA: steady near 0.12 uS, flat, these 6 minutes.\nPR: 63.0 -> 70.0 bpm, increasing, these 6 minutes.<EOS>",
15: "ACCEL: 0.018 -> 0.12 g, increasing, six-minute window.\nPR: 64.0 -> 71.0 bpm, increasing, six-minute window.\nEDA: 0.12 -> 0.11 uS, decreasing, six-minute window.\nStress score: -2 (qualitative label not reported).\nPhysiological Signals: Motion increases nearly sevenfold and the count almost triples to 116.0 as still turns walking, taking pulse up with it while conductance eases; largely an activity-driven window.<EOS>",
16: "Physiological Signals: Conductance and motion both decline as the count eases 106.0 to 43.0 under generic activity with temperature flat; pulse was not captured for this window, so the reading rests on the other channels.\nEDA: 0.09 -> 0.08 uS, decreasing, in these 6 minutes.\nPR: not reported for this window.\nStress score: 0 (qualitative label not reported).\nACCEL: 0.082 -> 0.04 g, decreasing, in these 6 minutes.<EOS>",
17: "PR: 70.0 -> 61.0 bpm, decreasing, over the preceding 6 minutes.\nEDA: 0.09 -> 0.08 uS, decreasing, over the preceding 6 minutes.\nACCEL: 0.058 -> 0.022 g, decreasing, over the preceding 6 minutes.\nPhysiological Signals: Conductance, pulse and motion all come down while temperature rises slightly, the count easing 63.0 to 43.0 as walking turns generic; the decline follows the movement.\nStress score: 0 (qualitative label not reported).<EOS>",
18: "Stress score: 0 (qualitative label not reported).\nPhysiological Signals: Motion drops steeply and the count more than halves to 46.0 as walking becomes generic, yet pulse edges up and conductance stays flat; that small cardiac rise is not explained by the falling movement.\nACCEL: 0.075 -> 0.031 g, decreasing, final 6 minutes.\nEDA: steady near 0.09 uS, flat, final 6 minutes.\nPR: 64.0 -> 66.0 bpm, increasing, final 6 minutes.<EOS>",
}

NEW_RESPONSE = {
1: ("Suggest Options",
    "Final-year projects carry a lot of weight, so it makes sense that you want to get the direction right. The good news is that cybersecurity and machine learning sit really well together, so you don't have to pick one - AI-based intrusion detection, phishing detection, malware classification, or anomaly detection all let you use both. I'm also picking up on gentle cues that your body hasn't fully settled yet, so take this at a pace that feels comfortable. Would you rather build something research-oriented, or something people could actually use?"),
2: ("Reflective Statements",
    "So you're leaning toward something people can actually pick up and use, rather than a paper. That tells me you care about seeing the impact of what you build, which is a good instinct to follow - and it shapes the project in practical ways too: you'd be prioritising a working interface and a real dataset over novelty, and you'd have something demonstrable to put in front of an interviewer in eight months. What would you want it to grow into once the project is submitted?"),
3: ("Affirmation",
    "Aiming for a startup idea takes some courage, and I think it says a lot that you're thinking beyond just clearing the semester. That ambition is genuinely an advantage here - it will push you to pick a problem people actually feel, rather than one that just looks good on a slide. The strongest starting points tend to be things small businesses struggle with: phishing defence, cloud security, or a security copilot for developers. Who do you picture as the person you're building this for?"),
4: ("Share Information",
    "Good question to ask before committing to it. At its core, it would look at emails, links, and attachments and flag phishing attempts - but the useful part is that it explains why something looks suspicious, like an odd sender domain, urgent pressure language, or a fake login page. You could start small as a browser extension and grow it into a dashboard for organisations later. Does that sound like the kind of thing you'd enjoy spending a year on?"),
5: ("Share Information",
    "Sure, keeping it short. ML earns its place in phishing detection, intrusion detection, malware detection, anomaly detection, user behaviour analytics, fraud detection, and insider threat detection. Anomaly detection and AI security copilots are where the startup potential is strongest right now. I notice your body seems a little more revved up than the conversation sounds, so feel free to slow this down if it's getting heavy."),
6: ("Provide Different Perspectives",
    "That's a fair challenge, and it's worth pushing on. The way I'd frame it is that ML isn't there to replace rule-based security - it sits alongside it. Rules catch the attacks we already know about, and ML flags the odd behaviour that doesn't match anything on the list yet, with a human analyst making the final call. Seen that way, it's less about ML being unbreakable and more about it widening what you can notice."),
7: ("Share Information",
    "You've understood it exactly right, and the load question is the one serious engineers actually worry about. The usual answer is triage: cheap rule-based filters handle the bulk of events, and the ML models only look at the small slice that seems suspicious. Lightweight models, batching, and risk-based sampling keep it affordable at scale. Making AI security cheaper to run, rather than just more accurate, is itself a strong startup angle."),
8: ("Share Information",
    "On the AI-driven side, the names worth studying are CrowdStrike, Palo Alto Networks, Microsoft Security, SentinelOne, Darktrace, Abnormal Security, and Vectra AI. For cybersecurity more broadly, add Fortinet, Check Point, Cloudflare, Zscaler, Trend Micro, and Mandiant. If you only have time for a few, look at CrowdStrike for endpoint telemetry at scale, Darktrace for unsupervised anomaly detection, and Abnormal Security for email - between them they cover most of how AI actually lands in a shipped product, and all three publish enough technical material to learn from."),
9: ("Collaborative Planning",
    "Narrowing down is often the hardest part, so let's do it together. If I had to pick one for you, I'd say AI-powered phishing detection - the datasets are public, it sits right where NLP meets security, and it can grow from a college project into something real. I'm also noticing some signs you're still carrying a bit of tension even though you sound steady, which is pretty normal at this stage of deciding. Shall we sketch out what a first version would need to do?"),
10: ("Share Information",
    "Of course. Phishing is an attack that tricks a person into handing over something sensitive or doing something harmful - clicking a link, entering a password, approving a payment. It arrives through fake emails, cloned websites, phone calls, SMS, and even QR codes, and it works by leaning on urgency, fear, curiosity, or trust. The technical part is almost the easy half; the psychology is what makes it effective."),
11: ("Provide Different Perspectives",
    "It doesn't really win against human psychology, and I think that's the honest framing. What it does is recognise the fingerprints those tactics leave behind - artificial urgency, lookalike domains, unexpected login requests, phrasing that doesn't match the sender - and warn you before you act on the impulse. So it isn't outsmarting the manipulation, it's buying you the pause you need to see it. Your signals suggest you've been moving around while we talk, so no rush on any of this."),
12: ("Reframe Negative Thoughts",
    "I can hear the worry that this turns into a losing race, but I'd gently push back on that. A good model generalises rather than memorises, so it can flag a new variant that shares the underlying shape of an old attack even if it has never seen those exact words. Add regular retraining, threat intelligence feeds, and human review, and defenders adapt too. It isn't a problem you solve once - it's one you stay ahead of, and that's very different from losing."),
13: ("Affirmation",
    "You've landed on something that a lot of people take years to see clearly. Cybersecurity is a genuine arms race - attackers keep inventing, defenders keep responding - and that's exactly why the field doesn't go stale: the tooling changes every few years, but the demand underneath it doesn't, which is why security budgets tend to survive downturns that cut elsewhere. Trusting that instinct is a good sign about how you're choosing your direction."),
14: ("Collaborative Planning",
    "I like that you want to go deeper rather than stop at the project. A path that works well: start with networking, Linux, and cryptography, then move into web security through the OWASP Top 10, and practise on TryHackMe, Hack The Box, or PortSwigger's Web Security Academy. Tools like Wireshark, Nmap, and Burp Suite come naturally once you're doing the labs. I'm picking up some small signs you may still be running a little warm, so let's keep this to one step at a time - which of those feels like the right place to start?"),
15: ("Normalize Experiences",
    "This is a much more common route than it looks from where you're standing - a lot of people in security today started in plain software development roles. Honestly, engineering is one of the strongest foundations you can have, because understanding how software is built is what makes you good at finding where it breaks. Take the dev offer, build real skills, and then angle toward Application Security, Cloud Security, or Security Engineering. Nothing about starting there closes the door."),
16: ("Suggest Options",
    "That's a completely reasonable thing to want, and the corporate path has a clear ladder here. The usual shape is Software Engineer, then Application Security Engineer, then either Security Architect or an AI Security specialist role. Application Security is the sweet spot for you - it keeps you coding while staying squarely in security, and demand for it is steady. Your signals look fairly settled while we go through this, which is a good sign you're thinking it through rather than stressing over it."),
17: ("Share Information",
    "Remote-friendly is a very fair thing to optimise for. Software Engineering has the largest pool of remote roles by far, followed by Cybersecurity, AI/ML Engineering, Cloud and DevOps, and Data Engineering. Given what you've said so far, Application Security and Cloud Security fit especially well - both are heavily remote and line up with the direction you're already heading."),
18: ("Suggest Options",
    "Fair thing to ask. I'd be careful about specialising too early in areas with fewer remote openings - traditional IT support, system administration, network administration, and hardware-heavy roles tend to keep you tied to a place. Building a base in software engineering, cloud, security, and AI keeps far more doors open. I notice your signals are still a bit elevated after all the moving around, so this is a good point to pause and let it settle."),
}

SCORES = {
1:  {"orig": [3, 5, 4, 1, 5, 5], "new": [5, 4, 5, 4, 5, 5]},
2:  {"orig": [2, 5, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
3:  {"orig": [2, 5, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
4:  {"orig": [2, 5, 5, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
5:  {"orig": [1, 5, 4, 1, 4, 5], "new": [4, 4, 4, 4, 5, 5]},
6:  {"orig": [2, 5, 4, 1, 5, 5], "new": [4, 4, 5, 1, 5, 5]},
7:  {"orig": [2, 5, 5, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
8:  {"orig": [1, 5, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
9:  {"orig": [2, 4, 4, 1, 5, 5], "new": [5, 4, 5, 5, 5, 5]},
10: {"orig": [2, 5, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
11: {"orig": [2, 4, 4, 1, 5, 5], "new": [4, 4, 5, 3, 5, 5]},
12: {"orig": [2, 5, 5, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
13: {"orig": [3, 4, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
14: {"orig": [2, 5, 4, 1, 5, 5], "new": [5, 5, 5, 4, 5, 5]},
15: {"orig": [3, 4, 4, 1, 5, 5], "new": [5, 4, 5, 1, 5, 5]},
16: {"orig": [2, 4, 4, 1, 4, 5], "new": [4, 4, 5, 4, 5, 5]},
17: {"orig": [2, 5, 4, 1, 5, 5], "new": [4, 5, 5, 1, 5, 5]},
18: {"orig": [2, 5, 4, 1, 5, 5], "new": [4, 5, 5, 4, 5, 5]},
}
