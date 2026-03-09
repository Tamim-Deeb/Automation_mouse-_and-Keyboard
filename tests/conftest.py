"""Shared pytest fixtures for integration tests"""
import os
import tempfile
from datetime import datetime
from openpyxl import Workbook

import pytest


@pytest.fixture
def sample_excel_file():
    """Create a temporary Excel file with sample data for testing"""
    wb = Workbook()
    ws = wb.active
    ws.title = "TestData"
    
    # Add headers
    ws.append(["Name", "Email", "Age"])
    
    # Add sample data rows
    ws.append(["John Doe", "john@example.com", 30])
    ws.append(["Jane Smith", "jane@example.com", 25])
    ws.append(["Bob Johnson", "bob@example.com", 35])
    ws.append(["Alice Brown", "alice@example.com", 28])
    ws.append(["Charlie Wilson", "charlie@example.com", 42])
    
    # Create temporary file
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    wb.save(path)
    
    yield path
    
    # Cleanup
    try:
        os.remove(path)
    except OSError:
        pass


@pytest.fixture
def sample_workflow():
    """Create a sample workflow for testing"""
    from src.workflow.models import Workflow, WorkflowStep, StepType
    
    steps = [
        WorkflowStep(
            type=StepType.CLICK,
            order=0,
            params={"x": 100, "y": 200}
        ),
        WorkflowStep(
            type=StepType.INSERT_COLUMN_VALUE,
            order=1,
            params={"column_name": "Name"}
        ),
        WorkflowStep(
            type=StepType.PRESS_HOTKEY,
            order=2,
            params={"hotkey": "Tab"}
        ),
        WorkflowStep(
            type=StepType.WAIT,
            order=3,
            params={"duration_ms": 500}
        ),
    ]
    
    return Workflow(
        name="Test Workflow",
        steps=steps,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_execution_session(sample_workflow, sample_excel_file):
    """Create a sample execution session for testing"""
    from src.workflow.models import ExecutionSession, ExcelDataSource
    
    data_source = ExcelDataSource(
        file_path=sample_excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=5
    )
    
    return ExecutionSession(
        workflow=sample_workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=False,
        log_entries=[]
    )
