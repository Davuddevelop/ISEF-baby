"""Loader for NinaPro DB6 .mat files.

ASSUMPTIONS TO VERIFY against https://ninapro.hevs.ch/instructions/DB6.html
when you download the data (these are written from memory, not checked):
  - files are named S{subject}_D{day}_T{time}.mat
  - EMG is in variable `emg` (samples x channels)
  - corrected labels are in `restimulus` / `rerepetition`
    (raw `stimulus` / `repetition` are the cue timings; the "re-" versions
    are re-labelled to match the actual movement and are usually preferred)
  - sampling rate is 2000 Hz
  - some channel columns may be empty (all zeros)
If any assumption is wrong, the loader fails loudly with a message saying which.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from .session import Session

DB6_FS_DEFAULT = 2000.0
_NAME = re.compile(r"S(\d+)_D(\d+)_T(\d+)", re.IGNORECASE)


def parse_name(path: str | Path) -> tuple[int, int, int]:
    m = _NAME.search(Path(path).stem)
    if not m:
        raise ValueError(
            f"Cannot read subject/day/time from file name '{Path(path).name}'. "
            "Expected something like S1_D1_T1.mat. Check data/README.md."
        )
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _pick(mat: dict, names: list[str], path: Path) -> np.ndarray:
    for n in names:
        if n in mat:
            return np.asarray(mat[n])
    available = sorted(k for k in mat if not k.startswith("__"))
    raise KeyError(f"{path.name}: none of {names} found. Variables in file: {available}")


def load_db6_session(path: str | Path, use_relabelled: bool = True,
                     drop_empty_channels: bool = True) -> Session:
    path = Path(path)
    subject, day, time = parse_name(path)
    mat = loadmat(path)

    emg = _pick(mat, ["emg"], path).astype(np.float64)
    label_keys = ["restimulus", "stimulus"] if use_relabelled else ["stimulus", "restimulus"]
    rep_keys = ["rerepetition", "repetition"] if use_relabelled else ["repetition", "rerepetition"]
    labels = _pick(mat, label_keys, path).ravel()
    repetition = _pick(mat, rep_keys, path).ravel()

    fs = DB6_FS_DEFAULT
    if "frequency" in mat:
        fs = float(np.asarray(mat["frequency"]).ravel()[0])

    meta = {"file": str(path), "channels_original": emg.shape[1]}
    if drop_empty_channels:
        keep = np.any(emg != 0, axis=0)
        meta["dropped_channels"] = [int(i) for i in np.where(~keep)[0]]
        emg = emg[:, keep]

    return Session(emg=emg, labels=labels, repetition=repetition, fs=fs,
                   subject=subject, day=day, time=time, source="ninapro_db6", meta=meta)


def list_db6_sessions(folder: str | Path, subject: int | None = None) -> list[Path]:
    """All DB6 files in a folder, sorted along the drift timeline."""
    folder = Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"{folder} does not exist. See data/README.md for where to put DB6.")
    files = [p for p in folder.glob("*.mat") if _NAME.search(p.stem)]
    if subject is not None:
        files = [p for p in files if parse_name(p)[0] == subject]
    return sorted(files, key=lambda p: (parse_name(p)[0], parse_name(p)[1], parse_name(p)[2]))
