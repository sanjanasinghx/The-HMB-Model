"""Shared plot style."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PALETTE = {
    "M": "#4C72B0",  # mediator (blue)
    "H": "#C44E52",  # no enforcer (red)
    "L": "#55A868",  # opaque action (green)
    "analytic": "#8172B3",  # closed form (purple)
    "learned": "#CCB974",  # learned (gold)
    "reference": "#555555",  # dashed reference lines (gray)
    "irreversible": "#4C72B0",
    "reversible": "#C44E52",
}

DPI = 150


def apply_style() -> None:
    """Set rcParams for all figures."""
    plt.rcParams.update(
        {
            "figure.figsize": (8.0, 5.0),
            "figure.dpi": 110,
            "savefig.dpi": DPI,
            "font.size": 13,
            "axes.titlesize": 15,
            "axes.labelsize": 13,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.7,
            "legend.frameon": False,
            "lines.linewidth": 2.2,
        }
    )


def caption(fig, text: str) -> None:
    """One-line caption at the bottom of the figure."""
    fig.text(
        0.5,
        0.005,
        text,
        ha="center",
        va="bottom",
        fontsize=10,
        color=PALETTE["reference"],
        style="italic",
    )


def finalize(fig, path: str, cap: str) -> None:
    """Add caption and save."""
    caption(fig, cap)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path)
    plt.close(fig)
