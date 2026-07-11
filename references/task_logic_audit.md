# Task Logic Audit

## 1. Paradigm Intent

- Task: Corsi Block-Tapping Task, computerized forward and backward span.
- Primary construct: visuospatial short-term memory (forward) and visuospatial working-memory manipulation (backward).
- Manipulated factors: recall direction (`forward`, `backward`) and adaptively increasing sequence length (2 through 9).
- Dependent measures: maximum span by direction, exact-sequence accuracy, first-tap latency, completion latency, selected block sequence, and stopping level.
- Key citations: Brunetti et al. (2014; `W2133111582`) is the canonical computerized protocol. Smyth and Scholey (1994; `W2024648041`) and Pickering et al. (1998; `W1972939642`) support construct interpretation. Owen et al. (1996; `W2165302691`) is construct evidence only and contributes no trial parameters.

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: two scored blocks, forward and backward, with three practice trials before each scored block.
- Trials per block: adaptive. Each scored direction starts at length 2 and presents two sequences at each length. At least one correct sequence advances to the next length; two failures at one length terminate that direction. The maximum is length 9.
- Randomization/counterbalancing: human mode counterbalances direction order from a seeded subject assignment; QA and simulation use a fixed forward-then-backward order. Sequence lists are generated before runtime from a stable task seed, contain no repeated block within sequences up to length 9, and are independent of timing.
- Condition weight policy: not applicable. Adaptive span trials cannot be represented by static weighted labels.
- Condition generation method: custom preplanned sequence generator plus a focused span controller. Built-in `BlockUnit.generate_conditions(...)` cannot determine the next sequence length because progression depends on prior trial accuracy. Each generated condition passed to `run_trial.py` is a dictionary containing `direction`, `sequence_length`, `sequence`, `attempt_index`, `is_practice`, and `block_id`.
- Runtime-generated trial values: no core factor is randomly generated in `run_trial.py`. Trial identity comes from PsyFlow. The controller only consumes scored accuracy and decides advance/stop according to the documented rule.

### Trial State Machine

1. `sequence_ready`
   - Onset trigger: `sequence_ready`.
   - Stimuli shown: the nine idle square outlines on black for 500 ms.
   - Valid responses: none.
   - Timeout behavior: advances automatically.
   - Next state: first `sequence_flash`.
2. `sequence_flash` and `sequence_gap`, repeated across items
   - Onset trigger: `sequence_flash` for each highlighted item.
   - Stimuli shown: all nine outlines; the current square is filled yellow for 500 ms, followed by the idle board for 500 ms. This yields a 1000 ms inter-onset interval.
   - Valid responses: none; premature clicks are ignored because recall is closed.
   - Timeout behavior: advances automatically through the preplanned sequence.
   - Next state: another flash/gap; the final flash includes the blue ready marker and transitions directly to `recall` without a post-final gap.
3. `recall`
   - Onset trigger: `recall_onset`.
   - Stimuli shown: nine idle squares and a small blue ready marker in the upper-right. Each accepted square briefly fills to acknowledge input.
   - Valid responses: pointer/touch activation inside one of the nine squares; exactly `sequence_length` accepted selections.
   - Timeout behavior: after the configured 30 s maximum, the partial response is scored incorrect and `recall_timeout` is emitted.
   - Next state: `practice_feedback` for practice trials, otherwise `trial_iti`.
4. `practice_feedback` (practice only)
   - Onset trigger: `feedback_onset`.
   - Stimuli shown: Chinese correct/incorrect feedback for 750 ms.
   - Valid responses: none.
   - Timeout behavior: advances automatically.
   - Next state: `trial_iti`.
5. `trial_iti`
   - Onset trigger: `trial_iti`.
   - Stimuli shown: blank black screen for 500 ms.
   - Valid responses: none.
   - Timeout behavior: advances automatically.
   - Next state: next adaptive trial or block summary.

## 3. Condition Semantics

- Condition ID: `forward`.
  - Participant-facing meaning: reproduce the flashed locations in the same order.
  - Concrete stimulus realization: an irregular nine-square board; yellow flashes followed by pointer/touch recall.
  - Outcome rules: selected sequence must exactly equal the presented sequence.
- Condition ID: `backward`.
  - Participant-facing meaning: reproduce the flashed locations in reverse order.
  - Concrete stimulus realization: the same board and flash sequence; recall target is the reversed sequence.
  - Outcome rules: selected sequence must exactly equal `reversed(presented_sequence)`.
