"""M2 - windowing and classic time-domain EMG features.

YOUR TASK. The function signatures and the spec are fixed (other modules and the
tests depend on them); the implementation is yours. tests/test_features.py is
the specification: remove the `skip` marker there and make the tests pass.

Before coding, read about the "Hudgins features" (Hudgins et al., 1993). They
are the classic baseline every EMG paper compares against.
"""
from __future__ import annotations

import numpy as np


def sliding_windows(n_samples: int, fs: float, win_s: float = 0.2, step_s: float = 0.05) -> np.ndarray:
    """Start indices of windows of length win_s, moved by step_s.

    Only full windows: the last window must end at or before n_samples.
    Returns an int array of start indices.
    """
    raise NotImplementedError("M2: your implementation")


def mav(x: np.ndarray) -> np.ndarray:
    """Mean absolute value per channel. x: (samples, channels) -> (channels,)"""
    raise NotImplementedError("M2: your implementation")


def rms(x: np.ndarray) -> np.ndarray:
    """Root mean square per channel."""
    raise NotImplementedError("M2: your implementation")


def waveform_length(x: np.ndarray) -> np.ndarray:
    """Sum of absolute differences between consecutive samples, per channel."""
    raise NotImplementedError("M2: your implementation")


def zero_crossings(x: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    """Number of sign changes per channel where the jump is larger than threshold.

    Think: why does a threshold matter for real, noisy EMG?
    """
    raise NotImplementedError("M2: your implementation")


def window_labels(labels: np.ndarray, starts: np.ndarray, win: int) -> np.ndarray:
    """One label per window. Decide the rule yourself and write it here:
    majority vote? label at the window's end? drop mixed windows?
    Be ready to defend the choice to a judge.
    """
    raise NotImplementedError("M2: your implementation")
