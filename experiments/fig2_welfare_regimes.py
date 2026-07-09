"""fig2: welfare by regime, with the first-best line.

M = 33.33, L = 23.00, H = 0.00, first best = 35. The gap between M and first
best is expected: even Myerson's mechanism leaves 1/12 of efficient trades
undone. Numbers come from the regime modules.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt

from env.bilateral import first_best_gains
from regimes import mediator_M, noenforcer_H, opaque_L
from experiments.plotting import PALETTE, apply_style, finalize


def make_figure(figures_dir: str) -> dict:
    apply_style()

    welfare_M = mediator_M.welfare()
    welfare_L = opaque_L.welfare()
    welfare_H = noenforcer_H.welfare()
    first_best = first_best_gains()

    labels = [
        "M\nmediator\n(enforced)",
        "L\nopaque\nirreversible action",
        "H\nno enforcer\n(cheap talk)",
    ]
    values = [welfare_M, welfare_L, welfare_H]
    colors = [PALETTE["M"], PALETTE["L"], PALETTE["H"]]

    fig, ax = plt.subplots()
    bars = ax.bar(range(3), values, color=colors, width=0.62)

    ax.axhline(first_best, ls="--", lw=1.2, color=PALETTE["reference"])
    ax.text(
        2.5,
        first_best,
        f"first best {first_best:.0f}",
        va="bottom",
        ha="right",
        fontsize=9,
        color=PALETTE["reference"],
    )

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.4,
            f"{value:.2f}",
            ha="center",
            va="bottom",
        )

    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 37)
    ax.set_title("Fig 2 - welfare by enforcement regime")
    ax.set_ylabel("expected gains from trade")

    finalize(
        fig,
        os.path.join(figures_dir, "fig2_welfare_regimes.png"),
        "Enforcement works (M), removing it breaks IC (H), "
        "costly action recovers about two thirds of the gains (L).",
    )

    return {
        "welfare_M": welfare_M,
        "welfare_L": welfare_L,
        "welfare_H": welfare_H,
        "first_best": first_best,
    }
