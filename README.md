# The HMB Model (hurwicz-sim)

Code for an economics paper on enforcement and incentive compatibility. It uses
Roger Myerson's bilateral-trade example (2007 Nobel lecture) as the base model.
Two tabular learners (fictitious play and Q-learning) check that the model is
coded correctly in fig1: they recover the closed-form payoffs (lie 45, honest
30) from experience. The three enforcement regimes (M, H, L) are then worked out
analytically on the same model; the learners don't play them. The world is the
same in every regime and only the enforcement rule changes.

## Summary

A seller and a buyer each privately know their own value. A "split-the-difference"
plan would be efficient if everyone told the truth, but the weak type does better
by lying: 45 by lying versus 30 by being honest. With a trusted mediator and
enforceable transfers (regime M) the incentive-efficient mechanism gets close to
efficient. Without an enforcer, where reports are cheap talk (regime H),
incentive compatibility breaks: everyone claims to be strong, nothing trades and
the gains go to zero. If the cheap report is replaced with a costly, irreversible
action taken under uncertainty (regime L), incentive compatibility partly comes
back, because only the type that actually values trade thinks the commitment is
worth paying for.

## Regimes

| Regime | Enforcement rule | What changes | Predicted behavior |
| --- | --- | --- | --- |
| M (Myerson) | Trusted mediator; type reports enforced by transfers | Reports are binding | Truthful; `q = 5/6`, `y = 20`, inefficiency `1/12` (the known answer) |
| H (Hurwicz) | No enforcer; reports are cheap talk | Reports cost nothing | Weak type lies (45 > 30); everyone claims strong; trade goes to 0 |
| L (Lancashire) | No enforcer; report replaced by a costly irreversible action under uncertainty | Type is never passed to the mechanism; the cost is sunk before the outcome | Types separate through the action; most of the gain is recovered |

M and H are named after two of the 2007 mechanism-design Nobel laureates,
Myerson and Hurwicz. "Lancashire" (L) is just a codename for the new
action-based regime, not a laureate. The third 2007 laureate, Eric Maskin, works
on implementation theory, which isn't what's modelled here.

## Caveat

A simulation is a fully specified probability space, so it can't capture true
Knightian uncertainty. Instead it uses a proxy with two parts: (1) the mechanism
never gets the agent's type as an input, and (2) the cost in regime L is
irreversible and paid before uncertainty resolves. Within this setup,
action-based enforcement recovers incentive compatibility that direct-report
enforcement loses.

`tests/test_validation.py` sweeps the commitment cost k across (0, 25) and checks
that the weak type commits and the strong type abstains throughout, and that the
weak type stops committing once k reaches 25. The figures use k = 2.

## How to run

```bash
pip install -r requirements.txt
python experiments/run_all.py     # regenerates all three figures + results/metrics.json
pytest                            # checks 45/30, q=5/6, y=20, floor=1/12
```

Everything is seeded (`seed = 0`) and the seed is printed at the start of each
run. The learners are tabular because with two types per side a table is exact.

## Figures

- `fig1_validation.png`: the weak type's learned payoff converging to 45 (lie)
  and 30 (honest), with dashed analytic reference lines. If these don't land on
  45 and 30, the model is wrong.
- `fig2_welfare_regimes.png`: expected gains from trade under M, H and L.
  H loses all of the gains and L gets back roughly two thirds.
- `fig3_trade_inefficiency.png`: trade probability and ex-post inefficiency by
  regime, with the dashed `1/12` Myerson floor that M sits on.

## Link to the Saito consensus work

- Seller / buyer values = an agent's valuation of settling now vs later.
- Mediator + transfers (M) = protocol-level security guarantees.
- Removing the enforcer (H) = the permissionless setting, where reports are
  cheap talk and nothing binds them.
- Irreversible action (L) = proof-of-work / forgone continuation value: a sunk
  cost that makes commitment credible.

## Layout

```
hurwicz-sim/
  env/bilateral.py            payoffs, type draws, split-the-difference plan
  regimes/mediator_M.py       regime M: incentive-efficient mechanism (q=5/6, y=20)
  regimes/noenforcer_H.py     regime H: cheap talk, IC collapse
  regimes/opaque_L.py         regime L: costly irreversible action
  agents/fictitious_play.py   main learner
  agents/q_learning.py        second learner, as a cross-check
  experiments/run_all.py      regenerates every figure
  experiments/fig1..fig3.py   one figure each
  experiments/plotting.py     shared plot style
  results/figures/            PNGs
  results/metrics.json        learned vs analytic numbers
  tests/test_validation.py    validation tests
  README.md  requirements.txt  .gitignore
```
