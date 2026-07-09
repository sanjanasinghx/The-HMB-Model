"""Fictitious play: keep counts of the opponent's type and best-respond.

Against a fixed honest opponent this just estimates the opponent's type
frequencies, so the estimated payoff of lying goes to 45 and of honesty to 30.
"""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List


class FictitiousPlay:
    """Belief-based best-response learner over a small opponent type space."""

    def __init__(self, opponent_values: Iterable[int]) -> None:
        # Laplace prior: start every count at 1
        self._counts: Dict[int, int] = {v: 1 for v in opponent_values}

    def observe(self, opponent_value: int) -> None:
        """Record one opponent type draw."""
        self._counts[opponent_value] += 1

    def beliefs(self) -> Dict[int, float]:
        """Empirical distribution over opponent types."""
        total = sum(self._counts.values())
        return {v: c / total for v, c in self._counts.items()}

    def expected_value(
        self, action: int, payoff_fn: Callable[[int, int], float]
    ) -> float:
        """Expected payoff of `action` under the current belief over the opponent."""
        beliefs = self.beliefs()
        return sum(p * payoff_fn(action, v) for v, p in beliefs.items())

    def best_action(
        self, actions: Iterable[int], payoff_fn: Callable[[int, int], float]
    ) -> int:
        """Greedy best response given current beliefs."""
        actions = list(actions)
        return max(actions, key=lambda a: self.expected_value(a, payoff_fn))

    def value_trajectory(
        self,
        actions: List[int],
        payoff_fn: Callable[[int, int], float],
        opponent_samples: Iterable[int],
    ) -> Dict[int, List[float]]:
        """Estimated value of each action after every opponent draw (plotted in fig1)."""
        history: Dict[int, List[float]] = {a: [] for a in actions}
        for opponent_value in opponent_samples:
            self.observe(opponent_value)
            for a in actions:
                history[a].append(self.expected_value(a, payoff_fn))
        return history
