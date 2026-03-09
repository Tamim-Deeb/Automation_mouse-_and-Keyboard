"""Integration tests for workflow serializer"""
import pytest
import tempfile
import os
from datetime import datetime
from src.workflow.models import Workflow, WorkflowStep, StepType
from src.workflow.serializer import WorkflowSerializer


@pytest.fixture
def sample_workflow():
    """Create a sample workflow with all step types"""
    steps = [
        WorkflowStep(
            type=StepType.CLICK,
            order=0,
            params={"x": 100, "y": 200}
        ),
        WorkflowStep(
            type=StepType.TYPE_TEXT,
            order=1,
            params={"text": "Hello World"}
        ),
        WorkflowStep(
            type=StepType.PRESS_HOTKEY,
            order=2,
            params={"hotkey": "Tab"}
        ),
        WorkflowStep(
            type=StepType.INSERT_COLUMN_VALUE,
            order=3,
            params={"column_name": "Name"}
        ),
        WorkflowStep(
            type=StepType.WAIT,
            order=4,
            params={"duration_ms": 500}
        ),
        WorkflowStep(
            type=StepType.DOUBLE_CLICK,
            order=5,
            params={"x": 300, "y": 400}
        ),
    ]
    
    return Workflow(
        name="Test Workflow",
        steps=steps,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_serializer_save_and_load(sample_workflow):
    """Test saving and loading a workflow"""
    serializer = WorkflowSerializer()
    
    # Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        # Save workflow
        serializer.save(sample_workflow, temp_path)
        
        # Verify file exists
        assert os.path.exists(temp_path)
        
        # Load workflow
        loaded_workflow = serializer.load(temp_path)
        
        # Verify workflow name
        assert loaded_workflow.name == sample_workflow.name
        
        # Verify step count
        assert len(loaded_workflow.steps) == len(sample_workflow.steps)
        
        # Verify each step
        for original_step, loaded_step in zip(sample_workflow.steps, loaded_workflow.steps):
            assert loaded_step.type == original_step.type
            assert loaded_step.order == original_step.order
            assert loaded_step.params == original_step.params
        
        # Verify timestamps (allow some tolerance)
        assert loaded_workflow.created_at is not None
        assert loaded_workflow.updated_at is not None
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_all_step_types():
    """Test that all step types are serialized correctly"""
    serializer = WorkflowSerializer()
    
    # Create workflow with all step types
    steps = [
        WorkflowStep(type=StepType.CLICK, order=0, params={"x": 10, "y": 20}),
        WorkflowStep(type=StepType.DOUBLE_CLICK, order=1, params={"x": 30, "y": 40}),
        WorkflowStep(type=StepType.TYPE_TEXT, order=2, params={"text": "Test"}),
        WorkflowStep(type=StepType.WAIT, order=3, params={"duration_ms": 100}),
        WorkflowStep(type=StepType.INSERT_COLUMN_VALUE, order=4, params={"column_name": "TestColumn"}),
        WorkflowStep(type=StepType.PRESS_HOTKEY, order=5, params={"hotkey": "Enter"}),
    ]
    
    workflow = Workflow(name="All Types", steps=steps)
    
    # Save and load
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        serializer.save(workflow, temp_path)
        loaded = serializer.load(temp_path)
        
        # Verify all step types
        assert len(loaded.steps) == 6
        assert loaded.steps[0].type == StepType.CLICK
        assert loaded.steps[1].type == StepType.DOUBLE_CLICK
        assert loaded.steps[2].type == StepType.TYPE_TEXT
        assert loaded.steps[3].type == StepType.WAIT
        assert loaded.steps[4].type == StepType.INSERT_COLUMN_VALUE
        assert loaded.steps[5].type == StepType.PRESS_HOTKEY
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_invalid_json():
    """Test loading invalid JSON file"""
    serializer = WorkflowSerializer()
    
    # Create temporary file with invalid JSON
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        with open(temp_path, 'w') as f:
            f.write("invalid json content")
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Invalid JSON format"):
            serializer.load(temp_path)
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_missing_required_field():
    """Test loading workflow with missing required field"""
    serializer = WorkflowSerializer()
    
    # Create temporary file with missing 'name' field
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        with open(temp_path, 'w') as f:
            f.write('{"steps": [], "created_at": "2024-01-01T00:00:00", "updated_at": "2024-01-01T00:00:00"}')
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Missing required field: name"):
            serializer.load(temp_path)
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_invalid_step_type():
    """Test loading workflow with invalid step type"""
    serializer = WorkflowSerializer()
    
    # Create temporary file with invalid step type
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        with open(temp_path, 'w') as f:
            f.write('''
            {
                "name": "Test",
                "steps": [
                    {"type": "invalid_type", "params": {}}
                ],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
            ''')
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Invalid step type"):
            serializer.load(temp_path)
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_empty_workflow():
    """Test saving and loading empty workflow"""
    serializer = WorkflowSerializer()
    
    workflow = Workflow(name="Empty", steps=[])
    
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        serializer.save(workflow, temp_path)
        loaded = serializer.load(temp_path)
        
        assert loaded.name == "Empty"
        assert len(loaded.steps) == 0
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_step_order_preserved():
    """Test that step order is preserved"""
    serializer = WorkflowSerializer()
    
    steps = [
        WorkflowStep(type=StepType.CLICK, order=0, params={"x": 1, "y": 1}),
        WorkflowStep(type=StepType.WAIT, order=1, params={"duration_ms": 100}),
        WorkflowStep(type=StepType.CLICK, order=2, params={"x": 2, "y": 2}),
    ]
    
    workflow = Workflow(name="Order Test", steps=steps)
    
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        serializer.save(workflow, temp_path)
        loaded = serializer.load(temp_path)
        
        # Verify order is preserved
        assert loaded.steps[0].order == 0
        assert loaded.steps[1].order == 1
        assert loaded.steps[2].order == 2
        
        # Verify step types in correct order
        assert loaded.steps[0].type == StepType.CLICK
        assert loaded.steps[1].type == StepType.WAIT
        assert loaded.steps[2].type == StepType.CLICK
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_serializer_complex_parameters():
    """Test serialization of complex parameter values"""
    serializer = WorkflowSerializer()
    
    steps = [
        WorkflowStep(
            type=StepType.TYPE_TEXT,
            order=0,
            params={"text": "Text with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"}
        ),
        WorkflowStep(
            type=StepType.WAIT,
            order=1,
            params={"duration_ms": 9999}
        ),
    ]
    
    workflow = Workflow(name="Complex Params", steps=steps)
    
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        serializer.save(workflow, temp_path)
        loaded = serializer.load(temp_path)
        
        # Verify complex parameters are preserved
        assert loaded.steps[0].params["text"] == "Text with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        assert loaded.steps[1].params["duration_ms"] == 9999
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
