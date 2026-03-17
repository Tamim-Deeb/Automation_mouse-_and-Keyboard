# Quickstart: Custom Hotkey Input

## Test Scenario 1: Custom Single-Modifier Hotkey (Ctrl+F1)

1. Launch the application
2. Click "Add Step" → select "Press Hotkey"
3. In the step editor, leave the dropdown unchanged
4. In the "Modifier (optional)" box, type: `ctrl`
5. In the "Key" box, type: `f1`
6. Click "Save"
7. Verify the workflow list shows: "Press Hotkey: ctrl+f1"
8. Open a text editor or application that responds to Ctrl+F1
9. Click "Run" to execute the workflow
10. Verify that Ctrl+F1 was pressed in the target application

## Test Scenario 2: Custom Multi-Modifier Hotkey (Ctrl+Shift+F1)

1. Add a new "Press Hotkey" step
2. In the "Modifier (optional)" box, type: `ctrl+shift`
3. In the "Key" box, type: `f1`
4. Click "Save"
5. Verify the workflow list shows: "Press Hotkey: ctrl+shift+f1"
6. Run the workflow and verify the key combination is pressed

## Test Scenario 3: Key-Only (No Modifier)

1. Add a new "Press Hotkey" step
2. Leave the "Modifier (optional)" box empty
3. In the "Key" box, type: `f5`
4. Click "Save"
5. Verify the workflow list shows: "Press Hotkey: f5"
6. Open a browser, run the workflow, verify the page refreshes (F5)

## Test Scenario 4: Predefined Dropdown Still Works

1. Add a new "Press Hotkey" step
2. Select "Ctrl+A" from the dropdown
3. Leave both custom input boxes empty
4. Click "Save"
5. Verify the step saves as "Ctrl+A" (predefined)
6. Run the workflow and verify Ctrl+A is pressed

## Test Scenario 5: Custom Input Overrides Dropdown

1. Add a new "Press Hotkey" step
2. Select "Ctrl+A" from the dropdown
3. In the "Key" box, type: `f5`
4. Click "Save"
5. Verify the step saves as "f5" (custom input takes priority)

## Test Scenario 6: Save and Reload

1. Complete Test Scenario 1 (create a Ctrl+F1 step)
2. Save the workflow to a JSON file
3. Close and reopen the application
4. Load the saved workflow
5. Verify the Ctrl+F1 step displays correctly
6. Run the workflow and verify it executes correctly

## Test Scenario 7: Validation — Empty Key

1. Add a new "Press Hotkey" step
2. Type "ctrl" in the modifier box but leave the Key box empty
3. Clear the dropdown selection (if possible) or leave it
4. Click "Save"
5. Verify a validation error appears (modifier alone is not valid for custom input)
