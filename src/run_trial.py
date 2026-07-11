from __future__ import annotations

from functools import partial

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import BLOCK_NAMES, expected_response, get_board_stimuli


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Present one preplanned Corsi sequence and collect ordered block taps."""
    trial_id = next_trial_id()
    direction = str(condition["direction"])
    sequence = [str(value) for value in condition["sequence"]]
    sequence_length = int(condition["sequence_length"])
    attempt_index = int(condition["attempt_index"])
    is_practice = bool(condition["is_practice"])
    block_id_value = str(block_id or condition.get("block_id") or direction)
    condition_id = f"{direction}_len{sequence_length}_attempt{attempt_index}"
    target_response = expected_response(sequence, direction)
    timing = dict(settings.timing)
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    trial_data = {
        "trial_id": int(trial_id),
        "block_id": block_id_value,
        "block_idx": int(block_idx or 0),
        "condition": direction,
        "condition_id": condition_id,
        "direction": direction,
        "sequence_length": sequence_length,
        "attempt_index": attempt_index,
        "is_practice": is_practice,
        "presented_sequence": list(sequence),
        "expected_response": list(target_response),
        "selected_sequence": [],
        "correct": False,
        "timed_out": False,
    }

    common_factors = {
        "direction": direction,
        "sequence_length": sequence_length,
        "attempt_index": attempt_index,
        "is_practice": is_practice,
    }

    ready = make_unit(unit_label="sequence_ready").add_stim(get_board_stimuli(stim_bank))
    set_trial_context(
        ready,
        trial_id=trial_id,
        phase="sequence_ready",
        deadline_s=float(timing["sequence_ready_duration"]),
        valid_keys=[],
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors=common_factors,
        stim_id="corsi_board_idle",
    )
    ready.show(
        duration=float(timing["sequence_ready_duration"]),
        onset_trigger=settings.triggers.get("sequence_ready"),
    ).to_dict(trial_data)

    flash_duration = float(timing["flash_duration"])
    gap_duration = max(0.0, float(timing["flash_ioi"]) - flash_duration)
    for item_index, block_name in enumerate(sequence):
        is_last = item_index == len(sequence) - 1
        flash = make_unit(unit_label=f"sequence_flash_{item_index + 1:02d}").add_stim(
            get_board_stimuli(stim_bank, active_block=block_name, ready=is_last)
        )
        set_trial_context(
            flash,
            trial_id=trial_id,
            phase="sequence_flash",
            deadline_s=flash_duration,
            valid_keys=[],
            block_id=block_id_value,
            condition_id=condition_id,
            task_factors={**common_factors, "serial_position": item_index + 1, "block_name": block_name},
            stim_id=f"active_{block_name}",
        )
        flash.show(
            duration=flash_duration,
            onset_trigger=settings.triggers.get("sequence_flash"),
        ).to_dict(trial_data)

        if not is_last and gap_duration > 0:
            gap = make_unit(unit_label=f"sequence_gap_{item_index + 1:02d}").add_stim(
                get_board_stimuli(stim_bank)
            )
            set_trial_context(
                gap,
                trial_id=trial_id,
                phase="sequence_gap",
                deadline_s=gap_duration,
                valid_keys=[],
                block_id=block_id_value,
                condition_id=condition_id,
                task_factors={**common_factors, "after_serial_position": item_index + 1},
                stim_id="corsi_board_idle",
            )
            gap.show(duration=gap_duration).to_dict(trial_data)

    targets = {name: stim_bank.get(name) for name in BLOCK_NAMES}
    highlights = {name: stim_bank.get(f"active_{name}") for name in BLOCK_NAMES}
    recall_timeout = float(timing["recall_timeout"])
    recall = make_unit(unit_label="recall").add_stim(get_board_stimuli(stim_bank, ready=True))
    set_trial_context(
        recall,
        trial_id=trial_id,
        phase="recall",
        deadline_s=recall_timeout,
        valid_keys=list(BLOCK_NAMES),
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors={**common_factors, "expected_response": list(target_response)},
        stim_id="corsi_board_recall",
    )
    recall.capture_pointer_sequence(
        targets=targets,
        max_selections=sequence_length,
        duration=recall_timeout,
        onset_trigger=settings.triggers.get("recall_onset"),
        selection_trigger=settings.triggers.get("block_select"),
        complete_trigger=settings.triggers.get("recall_complete"),
        timeout_trigger=settings.triggers.get("recall_timeout"),
        highlight_targets=highlights,
    ).to_dict(trial_data)

    selected = list(recall.get_state("responses", []) or [])
    completed = bool(recall.get_state("completed", False))
    correct = completed and selected == target_response
    trial_data.update(
        selected_sequence=selected,
        response_times=list(recall.get_state("response_times", []) or []),
        first_tap_latency=recall.get_state("first_rt", None),
        completion_latency=recall.get_state("rt", None),
        timed_out=not completed,
        correct=correct,
        outcome="correct" if correct else ("timeout" if not completed else "incorrect"),
    )

    if is_practice:
        feedback_id = "feedback_correct" if correct else "feedback_incorrect"
        feedback = make_unit(unit_label="practice_feedback").add_stim(stim_bank.get(feedback_id))
        set_trial_context(
            feedback,
            trial_id=trial_id,
            phase="practice_feedback",
            deadline_s=float(timing["feedback_duration"]),
            valid_keys=[],
            block_id=block_id_value,
            condition_id=condition_id,
            task_factors={**common_factors, "correct": correct},
            stim_id=feedback_id,
        )
        feedback.show(
            duration=float(timing["feedback_duration"]),
            onset_trigger=settings.triggers.get("feedback_onset"),
        ).to_dict(trial_data)

    iti = make_unit(unit_label="trial_iti").add_stim(stim_bank.get("blank"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="trial_iti",
        deadline_s=float(timing["iti_duration"]),
        valid_keys=[],
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors=common_factors,
        stim_id="blank",
    )
    iti.show(
        duration=float(timing["iti_duration"]),
        onset_trigger=settings.triggers.get("trial_iti"),
    ).to_dict(trial_data)
    return trial_data
