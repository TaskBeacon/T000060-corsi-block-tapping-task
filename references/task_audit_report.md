# Task Audit Report

Task: `T000060-corsi-block-tapping-task`

Verdict: no critical or serious findings after repair.

## Findings Repaired

- `[Moderate]` Moved participant-facing forward/backward labels from `main.py` into all four config profiles.
- `[Moderate]` Added deterministic QA error and timeout trials so responder coverage exercises correct, incorrect, timeout, advancement, and stopping semantics.
- `[Low]` Updated stimulus evidence mapping to record the blue ready marker on the final encoding flash.
- `[Serious]` Corrected the shared pointer-sequence timeout contract so a zero-selection timeout records generic `response=None` while preserving `responses=[]` for ordered detail.

## PsyFlow Ownership

| Concern | Owner | Audit result |
|---|---|---|
| Trial ID | PsyFlow `next_trial_id()` | Pass |
| Condition schedule | Documented custom adaptive sequence plan | Pass; static labels cannot express performance-dependent span |
| Randomness | Stable task seed, independent from timing | Pass |
| Response capture | PsyFlow `StimUnit.capture_pointer_sequence()` | Pass |
| Trigger emission | StimUnit trigger runtime; lifecycle events in `main.py` | Pass |
| Timing/deadline | Config plus StimUnit | Pass |
| Phase data/context | `set_trial_context()` plus `to_dict()` | Pass |
| Stimulus construction | Config/StimBank plus focused board helper | Pass |
| Responder integration | Standard runtime responder seam | Pass |

## Checks Run

- `check_task_standard.py`: pass.
- `taps_utils.validate`: pass after extending the response contract to accept pointer-sequence windows.
- `psyflow-qa`: pass.
- Scripted simulation: pass; deterministic incorrect/stopping path.
- Sampler simulation: pass; mixed correct/incorrect adaptive path.
- PsyFlow unit suite: 83 passed.

## Residual Risk

- Manual pointer behavior depends on PsychoPy device handling and is visually checked in QA; browser pointer parity is verified separately during `task-py2js`.
- The generated no-repeat sequence pool is a documented research adaptation and is not a clinical normative item set.
