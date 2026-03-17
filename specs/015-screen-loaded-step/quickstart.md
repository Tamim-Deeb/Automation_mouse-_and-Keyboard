# Quickstart: Screen Loaded Step

## Scenario 1: Screen Loads Successfully on First Try

**Goal**: Verify the step passes when text is immediately visible.

**Setup**:
1. Open a text editor with visible text
2. Build a workflow with:
   - **Screen Loaded** — start/end coordinates covering a word in the text editor, max tries 3
   - Click at (100, 200) — some next action
3. Run the workflow

**Expected Result**: The Screen Loaded step succeeds on the first attempt (clipboard has content after drag+copy). The workflow continues to the Click step immediately.

## Scenario 2: Screen Loads After Delay

**Goal**: Verify the retry mechanism works when content appears after a delay.

**Setup**:
1. Start with a blank/loading screen that will display text after ~2 seconds
2. Build a workflow with:
   - **Screen Loaded** — coordinates covering where text will appear, max tries 5
   - Type Text "success"
3. Run the workflow

**Expected Result**: The step retries 2-3 times (1 second each), then succeeds when text appears. The workflow continues to Type Text.

## Scenario 3: Max Tries Exceeded — Workflow Stops

**Goal**: Verify the workflow stops when the screen never loads.

**Setup**:
1. Point coordinates at an empty/blank area that will never have text
2. Build a workflow with:
   - **Screen Loaded** — coordinates over blank area, max tries 3
   - Click at (100, 200)
3. Run the workflow

**Expected Result**: The step retries 3 times (3 seconds total), then stops the workflow. The Click step never executes. Status shows the workflow was stopped.

## Scenario 4: Workflow Save/Load

**Goal**: Verify Screen Loaded step parameters persist correctly.

**Setup**:
1. Create a workflow with a Screen Loaded step (start: 100,200; end: 300,200; max tries: 5)
2. Save workflow as JSON
3. Close and reopen
4. Load the saved workflow

**Expected Result**: The Screen Loaded step appears with correct coordinates and max tries settings.
