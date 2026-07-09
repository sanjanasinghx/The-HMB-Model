"""Tabular Q-learning, used as a cross-check on fictitious play.

With a fixed honest opponent and a sample-average step size, Q converges to the
expected payoff of each action: Q[lie] -> 45, Q[honest] -> 30.
"""

from __future__ import annotations

from typing import Callable, Dict, List

import numpy as np


class QLearning:
    """Stateless-per-type tabular Q-learner with epsilon-greedy exploration."""

    def __init__(self, actions: List[int], seed: int = 0, epsilon: float = 0.2) -> None:
        self.actions = list(actions)
        self.epsilon = epsilon
        self._rng = np.random.default_rng(seed)
        self.q: Dict[int, float] = {a: 0.0 for a in self.actions}
        self._n: Dict[int, int] = {a: 0 for a in self.actions}

    def select(self) -> int:
        """Epsilon-greedy action choice."""
        if self._rng.random() < self.epsilon:
            return self.actions[int(self._rng.integers(len(self.actions)))]
        return max(self.actions, key=lambda a: self.q[a])

    def update(self, action: int, reward: float) -> None:
        """Sample-average update."""
        self._n[action] += 1
        alpha = 1.0 / self._n[action]
        self.q[action] += alpha * (reward - self.q[action])

    def learn(
        self,
        rounds: int,
        payoff_fn: Callable[[int, int], float],
        opponent_values: List[int],
    ) -> Dict[int, float]:
        """Learn against a fixed honest opponent and return Q."""
        for _ in range(rounds):
            action = self.select()
            # honest opponent, type drawn uniformly
            opponent_value = opponent_values[
                int(self._rng.integers(len(opponent_values)))
            ]
            reward = payoff_fn(action, opponent_value)
            self.update(action, reward)
        return dict(self.q)

    def best_action(self) -> int:
        return max(self.actions, key=lambda a: self.q[a])
