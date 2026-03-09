"""Workflow serialization for saving/loading workflows to/from JSON"""
import json
from datetime import datetime
from typing import Dict, Any
from src.workflow.models import Workflow, WorkflowStep, StepType


class WorkflowSerializer:
    """
    Serializes and deserializes workflows to/from JSON format.
    Validates against the workflow file schema.
    """
    
    def __init__(self):
        """Initialize the serializer"""
        pass
    
    def save(self, workflow: Workflow, file_path: str) -> None:
        """
        Save a workflow to a JSON file.
        
        Args:
            workflow: The workflow to save
            file_path: Path to the output JSON file
            
        Raises:
            ValueError: If workflow validation fails
            IOError: If file cannot be written
        """
        # Validate workflow
        errors = workflow.validate()
        if errors:
            raise ValueError(f"Workflow validation failed:\n" + "\n".join(errors))
        
        # Update timestamps
        workflow.updated_at = datetime.utcnow()
        if workflow.created_at is None:
            workflow.created_at = workflow.updated_at
        
        # Convert to dictionary
        workflow_dict = self._workflow_to_dict(workflow)
        
        # Write to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_dict, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to write workflow file: {e}")
    
    def load(self, file_path: str) -> Workflow:
        """
        Load a workflow from a JSON file.
        
        Args:
            file_path: Path to the input JSON file
            
        Returns:
            Loaded Workflow object
            
        Raises:
            ValueError: If file is invalid or validation fails
            IOError: If file cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_dict = json.load(f)
        except IOError as e:
            raise IOError(f"Failed to read workflow file: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        
        # Validate structure
        self._validate_structure(workflow_dict)
        
        # Convert to Workflow object
        workflow = self._dict_to_workflow(workflow_dict)
        
        # Validate workflow
        errors = workflow.validate()
        if errors:
            raise ValueError(f"Workflow validation failed:\n" + "\n".join(errors))
        
        return workflow
    
    def _workflow_to_dict(self, workflow: Workflow) -> Dict[str, Any]:
        """Convert a Workflow object to a dictionary"""
        return {
            "name": workflow.name,
            "steps": [self._step_to_dict(step) for step in workflow.steps],
            "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
            "updated_at": workflow.updated_at.isoformat() if workflow.updated_at else None
        }
    
    def _step_to_dict(self, step: WorkflowStep) -> Dict[str, Any]:
        """Convert a WorkflowStep object to a dictionary"""
        return {
            "type": step.type.value,
            "params": step.params
        }
    
    def _dict_to_workflow(self, workflow_dict: Dict[str, Any]) -> Workflow:
        """Convert a dictionary to a Workflow object"""
        steps = [self._dict_to_step(step_dict) for step_dict in workflow_dict.get("steps", [])]
        
        created_at = self._parse_datetime(workflow_dict.get("created_at"))
        updated_at = self._parse_datetime(workflow_dict.get("updated_at"))
        
        return Workflow(
            name=workflow_dict.get("name", "Workflow"),
            steps=steps,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def _dict_to_step(self, step_dict: Dict[str, Any]) -> WorkflowStep:
        """Convert a dictionary to a WorkflowStep object"""
        try:
            step_type = StepType(step_dict["type"])
        except ValueError:
            raise ValueError(f"Invalid step type: {step_dict.get('type')}")
        
        return WorkflowStep(
            type=step_type,
            order=step_dict.get("order", 0),
            params=step_dict.get("params", {})
        )
    
    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parse an ISO 8601 datetime string"""
        if not datetime_str:
            return None
        
        try:
            return datetime.fromisoformat(datetime_str)
        except ValueError:
            raise ValueError(f"Invalid datetime format: {datetime_str}")
    
    def _validate_structure(self, workflow_dict: Dict[str, Any]) -> None:
        """Validate the basic structure of a workflow dictionary"""
        # Check required fields
        required_fields = ["name", "steps", "created_at", "updated_at"]
        for field in required_fields:
            if field not in workflow_dict:
                raise ValueError(f"Missing required field: {field}")
        
        # Check types
        if not isinstance(workflow_dict["name"], str):
            raise ValueError("Field 'name' must be a string")
        
        if not isinstance(workflow_dict["steps"], list):
            raise ValueError("Field 'steps' must be a list")
        
        # Validate each step
        for i, step_dict in enumerate(workflow_dict["steps"]):
            if not isinstance(step_dict, dict):
                raise ValueError(f"Step {i} must be a dictionary")
            
            if "type" not in step_dict:
                raise ValueError(f"Step {i} missing required field: type")
            
            if "params" not in step_dict:
                raise ValueError(f"Step {i} missing required field: params")
            
            # Validate step type
            try:
                StepType(step_dict["type"])
            except ValueError:
                raise ValueError(f"Step {i} has invalid type: {step_dict['type']}")
