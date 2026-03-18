# Data Model: UI Polish & Visual Enhancement

## Overview

This feature introduces no new persistent data entities. All changes are visual — styling, sizing, positioning, and animation. The data model below documents the **theme configuration** used across the application.

## Theme Color Palette

### Dark Header Area
- **Background**: Dark charcoal (#2b2b2b)
- **Text/Labels**: White (#ffffff)
- **Menu bar**: Dark (#2b2b2b) with light text

### Light Content Panels
- **Panel background**: Light gray (#f5f5f5)
- **Panel border**: Medium gray (#cccccc)
- **LabelFrame title**: Dark accent (#2b2b2b) text on light background
- **Entry fields**: White (#ffffff) background, dark text (#333333)

### Buttons
- **Normal**: Medium blue (#4a90d9) background, white text
- **Hover (active)**: Darker blue (#357abd) background
- **Pressed**: Even darker blue (#2a5f9e) background
- **Disabled**: Gray (#999999) background

### Step Listbox
- **Normal row**: White (#ffffff) background, dark text (#333333)
- **Selected row**: Blue highlight (#4a90d9) background, white text
- **Condition equal row**: Light blue (#CCE5FF) — preserved from existing
- **Condition not-equal row**: Light yellow (#FFFFCC) — preserved from existing
- **New step highlight**: Light green (#90EE90) — 500ms pulse on add

### Accent Colors
- **Primary accent**: Blue (#4a90d9) — buttons, selected items
- **Success/highlight**: Light green (#90EE90) — new step animation
- **Section separator**: Medium gray (#cccccc) — between panels

## Dialog Sizes

| Dialog | Width | Height | Notes |
|--------|-------|--------|-------|
| Add Step | 320 | 580 | Fits all 11 buttons + cancel + padding |
| Click / Double Click | 400 | 300 | Coordinates + Pick button |
| Type Text | 400 | 300 | Text entry |
| Wait | 400 | 300 | Duration entry |
| Insert Column Value | 400 | 300 | Column dropdown |
| Press Hotkey | 400 | 350 | Dropdown + custom fields |
| Copy Field | N/A | N/A | No editor (instant step) |
| Click And Move | 400 | 450 | Start/end coordinates |
| Write To Excel | 400 | 350 | Column + mode selector |
| Screen Loaded | 400 | 500 | Start/end coords + max tries |
| Condition | 400 | 350 | Equal checkbox + word + count |

## Relationships to Existing Code

- **No new files created** for data model
- Theme colors applied via `ttk.Style` in a new theme module
- Dialog sizes defined as constants alongside dialog classes
- Condition step coloring (#CCE5FF, #FFFFCC) remains unchanged in `workflow_panel.py`
