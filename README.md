# Corsi Block-Tapping Task

| Field | Value |
|---|---|
| Name | Corsi Block-Tapping Task |
| Task ID | `T000060` |
| Variant | Computerized forward/backward span |
| Version | `v0.1.0` |
| Date Updated | 2026-07-12 |
| PsyFlow Version | `0.2.0` |
| PsychoPy Version | `2025.1.1` |
| Modality | Behavioral |
| Language | Chinese |
| Primary construct | Visuospatial short-term and working memory |
| Release | `v0.1.0` |

## 1. Task Overview

This task implements a computerized Corsi Block-Tapping Task based primarily on the eCorsi procedure. Nine identical square outlines occupy fixed irregular positions. A sequence of squares fills yellow one at a time, after which the participant reproduces the sequence by clicking the squares.

The forward condition requires the original order. The backward condition requires the reverse order. Each condition begins at sequence length 2 and uses two attempts per length. At least one correct attempt advances the span by one; two failures at the same length terminate that condition. Three length-3 practice trials precede each scored condition.

This is a research implementation. Deterministically generated no-repeat sequences support audit and replay, but the task does not claim clinical equivalence to unpublished or proprietary normative item sets.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

1. General instruction.
2. Forward and backward blocks in seeded counterbalanced order for human runs; fixed order for QA/simulation.
3. Direction-specific instruction and three practice trials.
4. Adaptive scored span trials from length 2 through a maximum of 9.
5. Direction summary, then final forward/backward span summary.

### Trial-Level Flow

| Phase | Duration | Participant-facing event |
|---|---:|---|
| Sequence ready | 500 ms | Nine idle yellow outlines on black |
| Sequence flash | 500 ms/item | One square fills yellow |
| Inter-flash gap | 500 ms | Idle board; produces 1000 ms flash onset interval |
| Recall | Self-paced, 30 s max | Blue ready marker and clickable board; selected squares light briefly |
| Practice feedback | 750 ms | Correct/incorrect text, practice only |
| Intertrial interval | 500 ms | Blank black screen |

The blue ready marker first appears with the final flash and remains visible during recall. Pointer input is accepted only after the final flash has completed.

### Controller Logic

`CorsiSpanController` owns only adaptive span progression. It presents both attempts at the current length, advances when at least one is correct, and stops after two failures or successful completion of length 9. Trial identity, phase data, trigger timing, pointer hit testing, and response timestamps remain PsyFlow-owned.

### Other Logic

Every core trial factor is preplanned by `build_sequence_pool()`. The sequence RNG uses a stable task seed and never shares state with timing. Sequences contain no repeated block through length 9. Human direction order is deterministically counterbalanced from subject ID.

## 3. Configuration Summary

### a. Subject Info

| Parameter | Value |
|---|---|
| Subject ID | Three digits |
| Input | Mouse or touch-compatible pointer |

### b. Window Settings

| Parameter | Value |
|---|---|
| Window | 1280 x 800 px |
| Background | Black |
| Units | Pixels |

### c. Stimuli

| Stimulus | Definition |
|---|---|
| Board | Nine identical 90 x 90 px yellow square outlines at fixed irregular coordinates |
| Active square | Yellow filled square at the same coordinate as its outline |
| Recall marker | Small blue circle in the upper-right |
| Text | Chinese, SimHei |

### d. Timing

| Parameter | Human profile |
|---|---:|
| Flash duration | 500 ms |
| Flash IOI | 1000 ms |
| Recall ceiling | 30 s |
| Attempts per length | 2 |
| Correct attempts required to advance | 1 |
| Sequence range | 2-9 |

QA and simulation profiles shorten timing and maximum span while preserving forward/backward rules, pointer-sequence semantics, practice feedback, adaptive advancement, and stopping behavior.

### e. Adaptive Controller

The focused controller stores only the current length, attempt count, correct attempts, span, and termination reason. It does not own trial identity, response capture, timing, or persistence.

### f. Triggers

| Event | Code |
|---|---:|
| Experiment start | 1 |
| Block start | 10 |
| Sequence ready | 20 |
| Sequence flash | 21 |
| Recall onset | 30 |
| Block selection | 31 |
| Recall complete | 32 |
| Recall timeout | 33 |
| Practice feedback | 40 |
| Trial ITI | 50 |
| Block end | 90 |
| Experiment end | 99 |

Run locally with:

```powershell
python main.py human
python main.py qa --config config/config_qa.yaml
python main.py sim --config config/config_scripted_sim.yaml
python main.py sim --config config/config_sampler_sim.yaml
```

## 4. Methods (for academic publication)

Participants completed a computerized Corsi Block-Tapping Task implemented with PsychoPy and PsyFlow. Nine identical yellow square outlines were displayed in fixed irregular positions on a black background. On each trial, squares filled yellow sequentially for 500 ms each with a 1000 ms onset-to-onset interval. A blue marker signaled the recall phase, during which participants selected the same squares using a pointer. In the forward block, participants reproduced the original order; in the backward block, they reproduced the reverse order. Each block began with three practice trials of length 3. Scored assessment began at length 2 with two trials per length. At least one correct sequence advanced the participant to the next length, while two incorrect sequences at one length terminated that block. Span was the longest sequence length successfully reproduced. Exact sequences, selections, first-tap latency, completion latency, accuracy, timeout status, and adaptive state were recorded.

## References

- Brunetti, R., Del Gatto, C., & Delogu, F. (2014). eCorsi: implementation and testing of the Corsi block-tapping task for digital tablets. *Frontiers in Psychology, 5*, 939. https://doi.org/10.3389/fpsyg.2014.00939
- Smyth, M. M., & Scholey, K. A. (1994). Interference in immediate spatial memory. *Memory & Cognition, 22*, 1-13. https://doi.org/10.3758/BF03202756
- Pickering, S. J., Gathercole, S. E., & Peaker, S. (1998). Verbal and visuospatial short-term memory in children. *Memory & Cognition, 26*, 1117-1126. https://doi.org/10.3758/BF03201189

Full evidence mappings are in `references/`.
