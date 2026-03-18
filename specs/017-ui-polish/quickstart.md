# Quickstart: UI Polish & Visual Enhancement

## Implementation Order

1. **Create theme module** (`src/gui/theme.py`) — centralized color palette and ttk.Style configuration
2. **Fix dialog sizing** — update Add Step dialog and all Step Editor dialog dimensions
3. **Add dialog centering** — helper function + apply to all Toplevel dialogs
4. **Apply theme to main window** — dark header, light panels, styled buttons
5. **Add step highlight animation** — color pulse on new step add
6. **Verify condition coloring** — ensure blue/yellow still works with new theme

## Key Design Decisions

1. **Theme module pattern**: All colors defined in one place (`theme.py`). Other GUI files import from it. This prevents color values scattered across multiple files.

2. **"clam" base theme**: Must switch from default OS theme to "clam" to enable full color customization. Do this once at app startup before any widgets are created.

3. **Center on screen, not parent**: Dialogs center on screen (not parent window) because coordinate-picking workflows need the dialog out of the way.

4. **Highlight respects condition colors**: When a new step is added under a Condition step's governance, the highlight animation must settle to the correct condition color (blue/yellow), not white. The `_apply_condition_coloring()` method already handles this — call it after the highlight timer fires.

## Integration Scenario

```text
User launches app
→ Theme module initializes "clam" theme with custom styles
→ Main window renders with dark title bar area, light panels
→ User clicks "Add Step"
→ Add Step dialog opens CENTERED on screen, sized to show all 11 buttons
→ User selects "Click"
→ Click Step Editor opens CENTERED, properly sized for coordinate fields
→ User clicks "Pick" to select coordinates
→ After picking, Step Editor returns CENTERED (not at pick location)
→ User saves the step
→ New step appears in workflow list with GREEN HIGHLIGHT for 500ms
→ Highlight fades to white (or blue/yellow if under a Condition)
→ User hovers over "Move Up" button
→ Button shows BLUE HOVER EFFECT
```

## Files Affected

| File | Change Type | Purpose |
|------|-------------|---------|
| `src/gui/theme.py` | NEW | Centralized theme colors and ttk.Style setup |
| `src/gui/app.py` | MODIFY | Apply theme at startup, style main window |
| `src/gui/step_editors.py` | MODIFY | Fix dialog sizes, add centering |
| `src/gui/workflow_panel.py` | MODIFY | Step highlight animation, themed listbox |
| `src/gui/excel_panel.py` | MODIFY | Apply themed styles to panel widgets |
| `src/gui/execution_panel.py` | MODIFY | Apply themed styles to panel widgets |
| `src/main.py` | MODIFY | Initialize theme before UI creation |
