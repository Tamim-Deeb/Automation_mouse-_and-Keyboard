# Data Model: Copy Field Step

## Entities

### StepType (existing, extended)

Add a new enum value to the existing `StepType` enum:

| Value | String Representation |
|-------|----------------------|
| COPY_FIELD | "copy_field" |

### WorkflowStep (existing, no changes)

The Copy Field step uses the existing `WorkflowStep` dataclass with:
- `type`: `StepType.COPY_FIELD`
- `order`: Position in the workflow
- `params`: Empty dictionary `{}` — no parameters needed

### Serialization

The existing `WorkflowSerializer` handles Copy Field steps automatically since it serializes `step.type.value` (the string "copy_field") and `step.params` (empty dict). No serialization changes needed.

## Validation Rules

- Copy Field step requires no parameters — `params` must be empty or omitted
- No validation errors should be generated for this step type (unlike CLICK which requires x/y)
