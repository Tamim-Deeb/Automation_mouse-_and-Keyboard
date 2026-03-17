# Research: Write To Excel Step

## Decision 1: Write Mechanism (openpyxl read_only vs write mode)

**Decision**: Use a separate `openpyxl.load_workbook(file_path, read_only=False)` call in ExcelWriter for write operations.

**Rationale**: The existing `ExcelReader` opens workbooks in `read_only=True` mode which does not support cell modification. openpyxl requires `read_only=False` to write. Since the executor holds the reader open in a `with` block during the entire run, the writer must open a separate workbook instance in write mode, modify the cell, and save. This is safe because openpyxl read_only and write mode can coexist on the same file (read_only uses a streaming reader, write mode loads the full workbook).

**Alternatives considered**:
- Close reader before writing, reopen after: Too complex, breaks the executor's row iteration.
- Buffer all writes and flush at end: Risk of data loss on crash; user expects immediate persistence per FR-007.
- Use xlsxwriter instead: Write-only library, cannot read existing files.

## Decision 2: Write Timing (per-step vs batched)

**Decision**: Open workbook, write cell, save, and close on every write_to_excel step execution.

**Rationale**: FR-007 requires saving after each write. Opening/writing/saving per step is simple and ensures data persistence. For typical workflows (tens to hundreds of rows), the overhead is acceptable. Each write operation takes ~50-200ms with openpyxl for small-to-medium files.

**Alternatives considered**:
- Keep workbook open across rows: Risk of file corruption if process crashes mid-run; complicates resource management.
- Batch writes per N rows: Violates FR-007 (save after each write); adds complexity with no user benefit at current scale.

## Decision 3: Clipboard Access for Paste Mode

**Decision**: Use `pyperclip.paste()` to read clipboard content. Add a `paste()` method to the existing `ClipboardModule`.

**Rationale**: The project already uses pyperclip (via ClipboardModule.clear()). Adding `paste()` is consistent and requires no new dependencies.

**Alternatives considered**:
- Direct pyperclip.paste() in handler: Bypasses module pattern; violates Constitution III (Modular Extensibility).
- tkinter clipboard access: Requires a root window reference; more complex for no benefit.

## Decision 4: Row Number Mapping (data row to Excel row)

**Decision**: The handler needs the current data row number (1-indexed) to compute the Excel row. Excel row = data_row_number + 1 (header is row 1, data starts at row 2). The executor already tracks `row_number` and can pass it via the session or as a parameter.

**Rationale**: The executor currently passes `(step, session, row_data)` to handlers. The session has `current_row` which is set to `row_number` before step execution. The write handler can use `session.current_row` to compute the Excel row as `session.current_row + 1`.

**Alternatives considered**:
- Add row_number as a 4th handler parameter: Changes handler signature; would break all existing handlers.
- Store in step params at runtime: Pollutes serializable params with runtime data.

## Decision 5: Column Name to Column Index Mapping

**Decision**: ExcelWriter accepts column name and maps it to the column index using the header row. Load header row on each write to get the column index, then write to the correct cell.

**Rationale**: Column names are what the user configures; the writer needs to find the matching column index. Reading the header row each time the writer opens the workbook is negligible overhead and ensures correctness even if columns were reordered externally.

**Alternatives considered**:
- Cache column index from reader: Adds coupling between reader and writer.
- Accept column index directly: Requires the UI to map names to indices; pushes complexity to the wrong layer.
