# Data Model: Custom Hotkey Input

## Entities

### WorkflowStep (existing — no schema change)

The `params` dict for a `PRESS_HOTKEY` step stores the hotkey as a string:

| Field   | Type   | Description                                                        |
|---------|--------|--------------------------------------------------------------------|
| hotkey  | string | Key combination string. Predefined (e.g., "Escape", "Ctrl+A") or custom (e.g., "ctrl+f1", "ctrl+shift+f1", "f5") |

**Validation rules**:
- `hotkey` must be a non-empty string
- For predefined hotkeys: must match a `Hotkey` enum value
- For custom hotkeys: must contain at least a key name; modifier(s) are optional
- All custom values normalized to lowercase

**Storage format**: JSON via existing `WorkflowSerializer`

```json
{
  "type": "press_hotkey",
  "order": 3,
  "params": {
    "hotkey": "ctrl+f1"
  }
}
```

## Relationships

- `WorkflowStep.params["hotkey"]` → checked against `Hotkey` enum first; if no match, treated as custom hotkey string
- Custom hotkeys bypass the `SUPPORTED_HOTKEYS` dict in `KeyboardAutomation` and are executed directly via pyautogui
