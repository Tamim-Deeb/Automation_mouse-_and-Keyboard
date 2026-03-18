# Quickstart: Write To Excel Step

## Scenario 1: Mark Rows as Done

**Goal**: Process Excel rows and mark each as complete by writing "x" to the "Status" column.

**Setup**:
1. Load an Excel file with columns: Name, Email, Status
2. Build a workflow with steps:
   - Click at (100, 200) — navigate to target field
   - Type Text "processed"
   - **Write To Excel** — Column: "Status", Mode: "Mark Done (x)"
3. Run the workflow

**Expected Result**: After execution, each processed row has "x" in the Status column.

## Scenario 2: Copy and Store Data

**Goal**: Copy a value from an application field and store it in the Excel file.

**Setup**:
1. Load an Excel file with columns: ID, Name, Result
2. Build a workflow with steps:
   - Click at (300, 400) — click into a result field
   - Copy Field — selects all and copies to clipboard
   - **Write To Excel** — Column: "Result", Mode: "Paste Clipboard"
3. Run the workflow

**Expected Result**: After execution, each row's "Result" column contains the text that was copied from the application field.

## Scenario 3: Workflow Save/Load

**Goal**: Verify Write To Excel steps persist correctly.

**Setup**:
1. Create a workflow with a Write To Excel step (Column: "Done", Mode: "Mark Done")
2. Save workflow as JSON
3. Close and reopen
4. Load the saved workflow

**Expected Result**: The Write To Excel step appears with correct column and mode settings.
