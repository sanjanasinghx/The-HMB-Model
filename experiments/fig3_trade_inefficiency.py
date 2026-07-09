"""fig3: trade probability and ex-post inefficiency by regime.

Ex-post inefficiency = probability that a positive-gain trade doesn't happen
(not the fraction of surplus lost). M should sit on the 1/12 floor, the minimum
for any IC, IR, budget-balanced mechanism in this example.
"""

from __future__ import annotations

import os

import numpy as np
import matplotlib.pyplot as plt

from regimes import mediator_M, noenforcer_H, opaque_L
from experiments.plotting import PALETTE, apply_style, finalize

MYERSON_FLOOR: float = 1.0 / 12.0


def make_figure(figures_dir: str) -> dict:
    apply_style()

    M = mediator_M.summary()
    H = noenforcer_H.summary()
    L = opaque_L.summary()

    trade_probability = {
        "M": M["trade_probability"],
        "L": L["trade_probability"],
        "H": H["trade_probability"],
    }
    inefficiency = {
        "M": M["inefficiency"],
        "L": L["inefficiency"],
        "H": H["inefficiency"],
    }

    groups = ["M mediator", "L opaque", "H no enforcer"]
    keys = ["M", "L", "H"]
    xpos = np.arange(3)
    width = 0.38

    fig, ax = plt.subplots()
    bars_tp = ax.bar(
        xpos - width / 2,
        [trade_probability[k] for k in keys],
        width=width,
        color=PALETTE["M"],
        label="trade probability",
    )
    bars_ineff = ax.bar(
        xpos + width / 2,
        [inefficiency[k] for k in keys],
        width=width,
        color=PALETTE["H"],
        label="ex-post inefficiency",
    )

    ax.axhline(MYERSON_FLOOR, ls="--", lw=1.2, color=PALETTE["reference"])
    ax.text(
        2.5,
        MYERSON_FLOOR + 0.012,
        "Myerson floor 1/12",
        ha="right",
        va="bottom",
        fontsize=9,
        color=PALETTE["reference"],
    )

    for bars in (bars_tp, bars_ineff):
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.015,
                f"{bar.get_height():.2f}",
                ha="center",
                va="bottom",
                fontsize=11,
            )

    ax.set_xticks(xpos)
    ax.set_xticklabels(groups)
    ax.set_ylim(0, 1.0)
    ax.set_title("Fig 3 - trade probability and ex-post inefficiency")
    ax.set_ylabel("probability")
    ax.legend(loc="upper center", ncol=2)

    finalize(
        fig,
        os.path.join(figures_dir, "fig3_trade_inefficiency.png"),
        "M sits on the 1/12 floor, L partly recovers, "
        "H trades nothing.",
    )

    return {
        "trade_probability": trade_probability,
        "inefficiency": inefficiency,
        "floor": MYERSON_FLOOR,
    }
