"""Regime M (Myerson): trusted mediator, transfers enforce truthful reports.

q = 5/6 and y = 20 are Myerson's solution for this example. Trade probability,
welfare and inefficiency are computed from q over the four type pairs and
checked against the published values in summary().

Each (seller_value, buyer_value) pair has mass 0.25:
    (0, 100)  surplus 100   efficient   trades w.p. 1
    (0,  20)  surplus  20   efficient   trades w.p. q   (marginal)
    (80, 100) surplus  20   efficient   trades w.p. q   (marginal)
    (80,  20) surplus -60   inefficient never trades
"""

from __future__ import annotations

from fractions import Fraction

from env.bilateral import TYPE_PROB

# Myerson's closed-form solution for this example
Q: Fraction = Fraction(5, 6)  # trade prob in the two surplus-20 marginal states
Y: int = 20  # transfer / handicap parameter

PAIR_MASS: float = TYPE_PROB * TYPE_PROB  # 0.25

# (seller_value, buyer_value) -> (surplus if traded, trade probability)
_STATES = {
    (0, 100): (100, 1.0),
    (0, 20): (20, float(Q)),
    (80, 100): (20, float(Q)),
    (80, 20): (-60, 0.0),
}


def trade_probability() -> float:
    """P(trade), summed over type pairs."""
    return sum(PAIR_MASS * prob for _, prob in _STATES.values())


def welfare() -> float:
    """Expected realized gains from trade."""
    return sum(PAIR_MASS * surplus * prob for surplus, prob in _STATES.values())


def ex_post_inefficiency() -> float:
    """Probability that an efficient trade doesn't happen."""
    return sum(
        PAIR_MASS * (1.0 - prob)
        for surplus, prob in _STATES.values()
        if surplus > 0
    )


def summary() -> dict:
    tp = trade_probability()
    w = welfare()
    ineff = ex_post_inefficiency()
    # check against the published values
    assert abs(tp - 2 / 3) < 1e-9, tp
    assert abs(w - 100 / 3) < 1e-9, w
    assert abs(ineff - 1 / 12) < 1e-9, ineff
    return {
        "q": "5/6",
        "q_float": float(Q),
        "y": Y,
        "trade_probability": tp,
        "welfare": w,
        "inefficiency": ineff,
    }
