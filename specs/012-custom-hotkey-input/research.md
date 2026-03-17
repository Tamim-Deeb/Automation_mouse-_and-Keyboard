# Research: Custom Hotkey Input

## Decision 1: Custom Hotkey Execution Strategy

**Decision**: Parse the custom hotkey string by splitting on "+" and pass all parts to `pyautogui.hotkey()`.

**Rationale**: pyautogui.hotkey() already accepts variable arguments (e.g., `pyautogui.hotkey('ctrl', 'shift', 'f1')`). Splitting the stored string "ctrl+shift+f1" on "+" produces exactly the argument list needed. No wrapper or mapping table required.

**Alternatives considered**:
- Building a lookup table of custom hotkeys → Unnecessary complexity; pyautogui handles arbitrary key names directly.
- Using pynput for custom hotkeys → Inconsistent with existing automation layer (pyautogui); would require managing key press/release manually.

## Decision 2: Storage Format for Custom Hotkeys

**Decision**: Store custom hotkeys in the same `params["hotkey"]` field as predefined hotkeys, using lowercase "+" separated strings (e.g., "ctrl+f1").

**Rationale**: The existing serializer and workflow model already handle the `hotkey` param as a string. Custom values like "ctrl+f1" serialize identically to predefined values like "Ctrl+A". The execution handler differentiates by attempting Hotkey enum lookup first, falling back to custom string parsing.

**Alternatives considered**:
- Separate `custom_hotkey` param field → Would require changes to serializer, workflow panel display, and validation; unnecessary when a single field works.
- Storing modifier and key separately → Would complicate serialization and display for no benefit.

## Decision 3: Priority When Both Dropdown and Custom Fields Are Filled

**Decision**: Custom input (Key box has content) takes priority over dropdown selection.

**Rationale**: The user explicitly typed a custom combination, indicating intent to override the dropdown. This matches UX conventions where manual input overrides presets.
