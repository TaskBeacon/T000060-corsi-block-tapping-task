from __future__ import annotations

import hashlib
import random
from typing import Any


BLOCK_NAMES = tuple(f"block_{index}" for index in range(1, 10))


def _stable_seed(base_seed: int, *parts: object) -> int:
    payload = "|".join([str(base_seed), *(str(part) for part in parts)])
    digest = hashlib.blake2b(payload.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, byteorder="big", signed=False)


def _sequence(base_seed: int, *parts: object, length: int) -> list[str]:
    if not 1 <= int(length) <= len(BLOCK_NAMES):
        raise ValueError("Corsi sequences must contain between 1 and 9 unique blocks")
    rng = random.Random(_stable_seed(base_seed, *parts))
    return rng.sample(list(BLOCK_NAMES), k=int(length))


def build_sequence_pool(settings: Any) -> dict[str, dict[str, Any]]:
    """Preplan every practice and scored sequence from an independent seed."""
    directions = [str(value) for value in list(settings.directions)]
    start_length = int(settings.start_length)
    max_length = int(settings.max_length)
    attempts = int(settings.attempts_per_length)
    practice_trials = int(settings.practice_trials_per_direction)
    practice_length = int(settings.practice_sequence_length)
    seed = int(settings.sequence_seed)

    pool: dict[str, dict[str, Any]] = {}
    for direction in directions:
        practice = [
            _sequence(seed, direction, "practice", index, length=practice_length)
            for index in range(practice_trials)
        ]
        scored = {
            length: [
                _sequence(seed, direction, "scored", length, attempt, length=length)
                for attempt in range(attempts)
            ]
            for length in range(start_length, max_length + 1)
        }
        pool[direction] = {"practice": practice, "scored": scored}
    return pool


def resolve_direction_order(subject_id: object, directions: list[str], *, fixed: bool) -> list[str]:
    order = [str(direction) for direction in directions]
    if fixed or len(order) != 2:
        return order
    parity = _stable_seed(0, subject_id, "corsi_direction_order") % 2
    return order if parity == 0 else list(reversed(order))


def expected_response(sequence: list[str], direction: str) -> list[str]:
    if direction == "forward":
        return list(sequence)
    if direction == "backward":
        return list(reversed(sequence))
    raise ValueError(f"Unsupported Corsi direction: {direction}")


def get_board_stimuli(stim_bank, *, active_block: str | None = None, ready: bool = False) -> list:
    stimuli = [stim_bank.get(name) for name in BLOCK_NAMES]
    if active_block is not None:
        stimuli.append(stim_bank.get(f"active_{active_block}"))
    if ready:
        stimuli.append(stim_bank.get("ready_marker"))
    return stimuli


def summarize_session(rows: list[dict]) -> dict[str, Any]:
    scored = [row for row in rows if not bool(row.get("is_practice"))]
    correct = [row for row in scored if bool(row.get("correct"))]
    spans = {
        direction: max(
            [int(row.get("span_after", 0)) for row in scored if row.get("direction") == direction],
            default=0,
        )
        for direction in ("forward", "backward")
    }
    return {
        "scored_trials": len(scored),
        "accuracy": (len(correct) / len(scored)) if scored else 0.0,
        "forward_span": spans["forward"],
        "backward_span": spans["backward"],
        "timeouts": sum(bool(row.get("timed_out")) for row in scored),
    }
