"""The one data format every part of the project agrees on.

Whether data comes from NinaPro, the synthetic generator, or (later) the real
armband, it becomes a `Session`. Code downstream never needs to know the source.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Session:
    """One continuous recording.

    emg:        (n_samples, n_channels) float array, raw EMG.
    labels:     (n_samples,) int array. 0 = rest, 1..K = movement/grasp id.
    repetition: (n_samples,) int array. Which repetition of the movement this
                sample belongs to (0 during rest). Used to split train/test
                WITHOUT leakage: never split windows randomly.
    fs:         sampling rate in Hz.
    subject, day, time: where this session sits in the drift timeline.
                time = 1 (morning) or 2 (afternoon) for DB6.
    source:     "ninapro_db6", "synthetic", "armband", ...
    """

    emg: np.ndarray
    labels: np.ndarray
    repetition: np.ndarray
    fs: float
    subject: int
    day: int
    time: int
    source: str
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.emg = np.asarray(self.emg, dtype=np.float64)
        self.labels = np.asarray(self.labels).astype(np.int64).ravel()
        self.repetition = np.asarray(self.repetition).astype(np.int64).ravel()
        if self.emg.ndim != 2:
            raise ValueError(f"emg must be 2-D (samples, channels), got shape {self.emg.shape}")
        n = self.emg.shape[0]
        if self.labels.shape[0] != n or self.repetition.shape[0] != n:
            raise ValueError(
                f"length mismatch: emg={n}, labels={self.labels.shape[0]}, "
                f"repetition={self.repetition.shape[0]}"
            )

    @property
    def n_channels(self) -> int:
        return self.emg.shape[1]

    @property
    def duration_s(self) -> float:
        return self.emg.shape[0] / self.fs

    @property
    def classes(self) -> np.ndarray:
        return np.unique(self.labels)

    @property
    def order(self) -> int:
        """Position on the drift timeline: D1T1=0, D1T2=1, D2T1=2, ..."""
        return (self.day - 1) * 2 + (self.time - 1)

    @property
    def name(self) -> str:
        return f"S{self.subject}_D{self.day}_T{self.time}"

    def segment(self, label: int, repetition: int) -> np.ndarray:
        """EMG samples of one repetition of one movement."""
        mask = (self.labels == label) & (self.repetition == repetition)
        return self.emg[mask]

    def summary(self) -> str:
        lines = [
            f"{self.name} [{self.source}] fs={self.fs:g} Hz, "
            f"{self.emg.shape[0]} samples ({self.duration_s:.1f} s), {self.n_channels} channels",
        ]
        for c in self.classes:
            reps = np.unique(self.repetition[self.labels == c])
            reps = reps[reps > 0]
            share = np.mean(self.labels == c) * 100
            lines.append(f"  class {c:>2}: {share:5.1f}% of samples, {len(reps)} repetitions")
        return "\n".join(lines)
