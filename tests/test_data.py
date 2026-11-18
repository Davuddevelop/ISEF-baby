import numpy as np
import pytest
from scipy.io import savemat

from emghand.data import Session, list_db6_sessions, load_db6_session, make_synthetic_session


def test_session_rejects_length_mismatch():
    with pytest.raises(ValueError):
        Session(np.zeros((10, 2)), np.zeros(9), np.zeros(10), 1000, 1, 1, 1, "test")


def test_synthetic_has_all_classes_and_reps():
    s = make_synthetic_session(n_classes=7, n_reps=6)
    assert s.classes.tolist() == list(range(8))  # rest + 7
    for c in range(1, 8):
        reps = np.unique(s.repetition[s.labels == c])
        assert reps.tolist() == list(range(1, 7))


def test_synthetic_same_subject_drifts_but_stays_related():
    a = make_synthetic_session(day=1, time=1)
    b = make_synthetic_session(day=1, time=1)
    late = make_synthetic_session(day=5, time=2)
    prof = lambda s: np.sqrt(np.mean(s.emg[s.labels == 3] ** 2, axis=0))
    assert np.allclose(a.emg, b.emg)                      # deterministic
    corr_late = np.corrcoef(prof(a), prof(late))[0, 1]
    assert 0.0 < corr_late < 0.999                         # changed, not unrelated


def test_db6_loader_on_fake_file(tmp_path):
    n = 500
    emg = np.random.default_rng(0).standard_normal((n, 16))
    emg[:, 8] = 0  # an empty channel, as DB6 may have
    lab = np.zeros(n); lab[100:200] = 2
    rep = np.zeros(n); rep[100:200] = 1
    savemat(tmp_path / "S3_D2_T1.mat", {"emg": emg, "restimulus": lab, "rerepetition": rep})
    files = list_db6_sessions(tmp_path)
    s = load_db6_session(files[0])
    assert (s.subject, s.day, s.time) == (3, 2, 1)
    assert s.n_channels == 15 and s.meta["dropped_channels"] == [8]
    assert s.segment(2, 1).shape == (100, 15)


def test_db6_loader_explains_missing_variables(tmp_path):
    savemat(tmp_path / "S1_D1_T1.mat", {"something_else": np.zeros(3)})
    with pytest.raises(KeyError, match="Variables in file"):
        load_db6_session(tmp_path / "S1_D1_T1.mat")
