from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    continue_key: str = "space"
    error_rate: float = 0.15
    timeout_rate: float = 0.03
    first_tap_rt_s: float = 0.18
    inter_tap_s: float = 0.12
    forced_error_trials: tuple[int, ...] | list[int] = ()
    forced_timeout_trials: tuple[int, ...] | list[int] = ()

    def __post_init__(self) -> None:
        self._rng: Any = None
        self._trial_modes: dict[str, str] = {}
        self._forced_errors = {str(value) for value in self.forced_error_trials}
        self._forced_timeouts = {str(value) for value in self.forced_timeout_trials}

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None
        self._trial_modes.clear()

    def _random(self) -> float:
        return float(self._rng.random())

    def act(self, obs: Observation) -> Action:
        if self._rng is None or not obs.valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "corsi_sampler", "outcome": "wait"})

        if obs.phase != "recall":
            key = self.continue_key if self.continue_key in obs.valid_keys else obs.valid_keys[0]
            return Action(key=key, rt_s=0.10, meta={"source": "corsi_sampler", "outcome": "continue"})

        trial_key = str(obs.trial_id)
        selection_index = int(obs.task_factors.get("selection_index", 0))
        expected = [str(value) for value in list(obs.task_factors.get("expected_response", []))]
        if trial_key not in self._trial_modes:
            if trial_key in self._forced_timeouts:
                self._trial_modes[trial_key] = "timeout"
            elif trial_key in self._forced_errors:
                self._trial_modes[trial_key] = "error"
            else:
                roll = self._random()
                if roll < float(self.timeout_rate):
                    self._trial_modes[trial_key] = "timeout"
                elif roll < float(self.timeout_rate) + float(self.error_rate):
                    self._trial_modes[trial_key] = "error"
                else:
                    self._trial_modes[trial_key] = "correct"

        mode = self._trial_modes[trial_key]
        if mode == "timeout" or selection_index >= len(expected):
            return Action(key=None, rt_s=None, meta={"source": "corsi_sampler", "outcome": mode})

        key = expected[selection_index]
        if mode == "error" and selection_index == 0:
            alternatives = [candidate for candidate in obs.valid_keys if candidate != key]
            if alternatives:
                key = str(alternatives[0])
        rt_s = float(self.first_tap_rt_s) + selection_index * float(self.inter_tap_s)
        return Action(key=key, rt_s=rt_s, meta={"source": "corsi_sampler", "outcome": mode})
