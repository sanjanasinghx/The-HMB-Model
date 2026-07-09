"""Regenerate every figure and write metrics.json.

Run from the repo root:  python experiments/run_all.py
"""

from __future__ import annotations

import json
import os
import sys

# make the repo root importable when run as a script
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from experiments import (  # noqa: E402
    fig1_validation,
    fig2_welfare_regimes,
    fig3_trade_inefficiency,
)
from regimes import mediator_M, noenforcer_H, opaque_L  # noqa: E402

SEED = 0


def main() -> None:
    print(f"[hurwicz-sim] seed = {SEED}")
    figures_dir = os.path.join(_ROOT, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    metrics: dict = {"seed": SEED}

    print("  building fig1_validation.png ...")
    metrics["fig1_validation"] = fig1_validation.make_figure(figures_dir, seed=SEED)
    print("  building fig2_welfare_regimes.png ...")
    metrics["fig2_welfare_regimes"] = fig2_welfare_regimes.make_figure(figures_dir)
    print("  building fig3_trade_inefficiency.png ...")
    metrics["fig3_trade_inefficiency"] = fig3_trade_inefficiency.make_figure(
        figures_dir
    )

    metrics["regime_M"] = mediator_M.summary()
    metrics["regime_H"] = noenforcer_H.summary()
    metrics["regime_L"] = opaque_L.summary()

    metrics_path = os.path.join(_ROOT, "results", "metrics.json")
    with open(metrics_path, "w") as fh:
        json.dump(metrics, fh, indent=2)

    _print_summary(metrics, figures_dir, metrics_path)


def _print_summary(metrics: dict, figures_dir: str, metrics_path: str) -> None:
    f1 = metrics["fig1_validation"]
    m = metrics["regime_M"]
    print("\n" + "=" * 66)
    print("SUMMARY  (learned vs analytic)")
    print("=" * 66)
    print(f"  weak seller, learned lie    = {f1['learned_lie']:.3f}   (analytic 45)")
    print(f"  weak seller, learned honest = {f1['learned_honest']:.3f}   (analytic 30)")
    print(f"  Q-learning   lie / honest   = {f1['q_lie']:.3f} / {f1['q_honest']:.3f}")
    print(
        f"  Myerson q                   = {m['q']}  ({m['q_float']:.4f}, analytic 5/6)"
    )
    print(f"  Myerson y                   = {m['y']}   (analytic 20)")
    print(f"  allocative inefficiency     = {m['inefficiency']:.5f}   (analytic 1/12)")
    print("-" * 66)
    print(
        "  welfare  M / L / H          = "
        f"{metrics['regime_M']['welfare']:.2f} / "
        f"{metrics['regime_L']['welfare']:.2f} / "
        f"{metrics['regime_H']['welfare']:.2f}"
    )
    print("-" * 66)
    print("  figures written:")
    for name in sorted(os.listdir(figures_dir)):
        if name.endswith(".png"):
            print(f"    - results/figures/{name}")
    print(f"  metrics: {os.path.relpath(metrics_path, _ROOT)}")
    print("=" * 66)


if __name__ == "__main__":
    main()