- Participant-facing text source: all instructions, block labels, ready prompts, and feedback text are defined in `config/*.yaml`. Board geometry and colors are also config-defined.
- Auditability: runtime code receives only preplanned condition dictionaries and resolves named config stimuli; no internal condition token is displayed directly.
- Localization strategy: participant-facing strings and fonts can be replaced in config without modifying Python code.

## 4. Response and Scoring Rules

- Response mapping: each pointer/touch selection maps to one of nine configured square IDs; selection order is retained.
- Response source: target geometry comes from config and response collection uses a reusable public PsyFlow pointer-sequence primitive because keyboard capture cannot represent block tapping.
- Missing-response policy: timeout or fewer than the required number of selections is incorrect; partial selections remain in the audit data.
- Correctness logic: forward requires exact serial equality; backward requires exact equality to the reversed presented sequence.
- Reward/penalty updates: none.
- Running metrics: attempts and correct count per length, current length, forward/backward span, first-tap latency, completion latency, and block termination reason.

## 5. Stimulus Layout Plan

- Screen name: Corsi board during encoding and recall.
- Stimulus IDs shown together: `block_1` through `block_9`; `ready_marker` appears only during recall.
- Layout anchors: nine non-grid-aligned normalized positions spanning approximately 70% of screen width and 65% of screen height. The ready marker sits at `(0.82, 0.76)` and does not overlap any block.
- Size/spacing: each square is 0.13 height units with a minimum center spacing greater than 0.22; the marker diameter is 0.035. All coordinates are stable across phases.
- Readability/overlap checks: QA screenshots and `task_flow.png` must show all nine squares fully separated at the configured 1280 x 800 window and in the browser responsive frame.
- Rationale: reproduces the irregular, identical-block Corsi board and keeps spatial location as the only item identity available to participants.

## 6. Trigger Plan

- `experiment_start`: 1
- `block_start`: 10
- `sequence_ready`: 20
- `sequence_flash`: 21
- `recall_onset`: 30
- `block_select`: 31
- `recall_complete`: 32
- `recall_timeout`: 33
- `feedback_onset`: 40
- `trial_iti`: 50
- `block_end`: 90
- `experiment_end`: 99

Individual block selections share `block_select`; selected block IDs and click timestamps are retained in the stage data.

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: one explicit mode-aware flow. It constructs preplanned sequence pools, runs practice, then drives one adaptive direction block at a time.
- `utils.py` used: yes.
- Exact purpose: deterministic nonrepeating sequence generation, direction-order counterbalancing, and pure sequence-scoring helpers.
- Custom controller used: yes, narrowly scoped to the two-attempt span progression rule. Static BlockUnit scheduling cannot express performance-dependent stopping and advancement.
- PsyFlow framework extension: a reusable pointer-sequence response primitive is required because existing `capture_response` is keyboard-only. It owns pointer polling, target hit testing, response timestamps, timeout, triggers, and stage data; task code only supplies configured targets and expected selection count.
- Legacy/backward-compatibility fallback logic required: no.

## 8. Inference Log

- Decision: use the eCorsi default of two scored trials per sequence length and require one correct to advance.
  - Why inference was required: the article describes selectable ratios but identifies two trials as the standardized default; the exact study call does not restate the UI setting in one sentence.
  - Citation-supported rationale: Brunetti et al. (2014), apparatus Span Sequence Mode and procedure sections.
- Decision: use a 30 s recall ceiling.
  - Why inference was required: eCorsi records cumulative response time but does not report a hard response deadline.
  - Citation-supported rationale: a generous ceiling preserves self-paced tapping while preventing an unbounded runtime; timeout is not treated as a real response.
- Decision: generate deterministic nonrepeating sequences rather than claim equivalence to proprietary or unavailable standardized item lists.
  - Why inference was required: the source states that default Kessels sequences are implemented but does not print the complete item set in the article text.
  - Citation-supported rationale: Brunetti et al. (2014) explicitly permits randomly generated no-repeat sequences through length 9. The README must state that this is a research implementation and not a clinical normative replacement.
- Decision: present forward before backward in fixed QA/simulation order and counterbalance in human mode.
  - Why inference was required: the paper counterbalanced order between participants but does not prescribe an assignment algorithm.
  - Citation-supported rationale: deterministic parity assignment preserves counterbalancing and reproducibility.

## Contract Note

- Participant-facing labels, instructions, options, geometry, colors, and timing are config-defined.
- `src/run_trial.py` may orchestrate phases and score a supplied sequence but must not generate sequences, poll pointer devices manually, or hardcode localized text.
