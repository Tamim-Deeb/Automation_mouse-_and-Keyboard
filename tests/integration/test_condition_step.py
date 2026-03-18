"""Integration tests for Condition step - evaluation, skip logic, and cascade skip"""
import pytest
from datetime import datetime
from unittest.mock import patch
from src.workflow.models import Workflow, WorkflowStep, StepType, ExecutionSession, ExcelDataSource
from src.engine.executor import WorkflowExecutor
from src.engine.step_registry import get_global_registry


@pytest.fixture
def executed_steps():
    """Track which steps were executed"""
    return []


@pytest.fixture
def condition_handlers(executed_steps):
    """Register handlers that track execution for testing"""
    registry = get_global_registry()

    def tracking_click_handler(step, session, row_data):
        executed_steps.append(("click", step.order))

    def tracking_type_handler(step, session, row_data):
        executed_steps.append(("type_text", step.order))

    def tracking_wait_handler(step, session, row_data):
        executed_steps.append(("wait", step.order))

    def condition_handler(step, session, row_data):
        """Condition handler that reads clipboard and sets skip counter"""
        import pyperclip
        compare_word = step.params["compare_word"]
        is_equal = step.params["is_equal"]
        step_count = step.params["step_count"]

        clipboard_content = pyperclip.paste()
        match = (clipboard_content == compare_word)
        condition_true = match if is_equal else not match

        executed_steps.append(("condition", step.order, condition_true))

        if not condition_true:
            # Find the executor — it's passed via the registry pattern
            # We need to set skip_remaining on the executor
            # In tests, we access it through a module-level reference
            condition_handler._executor.skip_remaining = step_count

    registry.register(StepType.CLICK, tracking_click_handler)
    registry.register(StepType.TYPE_TEXT, tracking_type_handler)
    registry.register(StepType.WAIT, tracking_wait_handler)
    registry.register(StepType.CONDITION, condition_handler)

    yield condition_handler

    registry.unregister(StepType.CLICK)
    registry.unregister(StepType.TYPE_TEXT)
    registry.unregister(StepType.WAIT)
    registry.unregister(StepType.CONDITION)


