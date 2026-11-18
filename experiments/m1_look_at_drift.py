"""M1 - look at the data before modelling anything.

Plots the same movement from two sessions (default: first vs last on the drift
timeline) so you can SEE drift with your own eyes:
  left:  RMS envelope of every channel during the movement
  right: average activation per channel (the "muscle map"), both sessions overlaid

Usage:
  python experiments/m1_look_at_drift.py --synthetic
  python experiments/m1_look_at_drift.py --data data/ninapro_db6 --subject 1 --movement 3
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emghand.data import Session, list_db6_sessions, load_db6_session, make_synthetic_session


def rms_envelope(x: np.ndarray, fs: float, win_s: float = 0.1) -> np.ndarray:
    """Moving RMS. (Plotting helper only. Your M2 features live in emghand.signal.)"""
    k = max(1, int(win_s * fs))
    kernel = np.ones(k) / k
    return np.sqrt(np.apply_along_axis(lambda c: np.convolve(c ** 2, kernel, mode="same"), 0, x))


def channel_profile(s: Session, movement: int) -> np.ndarray:
    """Mean RMS per channel over all repetitions of one movement."""
    seg = s.emg[s.labels == movement]
    if seg.size == 0:
        raise ValueError(f"movement {movement} not found in {s.name}; classes = {s.classes.tolist()}")
    return np.sqrt(np.mean(seg ** 2, axis=0))


def load(args) -> tuple[Session, Session]:
    if args.synthetic:
        return (make_synthetic_session(subject=args.subject, day=1, time=1),
                make_synthetic_session(subject=args.subject, day=5, time=2))
    files = list_db6_sessions(args.data, subject=args.subject)
    if len(files) < 2:
        raise SystemExit(f"Need at least 2 sessions for subject {args.subject} in {args.data}, found {len(files)}")
    return load_db6_session(files[0]), load_db6_session(files[-1])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", type=Path, default=Path("data/ninapro_db6"))
    p.add_argument("--synthetic", action="store_true", help="use synthetic data (NOT real)")
    p.add_argument("--subject", type=int, default=1)
    p.add_argument("--movement", type=int, default=1)
    p.add_argument("--repetition", type=int, default=1)
    p.add_argument("--out", type=Path, default=Path("outputs/m1"))
    args = p.parse_args()

    a, b = load(args)
    print(a.summary()); print(b.summary())

    args.out.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(13, 7), gridspec_kw={"width_ratios": [2.2, 1]})
    for row, s in enumerate((a, b)):
        seg = s.segment(args.movement, args.repetition)
        if seg.size == 0:
            raise SystemExit(f"{s.name}: no data for movement {args.movement}, repetition {args.repetition}")
        env = rms_envelope(seg, s.fs)
        t = np.arange(len(seg)) / s.fs
        ax = axes[row, 0]
        for ch in range(s.n_channels):
            ax.plot(t, env[:, ch] + ch * env.max() * 0.6, lw=0.8)
        ax.set_title(f"{s.name}: movement {args.movement}, rep {args.repetition} (RMS envelope, channels stacked)")
        ax.set_xlabel("time in movement (s)"); ax.set_yticks([])

    pa, pb = channel_profile(a, args.movement), channel_profile(b, args.movement)
    x = np.arange(len(pa))
    ax = axes[0, 1]
    ax.bar(x - 0.2, pa / pa.max(), 0.4, label=a.name)
    ax.bar(x + 0.2, pb / pb.max(), 0.4, label=b.name)
    ax.set_title("muscle map (normalised mean RMS)"); ax.set_xlabel("channel"); ax.legend()

    corr = float(np.corrcoef(pa, pb)[0, 1])
    axes[1, 1].axis("off")
    axes[1, 1].text(0.0, 0.85, f"pattern correlation: {corr:.2f}\n(1.0 = identical map)", fontsize=12, va="top")
    axes[1, 1].text(0.0, 0.45, "Question for you:\nwhich channels changed most,\nand is it a shift, a gain change,\nor both?", fontsize=11, va="top")
    if a.source == "synthetic":
        fig.suptitle("SYNTHETIC DATA - pipeline test only, not a result", color="crimson", fontweight="bold")

    out = args.out / f"drift_{a.source}_S{args.subject}_M{args.movement}.png"
    fig.tight_layout(); fig.savefig(out, dpi=120)
    print(f"pattern correlation {a.name} vs {b.name}: {corr:.3f}")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
