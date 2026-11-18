# ISEF-baby: self-adapting myoelectric hand

A low-cost prosthetic hand whose EMG decoder keeps adapting while it is used, so control doesn't degrade as the muscle signal drifts.

- Project brief: [`docs/Project-Brief-v0.1.pdf`](docs/Project-Brief-v0.1.pdf)
- Software plan: [`docs/software-v0-plan.md`](docs/software-v0-plan.md)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Run M1 (look at drift)

Without the dataset (synthetic pipeline test, not real data):

```bash
python experiments/m1_look_at_drift.py --synthetic --movement 3
```

With NinaPro DB6 (see [`data/README.md`](data/README.md) for download):

```bash
python experiments/m1_look_at_drift.py --data data/ninapro_db6 --subject 1 --movement 3
```

Plots go to `outputs/m1/`.

## Layout

```
src/emghand/
  data/       Session format, NinaPro DB6 loader, synthetic generator
  signal/     M2: windowing + features (your milestone)
  decoders/   M3/M4: frozen + recalibrated baselines
  adapt/      M5: the adapter (core contribution)
  eval/       M6: metrics and figures
  stream/     M7: hardware interface + fake armband
experiments/  one script per figure
tests/        specs; tests/test_features.py is the M2 spec
```
