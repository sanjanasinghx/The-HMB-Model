"""Checks against the closed form: 45/30, both learners, the M/H/L numbers,
first best 35, and the commitment-cost sweep over (0, 25)."""

from __future__ import annotations

import numpy as np

from agents.fictitious_play import FictitiousPlay
from agents.q_learning import QLearning
from env.bilateral import (
    BUYER_VALUES,
    HONEST_SELLER_REPORT,
    LYING_SELLER_REPORT,
    first_best_gains,
    seller_payoff_fn,
    weak_seller_expected_profit,
)
from regimes import mediator_M, noenforcer_H, opaque_L
from regimes.opaque_L import COMMIT_THRESHOLD, separation_holds


def test_temptation_numbers():
    assert weak_seller_expected_profit(HONEST_SELLER_REPORT) == 30
    assert weak_seller_expected_profit(LYING_SELLER_REPORT) == 45


def test_first_best():
    assert first_best_gains() == 35


def test_fictitious_play_converges():
    payoff = seller_payoff_fn()
    actions = [HONEST_SELLER_REPORT, LYING_SELLER_REPORT]
    rng = np.random.default_rng(0)
    samples = [BUYER_VALUES[int(i)] for i in rng.integers(len(BUYER_VALUES), size=6000)]
    hist = FictitiousPlay(BUYER_VALUES).value_trajectory(actions, payoff, samples)
    assert abs(hist[LYING_SELLER_REPORT][-1] - 45) < 1.0
    assert abs(hist[HONEST_SELLER_REPORT][-1] - 30) < 1.0


def test_q_learning_agrees():
    payoff = seller_payoff_fn()
    actions = [HONEST_SELLER_REPORT, LYING_SELLER_REPORT]
    q = QLearning(actions=actions, seed=0).learn(20000, payoff, list(BUYER_VALUES))
    assert abs(q[LYING_SELLER_REPORT] - 45) < 1.0
    assert abs(q[HONEST_SELLER_REPORT] - 30) < 1.0
    assert q[LYING_SELLER_REPORT] > q[HONEST_SELLER_REPORT]


def test_regime_M():
    m = mediator_M.summary()
    assert m["q"] == "5/6"
    assert abs(m["q_float"] - 5 / 6) < 1e-9
    assert m["y"] == 20
    assert abs(m["trade_probability"] - 2 / 3) < 1e-9
    assert abs(m["welfare"] - 100 / 3) < 1e-9
    assert abs(m["inefficiency"] - 1 / 12) < 1e-9


def test_regime_H():
    h = noenforcer_H.summary()
    assert h["trade_probability"] == 0.0
    assert h["welfare"] == 0.0
    assert abs(h["inefficiency"] - 0.75) < 1e-9


def test_regime_L():
    ell = opaque_L.summary()
    assert abs(ell["trade_probability"] - 0.25) < 1e-9
    assert abs(ell["welfare"] - 23.0) < 1e-9
    assert abs(ell["inefficiency"] - 0.5) < 1e-9


def test_welfare_ordering():
    assert (
        mediator_M.summary()["welfare"]
        > opaque_L.summary()["welfare"]
        > noenforcer_H.summary()["welfare"]
    )


def test_separation_across_open_interval():
    # weak commits, strong abstains, for k in (0, 25)
    for k in np.linspace(0.5, 24.5, 49):
        assert separation_holds(float(k)), k


def test_mechanism_collapses_at_threshold():
    # at k = 25 the weak type stops committing
    assert not separation_holds(COMMIT_THRESHOLD)
    assert opaque_L.welfare(COMMIT_THRESHOLD) == 0.0
    assert opaque_L.trade_probability(COMMIT_THRESHOLD) == 0.0
