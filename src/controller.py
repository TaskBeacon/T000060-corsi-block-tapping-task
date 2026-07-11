from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CorsiSpanController:
    """Advance or stop a Corsi span block after two attempts per length."""

    direction: str
    start_length: int
    max_length: int
    attempts_per_length: int
    correct_to_advance: int

    def __post_init__(self) -> None:
        self.current_length = int(self.start_length)
        self.attempt_index = 0
        self.correct_at_length = 0
        self.span = 0
        self.finished = False
        self.termination_reason = "running"

        if self.direction not in {"forward", "backward"}:
            raise ValueError(f"Unsupported Corsi direction: {self.direction}")
        if self.start_length < 1 or self.max_length < self.start_length:
            raise ValueError("Invalid Corsi sequence-length bounds")
        if self.attempts_per_length < 1:
            raise ValueError("attempts_per_length must be positive")
        if not 1 <= self.correct_to_advance <= self.attempts_per_length:
            raise ValueError("correct_to_advance must fit within attempts_per_length")

    def make_condition(self, sequence: list[str], *, block_id: str) -> dict:
        if self.finished:
            raise RuntimeError("Cannot request a condition from a finished span controller")
        if len(sequence) != self.current_length:
            raise ValueError("Sequence length does not match controller state")
        return {
            "direction": self.direction,
            "sequence_length": self.current_length,
            "sequence": list(sequence),
            "attempt_index": self.attempt_index + 1,
            "is_practice": False,
            "block_id": block_id,
        }

    def record(self, correct: bool) -> None:
        if self.finished:
            raise RuntimeError("Cannot update a finished span controller")

        self.attempt_index += 1
        self.correct_at_length += int(bool(correct))
        if self.attempt_index < self.attempts_per_length:
            return

        if self.correct_at_length >= self.correct_to_advance:
            self.span = self.current_length
            if self.current_length >= self.max_length:
                self.finished = True
                self.termination_reason = "maximum_span_reached"
                return
            self.current_length += 1
            self.attempt_index = 0
            self.correct_at_length = 0
            return

        self.finished = True
        self.termination_reason = "failed_level"

    def snapshot(self) -> dict:
        return {
            "direction": self.direction,
            "current_length": self.current_length,
            "attempt_index": self.attempt_index,
            "correct_at_length": self.correct_at_length,
            "span": self.span,
            "finished": self.finished,
            "termination_reason": self.termination_reason,
        }
