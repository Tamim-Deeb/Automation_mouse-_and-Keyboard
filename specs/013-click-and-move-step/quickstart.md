# Quickstart: Click And Move Step

## Test Scenario 1: Drag a Desktop Icon

1. Launch the application
2. Click "Add Step" → select "Click And Move"
3. In the step editor, click "Pick" next to the Start coordinates
4. Click on a desktop icon — verify Start X and Start Y are populated
5. Click "Pick" next to the End coordinates
6. Click on a folder on the desktop — verify End X and End Y are populated
7. Click "Save"
8. Verify the workflow list shows: "Click And Move: (x1, y1) → (x2, y2)"
9. Click "Run" to execute the workflow
10. Verify the icon is dragged from start to end position

## Test Scenario 2: Manual Coordinate Entry

1. Add a new "Click And Move" step
2. Type `100` in Start X, `200` in Start Y
3. Type `300` in End X, `400` in End Y
4. Click "Save"
5. Verify the step saves with all four coordinates

## Test Scenario 3: Drag to Same Position

1. Add a "Click And Move" step with identical start and end coords (e.g., 500, 500 → 500, 500)
2. Click "Save" — should succeed (no validation error)
3. Run the workflow — mouse should click-hold-release at the same position

## Test Scenario 4: Validation — Missing Coordinates

1. Add a "Click And Move" step
2. Fill in only Start X and Start Y, leave End X and End Y empty
3. Click "Save"
4. Verify a validation error appears

## Test Scenario 5: Save and Reload

1. Create a workflow with a Click And Move step (e.g., 100, 200 → 300, 400)
2. Save the workflow to JSON
3. Close and reopen the application
4. Load the saved workflow
5. Verify the Click And Move step displays correctly with all four coordinates
6. Run the workflow and verify the drag executes correctly

## Test Scenario 6: Negative Coordinates (Multi-Monitor)

1. Add a "Click And Move" step
2. Type `-100` in Start X, `200` in Start Y
3. Type `300` in End X, `400` in End Y
4. Click "Save" — should succeed (negative values accepted)

## Test Scenario 7: Existing Steps Still Work

1. Create a workflow with a Click step, a Click And Move step, and a Wait step
2. Run the workflow
3. Verify all three step types execute correctly
