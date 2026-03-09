# Quickstart: Excel-Driven Desktop Automation Workflow Builder

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Automation_mouse-_and-Keyboard

# Install dependencies
pip install pyautogui openpyxl pynput
```

## Running the Application

```bash
python src/main.py
```

The main application window opens with three panels:
1. **Excel panel** (top) — import workbook, select worksheet
2. **Workflow panel** (center) — build and manage steps
3. **Execution panel** (bottom) — start/stop, progress, settings

## Your First Workflow

### 1. Import an Excel File

- Click **Import Excel** and select a `.xlsx` file.
- Choose a worksheet from the dropdown.
- The column headers appear for use in "Insert Column Value" steps.

### 2. Add Workflow Steps

Click **Add Step** and choose a step type:

| Step Type           | What to configure               |
|---------------------|----------------------------------|
| Click               | Screen X, Y (use "Pick" button or type manually) |
| Double Click        | Screen X, Y (use "Pick" button or type manually) |
| Type Text           | The literal text to type         |
| Wait                | Duration in milliseconds (min 50) |
| Insert Column Value | Select a column from the dropdown |
| Press Hotkey        | Select from: Enter, Backspace, Esc, Tab, Shift+Tab, Ctrl+A, Ctrl+C, Ctrl+V |

### 3. Pick Screen Coordinates

For click steps, click the **Pick** button next to the coordinate fields.
A transparent overlay appears. Click the target location on your screen.
The X and Y values are filled in automatically. You can fine-tune them
manually afterward.

### 4. Run the Workflow

- (Optional) Set a **Start Row** if you want to skip already-processed rows.
- (Optional) Check **Dry Run** to log actions without executing them.
- Click **Start**. The system processes each Excel row, running your steps.
- Watch the progress indicator (e.g., "Row 42 of 500").
- Press **Stop** or the **Esc** key at any time to halt execution.

### 5. Save and Load

- Click **Save Workflow** to save to a `.json` file.
- Click **Load Workflow** to restore a previously saved workflow.
- Saved workflows retain all steps and parameters.

## Example Workflow

**Scenario**: Enter names and emails from Excel into a web form.

1. Click at (300, 400) — focus the "Name" field
2. Insert Column Value: "Name"
3. Press Hotkey: Tab — move to "Email" field
4. Insert Column Value: "Email"
5. Press Hotkey: Enter — submit the form
6. Wait: 1000ms — wait for page to reload

This workflow runs once per Excel row, filling in and submitting the
form for each person in the spreadsheet.

## Execution Log

After each run, a timestamped log is written showing every action taken.
Dry-run logs are prefixed with `[DRY-RUN]` for easy identification.

## Troubleshooting

- **Kill-switch not working?** Ensure no other application is capturing
  the Esc key globally.
- **Clicks landing in wrong place?** Verify your display scaling is set
  to 100%, or re-pick coordinates with the Pick button.
- **Excel values look wrong?** The system uses the displayed/formatted
  text. Check the cell formatting in Excel.