def _make_session(steps, excel_file):
    """Helper to create a session with given steps"""
    workflow = Workflow(
        name="Test Condition",
        steps=steps,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    data_source = ExcelDataSource(
        file_path=excel_file,
        sheet_name="TestData",
        headers=["Name", "Email", "Age"],
        row_count=1
    )
    return ExecutionSession(
        workflow=workflow,
        data_source=data_source,
        start_row=1,
        current_row=0,
        status="idle",
        dry_run=False,
        log_entries=[]
    )


class TestEqualModeCondition:
    """Tests for equal-mode condition (is_equal=True)"""

    @patch("pyperclip.paste", return_value="Success")
    def test_equal_mode_match_executes_governed_steps(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """When clipboard matches compare_word with is_equal=True, governed steps execute"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "Success", "is_equal": True, "step_count": 2
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
            WorkflowStep(type=StepType.CLICK, order=2, params={"x": 30, "y": 40}),
            WorkflowStep(type=StepType.WAIT, order=3, params={"duration_ms": 50}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        # All steps should execute (condition true, no skipping)
        assert ("condition", 0, True) in executed_steps
        assert ("click", 1) in executed_steps
        assert ("click", 2) in executed_steps
        assert ("wait", 3) in executed_steps

    @patch("pyperclip.paste", return_value="Failure")
    def test_equal_mode_mismatch_skips_governed_steps(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """When clipboard doesn't match compare_word with is_equal=True, governed steps are skipped"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "Success", "is_equal": True, "step_count": 2
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
            WorkflowStep(type=StepType.CLICK, order=2, params={"x": 30, "y": 40}),
            WorkflowStep(type=StepType.WAIT, order=3, params={"duration_ms": 50}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        # Condition false — steps 1 and 2 skipped, step 3 executes
        assert ("condition", 0, False) in executed_steps
        assert ("click", 1) not in executed_steps
        assert ("click", 2) not in executed_steps
        assert ("wait", 3) in executed_steps

    @patch("pyperclip.paste", return_value="")
    def test_equal_mode_empty_word_empty_clipboard(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """Empty compare_word with empty clipboard → condition true"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "", "is_equal": True, "step_count": 1
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, True) in executed_steps
        assert ("click", 1) in executed_steps

    @patch("pyperclip.paste", return_value="something")
    def test_equal_mode_empty_word_nonempty_clipboard(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """Empty compare_word with non-empty clipboard → condition false"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "", "is_equal": True, "step_count": 1
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, False) in executed_steps
        assert ("click", 1) not in executed_steps


class TestNotEqualModeCondition:
    """Tests for not-equal-mode condition (is_equal=False)"""

    @patch("pyperclip.paste", return_value="OK")
    def test_not_equal_mode_mismatch_executes(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """When clipboard != compare_word with is_equal=False, governed steps execute"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "Error", "is_equal": False, "step_count": 2
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
            WorkflowStep(type=StepType.CLICK, order=2, params={"x": 30, "y": 40}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, True) in executed_steps
        assert ("click", 1) in executed_steps
        assert ("click", 2) in executed_steps

    @patch("pyperclip.paste", return_value="Error")
    def test_not_equal_mode_match_skips(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """When clipboard == compare_word with is_equal=False, governed steps are skipped"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "Error", "is_equal": False, "step_count": 2
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
            WorkflowStep(type=StepType.CLICK, order=2, params={"x": 30, "y": 40}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, False) in executed_steps
        assert ("click", 1) not in executed_steps
        assert ("click", 2) not in executed_steps

    @patch("pyperclip.paste", return_value="")
    def test_not_equal_empty_word_empty_clipboard(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """Empty compare_word with empty clipboard in not-equal mode → condition false (they match)"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "", "is_equal": False, "step_count": 1
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, False) in executed_steps
        assert ("click", 1) not in executed_steps

    @patch("pyperclip.paste", return_value="something")
    def test_not_equal_empty_word_nonempty_clipboard(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """Empty compare_word with non-empty clipboard in not-equal mode → condition true"""
        steps = [
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "", "is_equal": False, "step_count": 1
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        assert ("condition", 0, True) in executed_steps
        assert ("click", 1) in executed_steps


class TestCascadeSkip:
    """Tests for cascade skip with nested conditions"""

    @patch("pyperclip.paste", return_value="wrong")
    def test_cascade_skip_nested_condition(
        self, mock_paste, sample_excel_file, executed_steps, condition_handlers
    ):
        """Outer condition false → inner condition and its governed steps all skipped"""
        steps = [
            # Outer condition: equal "right", step_count=3 (governs steps 1, 2, 3)
            WorkflowStep(type=StepType.CONDITION, order=0, params={
                "compare_word": "right", "is_equal": True, "step_count": 3
            }),
            WorkflowStep(type=StepType.CLICK, order=1, params={"x": 10, "y": 20}),
            # Inner condition at position 2, governs 2 steps (steps 3, 4)
            WorkflowStep(type=StepType.CONDITION, order=2, params={
                "compare_word": "inner", "is_equal": True, "step_count": 2
            }),
            WorkflowStep(type=StepType.CLICK, order=3, params={"x": 30, "y": 40}),
            # Step 4 is governed by inner condition but beyond outer's range
            WorkflowStep(type=StepType.CLICK, order=4, params={"x": 50, "y": 60}),
            # Step 5 should be free of both conditions
            WorkflowStep(type=StepType.WAIT, order=5, params={"duration_ms": 50}),
        ]
        session = _make_session(steps, sample_excel_file)
        executor = WorkflowExecutor(session)
        condition_handlers._executor = executor
        executor.execute()

        # Outer condition false → skip steps 1, 2, 3
        # Step 2 is inner CONDITION with step_count=2 → cascade adds 2 more skips
        # So skip steps 1, 2, 3, 4, 5... wait, let me recalculate:
        # skip_remaining starts at 3 (from outer)
        # Step 1 (click): skip_remaining=3, decrement → 2, skip
        # Step 2 (inner CONDITION): skip_remaining=2, add step_count(2) → 4, decrement → 3, skip
        # Step 3 (click): skip_remaining=3, decrement → 2, skip
        # Step 4 (click): skip_remaining=2, decrement → 1, skip
        # Step 5 (wait): skip_remaining=1, decrement → 0, skip
        # All skipped!
        assert ("condition", 0, False) in executed_steps
        assert ("click", 1) not in executed_steps
        assert ("click", 3) not in executed_steps
        assert ("click", 4) not in executed_steps
        assert ("wait", 5) not in executed_steps
