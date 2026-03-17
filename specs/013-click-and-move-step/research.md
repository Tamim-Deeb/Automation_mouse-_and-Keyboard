# Research: Click And Move Step

## Decision 1: pyautogui Drag API

**Decision**: Use `pyautogui.mouseDown()` at start coords, `pyautogui.moveTo()` to end coords, then `pyautogui.mouseUp()` for the drag operation.

**Rationale**: This gives full control over the drag — click position, move path, and release. pyautogui also provides `pyautogui.moveTo(x, y, duration=...)` which allows smooth movement that applications can detect properly. Some apps require a non-zero duration for drag to register.

**Alternatives considered**:
- `pyautogui.drag(xOffset, yOffset)` — works with relative offsets, not absolute coordinates. Would require computing the offset from start to end. Less intuitive for absolute positioning.
- `pyautogui.click(start) + pyautogui.drag(offset)` — same offset issue plus an extra click.

## Decision 2: Drag Duration

**Decision**: Use a default drag duration of 0.5 seconds (500ms) for the moveTo step. This ensures the drag is smooth enough for most applications to register.

**Rationale**: Instantaneous mouse movement (duration=0) can cause some applications to miss the drag gesture entirely. A 0.5s duration provides a good balance between speed and reliability.

## Decision 3: Coordinate Picker Reuse

**Decision**: Reuse the existing `on_pick_coords` callback pattern by creating two separate callback methods — one for start coords and one for end coords — each targeting their respective entry fields.

**Rationale**: The existing Click step passes `self._on_coords_picked` as a callback. For Click And Move, we create `_on_start_coords_picked` and `_on_end_coords_picked`, each populating their own set of X/Y entries. The `on_pick_coords` callback in workflow_panel.py already accepts any callback function, so no changes are needed to the picker infrastructure.
