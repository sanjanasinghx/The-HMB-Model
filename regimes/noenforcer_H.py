"""Regime H (Hurwicz): no enforcer, reports are cheap talk.

Reports are free, so the weak type claims strong (45 > 30): every seller reports
80 and every buyer reports 20. Trade needs buyer_report > seller_report, and
20 > 80 never holds, so nothing trades. The numbers are computed by running the
pooled reports through split_the_difference.
"""

from __future__ import annotations

from env.bilateral import (
    BUYER_VALUES,
    EFFICIENT_TRADE_MASS,
    LYING_SELLER_REPORT,
    SELLER_VALUES,
    TYPE_PROB,
    split_the_difference,
)

# Everyone claims strong.
_SELLER_POOLED_REPORT = LYING_SELLER_REPORT  # 80
_BUYER_POOLED_REPORT = BUYER_VALUES[1]  # 20 (strong buyer value)


def trade_probability() -> float:
    """Run the pooled reports through the mechanism for every true state."""
    total = 0.0
    for _s in SELLER_VALUES:
        for _b in BUYER_VALUES:
            trade, _ = split_the_difference(
                _SELLER_POOLED_REPORT, _BUYER_POOLED_REPORT
            )
            if trade:
                total += TYPE_PROB * TYPE_PROB
    return total


def welfare() -> float:
    """Realized gains from trade (zero, since nothing trades)."""
    total = 0.0
    for s in SELLER_VALUES:
        for b in BUYER_VALUES:
            trade, _ = split_the_difference(
                _SELLER_POOLED_REPORT, _BUYER_POOLED_REPORT
            )
            if trade and b > s:
                total += TYPE_PROB * TYPE_PROB * (b - s)
    return total


def ex_post_inefficiency() -> float:
    """No efficient trade happens, so this is the whole efficient mass."""
    return EFFICIENT_TRADE_MASS  # 0.75


def summary() -> dict:
    tp = trade_probability()
    w = welfare()
    ineff = ex_post_inefficiency()
    assert tp == 0.0, tp
    assert w == 0.0, w
    assert abs(ineff - 0.75) < 1e-9, ineff
    return {
        "trade_probability": tp,
        "welfare": w,
        "inefficiency": ineff,
    }
