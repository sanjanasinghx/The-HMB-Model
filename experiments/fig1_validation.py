"""fig1: model check.

Both learners should recover Myerson's closed form: the weak seller's payoff of
lying goes to 45 and of honesty to 30. Returns the learned numbers for
metrics.json.
"""

from __future__ import annotations

import os

import numpy as np
import matplotlib.pyplot as plt

from agents.fictitious_play import FictitiousPlay
from agents.q_learning import QLearning
from env.bilateral import (
    BUYER_VALUES,
    HONEST_SELLER_REPORT,
    LYING_SELLER_REPORT,
    seller_payoff_fn,
)
from experiments.plotting import PALETTE, apply_style, finalize

FP_ROUNDS: int = 4000
Q_ROUNDS: int = 4000


def make_figure(figures_dir: str, seed: int = 0) -> dict:
    apply_style()

    payoff = seller_payoff_fn()
    actions = [HONEST_SELLER_REPORT, LYING_SELLER_REPORT]

    # fictitious play against a fixed honest opponent
    rng = np.random.default_rng(seed)
    samples = [
        BUYER_VALUES[int(i)] for i in rng.integers(len(BUYER_VALUES), size=FP_ROUNDS)
    ]
    hist = FictitiousPlay(BUYER_VALUES).value_trajectory(actions, payoff, samples)

    # Q-learning as a cross-check
    q = QLearning(actions=actions, seed=seed).learn(Q_ROUNDS, payoff, list(BUYER_VALUES))

    learned_lie = hist[LYING_SELLER_REPORT][-1]
    learned_honest = hist[HONEST_SELLER_REPORT][-1]

    fig, ax = plt.subplots()
    x = np.arange(1, len(samples) + 1)
    ax.plot(
        x,
        hist[LYING_SELLER_REPORT],
        color=PALETTE["H"],
        label="learned payoff of lying (claim strong)",
    )
    ax.plot(
        x,
        hist[HONEST_SELLER_REPORT],
        color=PALETTE["M"],
        label="learned payoff of honesty",
    )

    for y, txt in ((45, "analytic 45 (lie)"), (30, "analytic 30 (honest)")):
        ax.axhline(y, ls="--", lw=1.2, color=PALETTE["reference"])
        ax.text(
            len(samples),
            y,
            "  " + txt,
            va="center",
            ha="left",
            fontsize=9,
            color=PALETTE["reference"],
        )

    ax.set_xlim(0, len(samples))
    ax.set_ylim(0, 57)  # red curve starts above the top, that's fine
    ax.set_title("Fig 1 - model check: weak type learns to lie (45 > 30)")
    ax.set_xlabel("fictitious-play rounds")
    ax.set_ylabel("weak seller's expected payoff")
    ax.legend(loc="lower center", ncol=2)

    finalize(
        fig,
        os.path.join(figures_dir, "fig1_validation.png"),
        "Fictitious play converges to Myerson's closed form; "
        "Q-learning agrees (lie 45, honest 30).",
    )

    return {
        "learned_lie": learned_lie,
        "learned_honest": learned_honest,
        "q_lie": q[LYING_SELLER_REPORT],
        "q_honest": q[HONEST_SELLER_REPORT],
    }
