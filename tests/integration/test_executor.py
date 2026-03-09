"""Integration tests for workflow executor"""
import pytest
from datetime import datetime
from src.workflow.models import Workflow, WorkflowStep, StepType, ExecutionSession, ExcelDataSource, LogEntry
from src.engine.executor import WorkflowExecutor
from src.engine.step_registry import register_step_handler, get_global_registry
from src.automation.mouse import MouseAutomation
from src.automation.keyboard import KeyboardAutomation
from src.automation.wait import WaitModule


@pytest.fixture
def mock_automation_modules():
    """Create mock automation modules for testing"""
    mouse = MouseAutomation(delay_ms=0)
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    wait = WaitModule()
    return mouse, keyboard, wait


@pytest.fixture
def registered_handlers(mock_automation_modules):
    """Register step handlers for testing"""
    mouse, keyboard, wait = mock_automation_modules
    registry = get_global_registry()
    
    # Register handlers for all step types
    def click_handler(step, session, row_data):
        x = step.params["x"]
        y = step.params["y"]
        mouse.click(x, y)
    
    def double_click_handler(step, session, row_data):
        x = step.params["x"]
        y = step.params["y"]
        mouse.double_click(x, y)
    
    def type_text_handler(step, session, row_data):
        text = step.params["text"]
        keyboard.type_text(text)
    
    def wait_handler(step, session, row_data):
        duration_ms = step.params["duration_ms"]
        wait.sleep(duration_ms)
    
    def insert_column_value_handler(step, session, row_data):
        column_name = step.params["column_name"]
        value = row_data.get(column_name, "")
        keyboard.type_text(value)
    
    def press_hotkey_handler(step, session, row_data):
        hotkey_str = step.params["hotkey"]
        keyboard.press_hotkey_by_string(hotkey_str)
    
    registry.register(StepType.CLICK, click_handler)
    registry.register(StepType.DOUBLE_CLICK, double_click_handler)
    registry.register(StepType.TYPE_TEXT, type_text_handler)
    registry.register(StepType.WAIT, wait_handler)
    registry.register(StepType.INSERT_COLUMN_VALUE, insert_column_value_handler)
    registry.register(StepType.PRESS_HOTKEY, press_hotkey_handler)
    
    yield
    
    # Cleanup
    registry.unregister(StepType.CLICK)
    registry.unregister(StepType.DOUBLE_CLICK)
    registry.unregister(StepType.TYPE_TEXT)
    registry.unregister(StepType.WAIT)
    registry.unregister(StepType.INSERT_COLUMN_VALUE)
    registry.unregister(StepType.PRESS_HOTKEY)


def test_executor_dry_run(sample_workflow, sample_excel_file, registered_handlers):
    """Test executor in dry-run mode"""
    # Create execution session
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=True,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute in dry-run mode
    executor.execute()
    
    # Verify session completed
    assert session.status == "completed"
    assert session.current_row == 5  # All rows processed
    
    # Verify log entries were created
    assert len(session.log_entries) > 0
    
    # Verify all log entries are marked as dry-run
    for entry in session.log_entries:
        assert entry.dry_run is True


def test_executor_normal_execution(sample_workflow, sample_excel_file, registered_handlers):
    """Test executor in normal mode"""
    # Create execution session
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=False,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute
    executor.execute()
    
    # Verify session completed
    assert session.status == "completed"
    assert session.current_row == 5
    
    # Verify log entries were created
    assert len(session.log_entries) > 0
    
    # Verify log entries are NOT marked as dry-run
    for entry in session.log_entries:
        assert entry.dry_run is False


def test_executor_with_start_row(sample_workflow, sample_excel_file, registered_handlers):
    """Test executor starting from a specific row"""
    # Create execution session starting from row 3
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=3,
        current_row=0,
        status="idle",
        dry_run=True,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute
    executor.execute()
    
    # Verify only rows 3, 4, 5 were processed
    assert session.status == "completed"
    assert session.current_row == 5
    
    # Verify log entries for correct rows
    row_numbers = {entry.row for entry in session.log_entries}
    assert row_numbers == {3, 4, 5}


def test_executor_log_entries(sample_workflow, sample_excel_file, registered_handlers):
    """Test that log entries contain correct information"""
    # Create execution session
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=True,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute
    executor.execute()
    
    # Verify log entry structure
    assert len(session.log_entries) > 0
    
    first_entry = session.log_entries[0]
    assert isinstance(first_entry.timestamp, datetime)
    assert first_entry.row == 1
    assert first_entry.step_type in ["click", "insert_column_value", "press_hotkey", "wait"]
    assert isinstance(first_entry.detail, str)
    assert first_entry.dry_run is True


def test_executor_empty_workflow(sample_excel_file, registered_handlers):
    """Test executor with empty workflow"""
    # Create empty workflow
    workflow = Workflow(
        name="Empty Workflow",
        steps=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Create execution session
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=True,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute
    executor.execute()
    
    # Verify session completed with no log entries
    assert session.status == "completed"
    assert len(session.log_entries) == 0


def test_executor_invalid_start_row(sample_workflow, sample_excel_file, registered_handlers):
    """Test executor with invalid start row"""
    # Create execution session with invalid start row
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    session = ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=10,  # Invalid: only 5 rows
        current_row=0,
        status="idle",
        dry_run=True,
        log_entries=[]
    )
    
    # Create executor
    executor = WorkflowExecutor(session)
    
    # Execute should handle gracefully
    executor.execute()
    
    # Verify session completed (no rows to process)
    assert session.status == "completed"
