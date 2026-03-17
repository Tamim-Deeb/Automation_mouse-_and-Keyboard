# Data Model: Click And Move Step

## Entities

### WorkflowStep — CLICK_AND_MOVE type

The `params` dict for a `CLICK_AND_MOVE` step stores four integer coordinates:

| Field   | Type | Description                        |
|---------|------|------------------------------------|
| start_x | int  | X coordinate of the drag start point |
| start_y | int  | Y coordinate of the drag start point |
| end_x   | int  | X coordinate of the drag end point   |
| end_y   | int  | Y coordinate of the drag end point   |

**Validation rules**:
- All four fields are required
- All four must be integers
- Negative values are accepted (multi-monitor support)

**Storage format**: JSON via existing `WorkflowSerializer`

```json
{
  "type": "click_and_move",
  "order": 2,
  "params": {
    "start_x": 100,
    "start_y": 200,
    "end_x": 300,
    "end_y": 400
  }
}
```

## Relationships

- `StepType.CLICK_AND_MOVE` enum value = `"click_and_move"`
- Uses `MouseAutomation.drag(start_x, start_y, end_x, end_y)` for execution
- Reuses `CoordinatePicker` from the Click step (no changes to picker)
