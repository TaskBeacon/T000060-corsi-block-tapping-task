from __future__ import annotations

from contextlib import nullcontext
from pathlib import Path
from typing import Any

import pandas as pd
from psychopy import core

from psyflow import (
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    reset_trial_counter,
    runtime_context,
    set_trial_context,
)

from src import (
    CorsiSpanController,
    build_sequence_pool,
    resolve_direction_order,
    run_trial,
    summarize_session,
)


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _show_continue(
    *,
    label: str,
    stim_id: str,
    win,
    kb,
    stim_bank,
    trigger_runtime,
    text_values: dict[str, Any] | None = None,
    terminate: bool = False,
) -> None:
    unit = StimUnit(label, win, kb, runtime=trigger_runtime)
    stimulus = stim_bank.get_and_format(stim_id, **text_values) if text_values else stim_bank.get(stim_id)
    set_trial_context(
        unit,
        trial_id=label,
        phase=label,
        deadline_s=None,
        valid_keys=["space"],
        block_id=label,
        condition_id=label,
        task_factors=dict(text_values or {}),
        stim_id=stim_id,
    )
    unit.add_stim(stimulus).wait_and_continue(keys=["space"], terminate=terminate)


def run(options: TaskRunOptions) -> None:
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    runtime_ctx = None
    output_dir = None
    runtime_scope = nullcontext()
    if options.mode in {"qa", "sim"}:
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "human":
            subject_data = SubInfo(cfg["subform_config"]).collect()
        else:
            participant = str(getattr(getattr(runtime_ctx, "session", None), "participant_id", options.mode))
            subject_data = {"subject_id": participant}

        settings = TaskSettings.from_dict(cfg["task_config"])
        settings.timing = dict(cfg.get("raw", {}).get("timing", {}) or {})
        settings.triggers = cfg["trigger_config"]
        settings.add_subinfo(subject_data)
        if output_dir is not None:
            settings.save_path = str(output_dir)
        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        trigger_runtime = initialize_triggers(mock=True) if options.mode in {"qa", "sim"} else initialize_triggers(cfg)
        win, kb = initialize_exp(settings)
        reset_trial_counter()
        stim_bank = StimBank(win, cfg["stim_config"]).preload_all()
        settings.save_to_json()

        trigger_runtime.send(settings.triggers.get("experiment_start"))
        _show_continue(
            label="instruction",
            stim_id="instruction_general",
            win=win,
            kb=kb,
            stim_bank=stim_bank,
            trigger_runtime=trigger_runtime,
        )

        directions = [str(value) for value in list(settings.directions)]
        direction_order = resolve_direction_order(
            subject_data.get("subject_id", "unknown"),
            directions,
            fixed=options.mode in {"qa", "sim"},
        )
        sequence_pool = build_sequence_pool(settings)
        all_rows: list[dict[str, Any]] = []

        for block_idx, direction in enumerate(direction_order):
            block_id = f"block_{block_idx + 1:02d}_{direction}"
            trigger_runtime.send(settings.triggers.get("block_start"))
            _show_continue(
                label=f"{direction}_instruction",
                stim_id=f"instruction_{direction}",
                win=win,
                kb=kb,
                stim_bank=stim_bank,
                trigger_runtime=trigger_runtime,
            )

            for practice_index, sequence in enumerate(sequence_pool[direction]["practice"], start=1):
                condition = {
                    "direction": direction,
                    "sequence_length": int(settings.practice_sequence_length),
                    "sequence": list(sequence),
                    "attempt_index": practice_index,
                    "is_practice": True,
                    "block_id": block_id,
                }
                all_rows.append(
                    run_trial(
                        win=win,
                        kb=kb,
                        settings=settings,
                        condition=condition,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        block_id=block_id,
                        block_idx=block_idx,
                    )
                )

            controller = CorsiSpanController(
                direction=direction,
                start_length=int(settings.start_length),
                max_length=int(settings.max_length),
                attempts_per_length=int(settings.attempts_per_length),
                correct_to_advance=int(settings.correct_to_advance),
            )
            while not controller.finished:
                sequence = sequence_pool[direction]["scored"][controller.current_length][controller.attempt_index]
                row = run_trial(
                    win=win,
                    kb=kb,
                    settings=settings,
                    condition=controller.make_condition(sequence, block_id=block_id),
                    stim_bank=stim_bank,
                    trigger_runtime=trigger_runtime,
                    block_id=block_id,
                    block_idx=block_idx,
                )
                controller.record(bool(row["correct"]))
                row.update({f"controller_{key}": value for key, value in controller.snapshot().items()})
                row["span_after"] = controller.span
                all_rows.append(row)

            trigger_runtime.send(settings.triggers.get("block_end"))
            _show_continue(
                label="block_summary",
                stim_id="block_summary",
                win=win,
                kb=kb,
                stim_bank=stim_bank,
                trigger_runtime=trigger_runtime,
                text_values={
                    "direction_label": dict(settings.direction_labels)[direction],
                    "span": controller.span,
                },
            )

        summary = summarize_session(all_rows)
        _show_continue(
            label="goodbye",
            stim_id="good_bye",
            win=win,
            kb=kb,
            stim_bank=stim_bank,
            trigger_runtime=trigger_runtime,
            text_values=summary,
            terminate=True,
        )
        trigger_runtime.send(settings.triggers.get("experiment_end"))
        pd.DataFrame(all_rows).to_csv(settings.res_file, index=False)
        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run the Corsi Block-Tapping Task in human, QA, or simulation mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
