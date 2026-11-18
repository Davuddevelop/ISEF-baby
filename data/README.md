# Data folder

Datasets are **not committed** to git (they're large, and the licence requires registration).

## NinaPro DB6 (start here)
- What it is: 10 intact subjects, 7 grasps, 12 repetitions, **twice a day for 5 days**. That gives real day-to-day drift.
- Download: https://ninapro.hevs.ch → DB6. Read the licence and the DB6 guidelines page first.
- Put the files here:

```
data/ninapro_db6/
  S1_D1_T1.mat
  S1_D1_T2.mat
  ...
```

The loader expects names like `S{subject}_D{day}_T{time}.mat`. If your download is named differently, **don't rename things blindly**. Open one file, check which variables it contains, and compare with the DB6 guidelines. Then tell us, so we fix the loader rather than the data.

## NinaPro DB5 (later)
Cheap 8-electrode Myo armbands at 200 Hz, closest to our hardware. Goes in `data/ninapro_db5/`.
