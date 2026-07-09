"""Regime L (Lancashire): no enforcer, the report is replaced by a costly
irreversible action taken under uncertainty.

The mechanism never sees a type. Each trader decides whether to pay a
commitment cost k before the outcome is known, and only the type that values
trade finds it worth paying.

Separation
----------
A trade happens only when both sides commit, at the midpoint of the two weak
values, COMMIT_PRICE = 50.

  weak seller  (value 0):   trade profit 50 - 0  = +50, realized w.p. 0.5
                            expected benefit of committing = 0.5 * 50 = 25
  strong seller(value 80):  trade profit 50 - 80 = -30  -> never commits
  weak buyer   (value 100): trade profit 100 - 50 = +50, expected benefit 25
  strong buyer (value 20):  trade profit 20 - 50 = -30  -> never commits

So a weak type commits iff k < COMMIT_THRESHOLD = 25, and a strong type never
commits since the trade loses it money. The figures use k = 2.

Welfare
-------
Only (0, 100) trades (surplus 100, mass 0.25). Every committer pays k whether
or not a trade happens: the weak seller commits with mass 0.5 and the weak
buyer with mass 0.5, so the expected cost is k.
"""

from __future__ import annotations

from env.bilateral import EFFICIENT_TRADE_MASS, TYPE_PROB

PAIR_MASS: float = TYPE_PROB * TYPE_PROB  # 0.25
COMMIT_PRICE: float = 50.0  # midpoint of the two weak values (0 and 100)
COMMIT_THRESHOLD: float = 25.0  # weak type's expected gain from committing
DEFAULT_K: float = 2.0

# Mass on which each side pays the cost when its weak type commits.
_WEAK_SELLER_MASS: float = 0.5  # states with seller value 0
_WEAK_BUYER_MASS: float = 0.5  # states with buyer value 100


def weak_type_commits(k: float = DEFAULT_K) -> bool:
    """Weak type commits iff its expected gain exceeds k."""
    return k < COMMIT_THRESHOLD


def strong_type_commits(k: float = DEFAULT_K) -> bool:
    """Strong type never commits (the trade loses it money)."""
    return False


def trade_probability(k: float = DEFAULT_K) -> float:
    """Only (0, 100) trades, and only if weak types commit."""
    return PAIR_MASS if weak_type_commits(k) else 0.0


def welfare(k: float = DEFAULT_K) -> float:
    """Gains from the (0, 100) trade minus the commitment cost."""
    if not weak_type_commits(k):
        return 0.0
    gross = PAIR_MASS * 100.0  # (0, 100) surplus 100
    burned = (_WEAK_SELLER_MASS + _WEAK_BUYER_MASS) * k
    return gross - burned


def ex_post_inefficiency(k: float = DEFAULT_K) -> float:
    """Probability that an efficient trade doesn't happen."""
    if not weak_type_commits(k):
        return EFFICIENT_TRADE_MASS  # 0.75, nobody commits
    # (0,20) and (80,100) fail because the strong side doesn't commit
    return PAIR_MASS + PAIR_MASS  # 0.5


def separation_holds(k: float) -> bool:
    """True iff the weak type commits and the strong type abstains at cost k."""
    return weak_type_commits(k) and not strong_type_commits(k)


def summary() -> dict:
    tp = trade_probability()
    w = welfare()
    ineff = ex_post_inefficiency()
    assert abs(tp - 0.25) < 1e-9, tp
    assert abs(w - 23.0) < 1e-9, w
    assert abs(ineff - 0.5) < 1e-9, ineff
    return {
        "k": DEFAULT_K,
        "trade_probability": tp,
        "welfare": w,
        "inefficiency": ineff,
    }
