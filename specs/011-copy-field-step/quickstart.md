# Quickstart: Copy Field Step

## How to Use

1. **Open the workflow builder** and click "Add Step"
2. **Select "Copy Field"** from the step type dropdown
3. **Save the step** — no parameters to configure
4. **Ensure a prior step focuses the target field** (e.g., a Click step on the input field)
5. **Run the workflow** — the Copy Field step will:
   - Clear the clipboard
   - Select all text in the focused field (Ctrl+A)
   - Copy the selected text (Ctrl+C)
6. The clipboard now contains the field's contents

## When to Use

- Capturing text from input fields during automation
- Extracting values from form fields for verification
- Any scenario where you need the contents of a focused text field on the clipboard

## Testing Checklist

- [ ] Add a Copy Field step to a workflow → step appears as "Copy Field" in the steps list
- [ ] Run workflow with a text field focused containing "Test123" → clipboard contains "Test123"
- [ ] Run workflow with an empty focused field → clipboard is empty
- [ ] Put stale data on clipboard, then run Copy Field on a field → stale data is replaced
- [ ] Save and reload a workflow containing a Copy Field step → step persists correctly
- [ ] Run in dry-run mode → step is logged but not executed
- [ ] Delete a Copy Field step from workflow → step is removed cleanly
