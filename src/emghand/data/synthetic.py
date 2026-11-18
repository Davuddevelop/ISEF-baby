"""Synthetic EMG with controllable drift.

THIS IS NOT REAL DATA. It exists for three reasons:
  1. test the pipeline before the real dataset is downloaded,
  2. unit tests (we know the ground truth because we made it),
  3. later, a fake armband for the real-time pipeline.
Never put synthetic results on the poster as if they were measurements.

Model: each movement activates the channels with its own pattern (a fixed
"muscle map"). EMG is band-limited noise whose amplitude follows that pattern.
Drift is modelled with the three effects from the project brief:
  - electrode shift  -> the activation pattern rotates around the armband,
  - sweat/impedance  -> per-channel gain changes,
  - noise            -> more background noise.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

from .session import Session


def _class_patterns(n_classes: int, n_channels: int, rng: np.random.Generator) -> np.ndarray:
    """(n_classes + 1, n_channels) activation levels. Row 0 = rest."""
    pats = np.zeros((n_classes + 1, n_channels))
    pats[0] = 0.05
    angles = np.arange(n_channels) / n_channels * 2 * np.pi
    for c in range(1, n_classes + 1):
        centre = rng.uniform(0, 2 * np.pi)
        width = rng.uniform(0.6, 1.4)
        bump = np.exp(np.cos(angles - centre) / width)
        bump = bump / bump.max()
        pats[c] = 0.15 + 0.85 * bump * rng.uniform(0.6, 1.0)
    return pats


def _rotate(pattern: np.ndarray, shift_channels: float) -> np.ndarray:
    """Rotate a channel pattern around the armband by a fractional number of channels."""
    n = pattern.shape[-1]
    idx = (np.arange(n) - shift_channels) % n
    lo = np.floor(idx).astype(int)
    hi = (lo + 1) % n
    frac = idx - lo
    return pattern[..., lo] * (1 - frac) + pattern[..., hi] * frac


def make_synthetic_session(subject: int = 1, day: int = 1, time: int = 1,
                           n_classes: int = 7, n_channels: int = 8, fs: float = 1000.0,
                           n_reps: int = 6, hold_s: float = 3.0, rest_s: float = 2.0,
                           shift_channels: float | None = None,
                           gain_spread: float | None = None,
                           noise: float | None = None,
                           seed: int = 0) -> Session:
    """One synthetic session. Drift grows with (day, time) unless set explicitly.

    The class "muscle map" depends only on `subject` + `seed`, so two sessions of
    the same subject share the same underlying patterns: only the drift differs.
    """
    order = (day - 1) * 2 + (time - 1)
    if shift_channels is None:
        shift_channels = 0.18 * order          # slow rotation of the band
    if gain_spread is None:
        gain_spread = 0.06 * order             # sweat / impedance
    if noise is None:
        noise = 0.03 + 0.005 * order

    base_rng = np.random.default_rng(seed * 1000 + subject)
    pats = _class_patterns(n_classes, n_channels, base_rng)
    pats = _rotate(pats, shift_channels)

    rng = np.random.default_rng(seed * 1000 + subject * 100 + order + 1)
    gains = np.exp(rng.normal(0.0, gain_spread, size=n_channels)) if gain_spread > 0 else np.ones(n_channels)

    hold, rest = int(hold_s * fs), int(rest_s * fs)
    labels, reps = [np.zeros(rest, int)], [np.zeros(rest, int)]
    for r in range(1, n_reps + 1):
        for c in range(1, n_classes + 1):
            labels += [np.full(hold, c), np.zeros(rest, int)]
            reps += [np.full(hold, r), np.zeros(rest, int)]
    labels, reps = np.concatenate(labels), np.concatenate(reps)
    n = labels.shape[0]

    # amplitude envelope per sample, smoothed so on/offsets aren't instant
    env = pats[labels] * gains
    k = max(1, int(0.08 * fs))
    kernel = np.ones(k) / k
    env = np.apply_along_axis(lambda x: np.convolve(x, kernel, mode="same"), 0, env)
    env *= 1 + 0.1 * rng.standard_normal(env.shape).cumsum(axis=0) / np.sqrt(n)  # slow wobble

    sos = butter(4, [20, min(450, fs / 2 - 1)], btype="band", fs=fs, output="sos")
    carrier = sosfilt(sos, rng.standard_normal((n, n_channels)), axis=0)
    carrier /= carrier.std(axis=0, keepdims=True)
    emg = env * carrier + noise * rng.standard_normal((n, n_channels))

    return Session(emg=emg, labels=labels, repetition=reps, fs=fs,
                   subject=subject, day=day, time=time, source="synthetic",
                   meta={"shift_channels": shift_channels, "gain_spread": gain_spread,
                         "noise": noise, "seed": seed})
