# Our project in simple words: what we build, in which order

*Written 18 Nov 2026. Dates are planning guesses, not official deadlines.*

---

## 1. The big picture (read this first)

We are building a **robot hand that gets better the longer you use it**.

A normal bionic hand listens to the tiny electric signals your arm muscles make, and guesses what you want to do. The problem: those signals change all the time (sweat, tired muscles, the sensor band sliding a little). So the guesses get worse during the day, and people get frustrated.

Today's fix is to stop and "recalibrate" by hand. Nobody likes doing that.

**Our idea:** the hand keeps learning while you use it, so you never have to recalibrate.

We prove it with numbers: *"after X hours, a normal hand is only Y% correct, ours is still Z% correct."*

---

## 2. The three parts of the product

| Part | What it is | Who builds it |
|---|---|---|
| **The band** | A strap with 8 sensors that reads muscle signals from the arm | Your friend |
| **The brain** | Software that turns the signals into "which grip does the person want?" and keeps learning | **You** |
| **The hand** | 3D-printed fingers moved by small motors | Your friend |

The brain is the most important part for the competition. It is the thing nobody else has built the way we want to.

---

## 3. The versions (what we build, in order)

Think of it as stairs. Each step must work before we climb to the next.

| Version | What it does | What you can show | Rough time |
|---|---|---|---|
| **v0: Brain on public data** | Works only on a computer, using recordings that scientists already made (NinaPro). No hardware. | One chart: our brain stays accurate over days while a normal one gets worse | Nov to mid Jan |
| **v0.5: Fake band** | A program pretends to be the band by replaying the recordings, so the brain works "live" | Brain running in real time | Dec to Jan |
| **v1: Real band + one finger** | Your friend's real sensors and one working finger with a motor | One finger that moves when you tense your arm | Dec to Feb |
| **v2: Whole hand** | 5 fingers and a moving thumb, about 6 motors | The full hand, gripping things | Jan to Feb |
| **v3: Real tests** | We test with real people wearing the band, with the hand on a stand next to them. Needs permission first. | Our own data and our own chart | Feb |
| **Final** | Poster, practice for the judges' questions | The project at the national round | Early March (guess) |

**Safety net:** if the hardware is late, **v0 still gives you real results** for the written application, because it uses real recordings.

---

## 4. Where we are right now

**Done**
- Project folder is set up, with a shared way to store EMG data.
- We downloaded real data for subject 1 (days 1 to 3) and ran the first chart on it.
- We looked at the chart: some channels got louder and others did not, and the biggest channels stayed in the same place. That looks more like a **strength change** than the band sliding around. But this is **one person, one movement**, so it is only a first hint.
- We checked the data: one grasp is one unbroken stretch of about 6.7 seconds. That is longer than the 4 seconds in the cue, because the dataset's authors adjusted the labels afterwards.

**Not done yet**
- The second half of subject 1's data (days 4 and 5) and the other 9 people. We are short on disk space, so we wait.
- Which grasp has which ID number. The page does not say. We must check it in the original paper.

---

## 5. What comes next, step by step (the "M" steps)

Each step produces something you can see.

**M2: Turn the raw signal into numbers a computer can learn from.**
The raw signal is a wiggly line. We cut it into short pieces (windows of 0.2 seconds) and describe each piece with a few numbers, like "how strong is it?" and "how jagged is it?". **You write this code.** I give you tests that tell you when it is right.

**M3: The "frozen" brain.**
Train a simple classifier on day 1 and never change it. Test it on later days. We expect it to get worse. That drop **is the problem** we are solving, so this chart matters.

**M4: The "recalibrated" brain.**
Same classifier, but retrained at the start of every session. This is what real products do today. It is the competitor we must beat or match.

**M5: Our adapting brain (the core of the project).**
First a very simple version: keep re-balancing how strong each channel is. Then a smarter version that learns from feedback ("that grip was right", "that one was wrong"). **You design and write this.** I will question your choices, as a judge would.

**M6: The final chart.**
All three brains, all 10 people, one picture. This goes into the written application.

**M7: The agreement with your friend** (starts early, in parallel).
You write down exactly what the band sends to the software and what the software sends back to the hand. If both of you follow it, the parts will plug together later.

---

## 6. How we work together

- **You write the important code** (the features, the classifiers, the adapting part). You must understand every line, because the judges will ask.
- **I build the tools around it** and I review your work. Before each step you tell me your plan in 3 or 4 sentences, and I try to find holes in it.
- **Tests come first.** A test says what "correct" means. When it goes green, the code is correct.
- **Save your work often with git** (commit and push). Never lose work.

**Golden rules for honest results**
1. Never mix training and test data from the same moment. Test on a different day.
2. "Rest" is about a quarter of the data, so always look at accuracy per grip, not only the average.
3. Choose all settings using day 1 only. Days 2 and later are the exam.
4. One person is not a result. Use all ten.
5. Made-up (synthetic) data is only for testing code. It never goes on the poster.

---

## 7. Decisions that are still open (they belong to you)

1. **The reward:** how does the brain find out it was right? (a button press, the task result, or the person correcting themselves)
2. **What to call it:** it may technically be a "contextual bandit", a simple form of reinforcement learning. Decide and be ready to defend the name.
3. **The goal in numbers:** "stay above X% accuracy for T hours with no recalibration."
4. **Finger design** (your friend decides): two strings per finger or a linkage; the plan so far is 6 motors, with 2 for the thumb.
5. **Human testing rules:** find out what permission the competition needs before anyone tests on a person, including yourselves.
6. **Project name.**

---

## 8. Words explained

| Word | Meaning |
|---|---|
| **EMG** | The tiny electric signal your muscles make |
| **Decoder** | The software that guesses which grip you want from the EMG |
| **Drift** | The signal slowly changing over hours and days |
| **Frozen** | Trained once and never changed |
| **Recalibration** | Stopping to retrain the decoder |
| **Adapter** | Our part, which updates the decoder while you use it |
| **Window** | A short piece of signal (0.2 seconds) cut out for analysis |
| **Feature** | A number that describes a window, such as "how strong is it?" |
| **Baseline** | The thing we compare ourselves against (frozen and recalibrated) |
| **Reward** | The "right or wrong" message the brain learns from |
| **Synthetic data** | Made-up data used only to test that code runs |

---

## 9. Your checklist for this week

- [ ] Free more disk space (aim for 5 GB or more).
- [ ] Write your **M2 plan** in 3 or 4 sentences: window and step sizes in samples at 2000 Hz, and how you will label a window that is half rest and half movement.
- [ ] Do the feature tests on paper (use the small array in `tests/test_features.py`).
- [ ] Look up in the Palermo et al. 2017 paper which ID is which grasp.
- [ ] Ask your friend: two strings or linkage? What parts do you already have?
- [ ] Find the official deadlines and the human-testing rules for the competition.
