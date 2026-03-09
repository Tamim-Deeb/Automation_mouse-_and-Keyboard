#!/usr/bin/env python3
"""
Quickstart validation script for the Excel Automation Workflow Builder.

This script validates that the application can be run and basic functionality works.
For full validation, manually run the scenarios from quickstart.md.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.workflow.models import Workflow, WorkflowStep, StepType, ExecutionSession, ExcelDataSource
        from src.workflow.serializer import WorkflowSerializer
        from src.engine.executor import WorkflowExecutor
        from src.engine.step_registry import StepRegistry, get_global_registry
        from src.engine.kill_switch import KillSwitch
        from src.excel.reader import ExcelReader
        from src.automation.mouse import MouseAutomation
        from src.automation.keyboard import KeyboardAutomation
        from src.automation.wait import WaitModule
        from src.action_logging.action_logger import ActionLogger
        from src.gui.app import App
        from src.gui.excel_panel import ExcelPanel
        from src.gui.workflow_panel import WorkflowPanel
        from src.gui.execution_panel import ExecutionPanel
        from src.gui.coordinate_picker import CoordinatePicker
        from src.gui.step_editors import StepEditorDialog, AddStepDialog
        
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_workflow_creation():
    """Test creating a workflow with steps"""
    print("\nTesting workflow creation...")
    
    try:
        from src.workflow.models import Workflow, WorkflowStep, StepType
        from datetime import datetime
        
        # Create workflow with multiple step types
        steps = [
            WorkflowStep(type=StepType.CLICK, order=0, params={"x": 100, "y": 200}),
            WorkflowStep(type=StepType.TYPE_TEXT, order=1, params={"text": "Hello"}),
            WorkflowStep(type=StepType.WAIT, order=2, params={"duration_ms": 500}),
        ]
        
        workflow = Workflow(
            name="Test Workflow",
            steps=steps,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Validate workflow
        errors = workflow.validate()
        if errors:
            print(f"✗ Workflow validation failed: {errors}")
            return False
        
        print(f"✓ Workflow created with {len(steps)} steps")
        return True
    except Exception as e:
        print(f"✗ Workflow creation failed: {e}")
        return False


def test_step_registry():
    """Test step registry functionality"""
    print("\nTesting step registry...")
    
    try:
        from src.engine.step_registry import StepRegistry, StepType
        from src.workflow.models import WorkflowStep, ExecutionSession, ExcelDataSource
        
        registry = StepRegistry()
        
        # Register a test handler
        def test_handler(step, session, row_data):
            pass
        
        registry.register(StepType.CLICK, test_handler)
        
        # Check handler is registered
        if not registry.has_handler(StepType.CLICK):
            print("✗ Handler registration failed")
            return False
        
        # Get handler
        handler = registry.get_handler(StepType.CLICK)
        if handler is None:
            print("✗ Handler retrieval failed")
            return False
        
        print("✓ Step registry working correctly")
        return True
    except Exception as e:
        print(f"✗ Step registry test failed: {e}")
        return False


def test_automation_modules():
    """Test automation modules"""
    print("\nTesting automation modules...")
    
    try:
        from src.automation.mouse import MouseAutomation
        from src.automation.keyboard import KeyboardAutomation
        from src.automation.wait import WaitModule
        
        # Create instances
        mouse = MouseAutomation(delay_ms=0)
        keyboard = KeyboardAutomation(inter_key_delay_ms=0)
        wait = WaitModule()
        
        # Test basic functionality
        screen_size = mouse.get_screen_size()
        if screen_size[0] <= 0 or screen_size[1] <= 0:
            print("✗ Invalid screen size")
            return False
        
        hotkeys = KeyboardAutomation.get_supported_hotkeys()
        if len(hotkeys) == 0:
            print("✗ No supported hotkeys")
            return False
        
        min_delay = WaitModule.get_min_delay()
        if min_delay != 50:
            print("✗ Invalid minimum delay")
            return False
        
        print("✓ Automation modules working correctly")
        return True
    except Exception as e:
        print(f"✗ Automation modules test failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Excel Automation Workflow Builder - Quickstart Validation")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Workflow Creation", test_workflow_creation()))
    results.append(("Step Registry", test_step_registry()))
    results.append(("Automation Modules", test_automation_modules()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    # Overall result
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("\nThe application is ready for manual testing.")
        print("Please run the scenarios from quickstart.md to validate full functionality:")
        print("  1. Your First Workflow")
        print("  2. Example Workflow")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
