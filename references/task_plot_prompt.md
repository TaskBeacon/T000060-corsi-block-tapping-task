Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Corsi Block-Tapping Task
Construct: visuospatial short-term memory / working memory
Rows/conditions:
- Forward: reproduce highlighted blocks in the same serial order.
- Backward: reproduce highlighted blocks in reverse serial order.

Timeline phases:
- Forward: Ready (500 ms; no response; black participant screen with nine identical yellow square outlines in an irregular layout) -> Encode (three representative yellow block highlights, each 500 ms, with 500 ms outline-only gaps) -> Recall (30 s max; small blue circle in upper-right; mouse pointer selects the same three locations in the same order) -> Feedback (750 ms; Practice only; simple correct check or incorrect cross) -> Blank (500 ms; black screen).
- Backward: Ready (500 ms; no response; same nine-outline irregular board) -> Encode (three representative yellow block highlights, each 500 ms, with 500 ms outline-only gaps) -> Recall (30 s max; small blue circle in upper-right; mouse pointer selects the same three locations in reverse order) -> Feedback (750 ms; Practice only; simple correct check or incorrect cross) -> Blank (500 ms; black screen).

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per condition or representative trial type.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows the visible stimulus or feedback, not internal variable names.
- The Corsi board must show exactly nine square outlines in the same irregular positions in every board snapshot.
- Show three tiny numbered sequence indicators outside the participant screen to clarify encoding order; do not put numbers inside the blocks.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 15-18% of the image. This band is reserved for a fixed title, `Construct: ...` subtitle, and TaskBeacon logo lockup that will be added after generation.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Use a black field inside every board snapshot, with yellow square outlines and yellow filled highlights.
- The blue ready marker appears only on the Recall snapshot and the final encoded highlight if represented.
- Forward recall must visibly repeat the same three selected positions in order; Backward recall must visibly select them in reverse order.
- Practice feedback is explicitly marked `Practice only`.
- If a detail is unknown, omit it rather than guessing.
- Preserve these exact terms where used: Forward, Backward, Ready, Encode, Recall, Practice only, Blank, 500 ms, 500 ms gap, 30 s max, Same order, Reverse order.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
