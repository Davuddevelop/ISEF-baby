# Software v0 plan

## Definition of done
**One figure:** intent-decoding accuracy across the 10 DB6 sessions (5 days × morning/afternoon) for:
1. **Frozen**: trained on D1T1, never updated
2. **Recalibrated**: retrained at the start of every session (the commercial approach)
3. **Adaptive (ours)**: updated online from a reward signal, no manual step

Averaged over all 10 subjects, with spread. Real data, no hardware. This figure goes into the January annotation.

## Milestones

| # | Milestone | Owner | Status |
|---|---|---|---|
| M0 | Repo, environment, data format (`Session`), tests | Claude (scaffold) | ✅ done |
| M1 | Look at the data: loader + drift plot | Claude (tools), **you** (run on DB6, interpret) | 🔧 tools ready, waiting for DB6 |
| M2 | Windowing + Hudgins features (`src/emghand/signal/features.py`) | **You** | ⏳ spec in `tests/test_features.py` |
| M3 | Frozen LDA baseline, split by session | **You** | ⏳ |
| M4 | Per-session recalibration baseline | **You** | ⏳ |
| M5 | Adapter: (a) unsupervised re-normalisation, (b) reward-driven bandit/RL | **You** (core contribution) | ⏳ |
| M6 | Evaluation across 10 subjects + final figure | **You**, Claude reviews | ⏳ |
| M7 | Interface contract with hardware + fake armband stream | **Both of you** + friend | ⏳ parallel |

## Rules
1. **Never split windows randomly.** Train and test come from different sessions or repetitions.
2. Report per-class accuracy and a confusion matrix; "rest" dominates the data.
3. Choose settings using D1 data only; days 2–5 are the test.
4. Ten subjects, not one.
5. Synthetic data (`make_synthetic_session`) is for testing code only. It never appears on the poster as a result.
6. Before each milestone, write your plan in 3–4 sentences and get it reviewed **before** coding.

## Open assumptions to verify when DB6 is downloaded
- File names `S{subject}_D{day}_T{time}.mat`, variables `emg`, `restimulus`, `rerepetition`, sampling rate 2000 Hz (written from memory; check the official DB6 guidelines).
- Which channel columns are empty.
