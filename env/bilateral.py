"""Bilateral-trade model from Myerson's 2007 Nobel lecture.

Seller value in {0, 80}, buyer value in {100, 20}, each equally likely. Each
trader only knows their own value.

  weak   = seller value 0, buyer value 100 (willing to trade at more prices)
  strong = seller value 80, buyer value 20

Split-the-difference: trade if buyer value > seller value, at the midpoint of
the two reported values. Honesty isn't an equilibrium here: the weak type gets
45 by lying vs 30 by being honest (checked in tests/test_validation.py).
"""

from __future__ import annotations

from typing import Callable, Tuple

SELLER_VALUES: Tuple[int, int] = (0, 80)  # weak seller values 0, strong values 80
BUYER_VALUES: Tuple[int, int] = (100, 20)  # weak buyer values 100, strong values 20
TYPE_PROB: float = 0.5  # each value equally likely

# The two reports the seller can send.
HONEST_SELLER_REPORT: int = 0  # weak seller telling the truth
LYING_SELLER_REPORT: int = 80  # weak seller claiming to be the strong type


def is_weak_seller(value: int) -> bool:
    """Weak seller has value 0 (willing to trade at more prices)."""
    return value == 0


def is_weak_buyer(value: int) -> bool:
    """Weak buyer has value 100 (willing to trade at more prices)."""
    return value == 100


def split_the_difference(
    seller_report: float, buyer_report: float
) -> Tuple[bool, float]:
    """Trade iff buyer_report > seller_report, at the midpoint price.

    Only sees reports, never true values.
    """
    trade = buyer_report > seller_report
    price = (seller_report + buyer_report) / 2.0 if trade else 0.0
    return trade, price


def seller_profit(
    seller_value: float, seller_report: float, buyer_report: float
) -> float:
    """Seller profit: price minus true value if a trade happens."""
    trade, price = split_the_difference(seller_report, buyer_report)
    return (price - seller_value) if trade else 0.0


def buyer_profit(
    buyer_value: float, seller_report: float, buyer_report: float
) -> float:
    """Buyer profit: true value minus price if a trade happens."""
    trade, price = split_the_difference(seller_report, buyer_report)
    return (buyer_value - price) if trade else 0.0


def weak_seller_expected_profit(seller_report: int) -> float:
    """Expected profit of the weak seller (value 0) against an honest buyer.

    Honest report (0):  0.5*50 + 0.5*10 = 30
    Lying  report (80): 0.5*90 + 0.5*0  = 45
    (Myerson lecture, Fig 2.)
    """
    return TYPE_PROB * seller_profit(
        0, seller_report, BUYER_VALUES[0]
    ) + TYPE_PROB * seller_profit(0, seller_report, BUYER_VALUES[1])


def seller_payoff_fn() -> Callable[[int, int], float]:
    """(report, buyer_value) -> weak seller's profit, used by the learners."""
    return lambda report, buyer_value: seller_profit(0, report, buyer_value)


def first_best_gains() -> float:
    """Expected gains if every efficient trade happened.

    (0,100): 100, (0,20): 20, (80,100): 20, (80,20): none
    E[gain] = 0.25*(100 + 20 + 20 + 0) = 35
    """
    total = 0.0
    for s in SELLER_VALUES:
        for b in BUYER_VALUES:
            if b > s:
                total += TYPE_PROB * TYPE_PROB * (b - s)
    return total


# Mass of states where trade is efficient: (0,100), (0,20), (80,100) = 0.75
EFFICIENT_TRADE_MASS: float = sum(
    TYPE_PROB * TYPE_PROB for s in SELLER_VALUES for b in BUYER_VALUES if b > s
)
