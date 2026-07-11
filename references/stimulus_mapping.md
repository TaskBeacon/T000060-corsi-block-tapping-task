# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `forward` | `instruction` | `instruction_forward` | Chinese instruction to tap the flashed blocks in the same order. | `W2133111582` | Procedure defines forward recall as tapping in the same serial order. | `psychopy_builtin` | `config/*.yaml` | Config-driven SimHei text. |
| `backward` | `instruction` | `instruction_backward` | Chinese instruction to tap the flashed blocks in reverse order. | `W2133111582` | Procedure defines backward recall from last flashed block to first. | `psychopy_builtin` | `config/*.yaml` | Config-driven SimHei text. |
| `forward`, `backward` | `sequence_ready` | `block_1` through `block_9` | Nine identical yellow square outlines on a black field. | `W2133111582` | Procedure describes a traditional nine-frame Corsi board on black. | `psychopy_builtin` | `config/*.yaml` | Stable irregular coordinates; no visible numbers. |
| `forward`, `backward` | `sequence_flash` | `block_1` through `block_9`, `active_block_1` through `active_block_9`, `ready_marker` | One square at a time fills yellow for 500 ms while the other outlines remain visible; the final flash also shows the blue ready marker. | `W2133111582` | Procedure specifies 500 ms yellow fills, a 1000 ms inter-onset interval, and a blue light appearing with the last flash. | `psychopy_builtin` | `config/*.yaml` | Active block shares geometry with its idle outline; marker appears only on the final flash and recall. |
| `forward`, `backward` | `sequence_gap` | `block_1` through `block_9` | The idle nine-outline board for 500 ms between flashes. | `W2133111582` | 500 ms flash with 1000 ms IOI implies a 500 ms non-highlight interval. | `psychopy_builtin` | `config/*.yaml` | Keeps board coordinates continuously available. |
| `forward`, `backward` | `recall` | `block_1` through `block_9`, `ready_marker` | Idle board plus a small blue upper-right marker; selected blocks briefly fill to acknowledge taps. | `W2133111582` | Apparatus and procedure describe the blue recall signal and blocks lighting when tapped. | `psychopy_builtin` | `config/*.yaml` | Pointer/touch hit regions match block geometry. |
| `forward`, `backward` | `practice_feedback` | `feedback_correct`, `feedback_incorrect` | Short Chinese correct/incorrect feedback. | `W2133111582` | eCorsi supports on-screen error feedback; task understanding is checked in practice. | `psychopy_builtin` | `config/*.yaml` | Practice only; scored trials omit trial feedback. |
| `forward`, `backward` | `trial_iti` | `blank` | Blank black screen. | `W2133111582` | No additional participant-facing content is specified between sequences. | `psychopy_builtin` | `config/*.yaml` | Duration is inferred and documented. |

## Layout Coordinates

All nine blocks use identical square size and an irregular spatial arrangement. Coordinates are normalized for the task window and are held constant in every phase. No square number or internal ID is participant-visible.
