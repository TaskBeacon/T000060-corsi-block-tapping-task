# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `directions` | `task.directions` | `[forward, backward]` | `W2133111582` | Procedure: participants completed forward and backward conditions, counterbalanced between subjects. | `direct` | Forward and backward are scored separately. |
| `start_length` | `task.start_length` | `2` | `W2133111582` | Procedure: span assessment starts from sequences of two items. | `direct` | Applies independently to each direction. |
| `max_length` | `task.max_length` | `9` | `W2133111582` | Nine-block board; free generation avoids repeats through length nine. | `direct` | Prevents within-sequence repeats. |
| `attempts_per_length` | `task.attempts_per_length` | `2` | `W2133111582` | Apparatus: two trials per length selects the standardized default span mode. | `direct` | One correct trial advances. |
| `correct_to_advance` | `task.correct_to_advance` | `1` | `W2133111582` | Procedure: at least one correctly reproduced sequence advances to the next length. | `direct` | Two failures terminate the direction. |
| `practice_trials` | `task.practice_trials_per_direction` | `3` | `W2133111582` | Procedure: understanding was verified with three practice trials of three blocks. | `direct` | Repeated before each direction to teach the rule. |
| `practice_length` | `task.practice_sequence_length` | `3` | `W2133111582` | Procedure: three practice trials were three blocks long. | `direct` | Practice feedback is enabled. |
| `flash_duration` | `timing.flash_duration` | `0.5 s` | `W2133111582` | Procedure: each square filled yellow for 500 ms. | `direct` | Encoding display only. |
| `flash_ioi` | `timing.flash_ioi` | `1.0 s` | `W2133111582` | Procedure: inter-onset interval was 1000 ms. | `direct` | Implemented as 500 ms flash plus 500 ms idle gap. |
| `ready_duration` | `timing.sequence_ready_duration` | `0.5 s` | `W2133111582` | No pre-sequence duration is specified. | `inferred` | Brief stable-board preview before encoding. |
| `recall_timeout` | `timing.recall_timeout` | `30 s` | `W2133111582` | Recall is self-paced and cumulative response time is recorded; no ceiling is reported. | `inferred` | Generous safety ceiling, not a speed manipulation. |
| `feedback_duration` | `timing.feedback_duration` | `0.75 s` | `W2133111582` | On-screen error feedback is configurable; exact duration is not reported. | `inferred` | Used only in practice. |
| `iti_duration` | `timing.iti_duration` | `0.5 s` | `W2133111582` | Intertrial blank duration is not reported. | `inferred` | Separates trials without changing encoding IOI. |
| `board_count` | `task.block_count` | `9` | `W2133111582` | Apparatus and procedure show nine square frames. | `direct` | All blocks are visually identical. |
| `board_style` | `stimuli.block_*` | `yellow outlines on black; yellow fill when active` | `W2133111582` | Procedure: nine yellow square frames on black; flashes fill a frame in yellow. | `direct` | Coordinates are normalized for display portability. |
| `ready_marker` | `stimuli.ready_marker` | `small blue circle, upper-right` | `W2133111582` | Apparatus/procedure: a little blue circle/light signals that recall may begin. | `direct` | Does not overlap any block. |
| `sequence_policy` | `task.sequence_seed` | `deterministic, no repeated block within a sequence` | `W2133111582` | Free Trial Mode randomly generates sequences while avoiding repeats through length nine. | `adapted` | Deterministic seeds make QA and replay auditable. |
| `response_mode` | `task.response_mode` | `pointer/touch block selection` | `W2133111582` | Participants reproduce by tapping squares; computerized variants may use mouse clicks. | `direct` | Keyboard substitutions are not used. |

## Interpretation Boundary

This implementation follows the computerized research procedure and does not claim clinical equivalence to a proprietary or unpublished standardized item set. All deviations are explicitly marked `adapted` or `inferred`.
