"""Specification for M2. Remove the skip marker when you start implementing.

Each test is small enough to check by hand on paper. Do that first: if you
can't compute the expected answer yourself, you don't understand the feature yet.
"""
import numpy as np
import pytest

from emghand.signal import features as F

pytestmark = pytest.mark.skip(reason="M2 is your milestone: remove this line to start")

X = np.array([[1.0, -2.0], [-1.0, 2.0], [1.0, -2.0], [-1.0, 2.0]])


def test_windows_only_full():
    starts = F.sliding_windows(n_samples=1000, fs=1000, win_s=0.2, step_s=0.05)
    assert starts[0] == 0 and starts[1] == 50
    assert starts[-1] + 200 <= 1000
    assert len(starts) == 17


def test_mav():
    assert np.allclose(F.mav(X), [1.0, 2.0])


def test_rms():
    assert np.allclose(F.rms(X), [1.0, 2.0])


def test_waveform_length():
    assert np.allclose(F.waveform_length(X), [6.0, 12.0])


def test_zero_crossings_with_threshold():
    assert F.zero_crossings(X).tolist() == [3, 3]
    assert F.zero_crossings(X, threshold=3.0).tolist() == [0, 3]


def test_window_labels_shape():
    labels = np.array([0] * 100 + [1] * 100)
    starts = np.array([0, 50, 100])
    out = F.window_labels(labels, starts, win=100)
    assert out.shape == (3,)
    assert out[0] == 0 and out[2] == 1  # pure windows are unambiguous
