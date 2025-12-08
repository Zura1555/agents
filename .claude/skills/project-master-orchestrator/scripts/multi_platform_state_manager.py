"""
Multi-Platform State Manager for Project Workflow Orchestration

Extends the base StateManager to support multi-platform workflows across
GitHub, Plane.so, and ClickUp with enhanced state tracking and metrics.

Author: Thuong-Tuan Tran
Version: 1.0.0
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class MultiPlatformStateManager:
    """
    Enhanced state manager for multi-platform workflow management.

    Tracks state across multiple platforms (ClickUp, GitHub, Plane.so)
    with detailed phase tracking, metrics collection, and error handling.
    """

    def __init__(self, state_file_path: str):
        """
        Initialize the state manager.

        Args:
            state_file_path: Path to the global state JSON file
        """
        self.state_file_path = state_file_path
        self.state = self._load_or_initialize_state()

    def _load_or_initialize_state(self) -> Dict[str, Any]:
        """
        Load existing state file or initialize new state.

        Returns:
            Initialized state dictionary
        """
        if os.path.exists(self.state_file_path):
            try:
                with open(self.state_file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state file: {e}")
                print("Initializing new state...")

        # Generate unique workflow ID
        workflow_id = f"workflow-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"

        # Initialize new state
        initial_state = {
            "workflowId": workflow_id,
            "action": "",
            "platforms": [],
            "status": "initialization",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "author": "Thuong-Tuan Tran",
            "phases": {
                "initialization": {
                    "status": "in_progress",
                    "output": "global-state.json",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                "discovery": {
                    "status": "pending",
                    "output": "",
                    "agents": {}
                },
                "analysis": {
                    "status": "pending",
                    "output": ""
                },
                "actions": {
                    "status": "pending",
                    "output": "",
                    "subphases": {}
                },
                "synchronization": {
                    "status": "pending",
                    "output": ""
                },
                "reporting": {
                    "status": "pending",
                    "output": ""
                }
            },
            "metadata": {
                "executionTime": 0,
                "startTime": datetime.utcnow().isoformat() + "Z",
                "platformsData": {},
                "metrics": {
                    "tasksCreated": 0,
                    "tasksUpdated": 0,
                    "tasksCompleted": 0,
                    "reportsGenerated": 0,
                    "monitoringEventsProcessed": 0,
                    "apiCallsMade": 0,
                    "apiSuccessRate": 0
                },
                "errors": []
            }
        }

        self._save_state(initial_state)
        return initial_state

    def _save_state(self, state: Optional[Dict[str, Any]] = None) -> None:
        """
        Save state to file.

        Args:
            state: State to save (uses self.state if not provided)
        """
        state_to_save = state if state is not None else self.state

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)

            # Write to temporary file first, then rename (atomic operation)
            temp_file = f"{self.state_file_path}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(state_to_save, f, indent=2, ensure_ascii=False)
            os.rename(temp_file, self.state_file_path)

        except IOError as e:
            print(f"Error saving state file: {e}")
            raise

    def update_workflow_info(self, action: str, platforms: List[str], project: str) -> None:
        """
        Update workflow metadata.

        Args:
            action: Workflow action (monitor, report, manage, sync)
            platforms: List of platforms to process
            project: Project identifier
        """
        self.state["action"] = action
        self.state["platforms"] = platforms
        self.state["project"] = project
        self._save_state()

    def update_phase(self, phase_name: str, status: str, output: str = "") -> None:
        """
        Update phase status.

        Args:
            phase_name: Name of the phase
            status: Status (pending, in_progress, complete, error)
            output: Path to output file (optional)
        """
        if phase_name not in self.state["phases"]:
            self.state["phases"][phase_name] = {
                "status": "pending",
                "output": ""
            }

        self.state["phases"][phase_name]["status"] = status
        self.state["phases"][phase_name]["timestamp"] = datetime.utcnow().isoformat() + "Z"

        if output:
            self.state["phases"][phase_name]["output"] = output

        # Update overall status to current phase
        self.state["status"] = phase_name

        self._save_state()

    def add_agent_status(self, phase_name: str, agent_name: str, status: str) -> None:
        """
        Add agent status to a phase.

        Args:
            phase_name: Phase containing the agent
            agent_name: Name of the agent
            status: Agent status
        """
        if "agents" not in self.state["phases"][phase_name]:
            self.state["phases"][phase_name]["agents"] = {}

        self.state["phases"][phase_name]["agents"][agent_name] = status
        self._save_state()

    def add_subphase_status(self, phase_name: str, subphase_name: str, status: str) -> None:
        """
        Add subphase status to actions phase.

        Args:
            phase_name: Should be "actions"
            subphase_name: Name of the subphase
            status: Status of the subphase
        """
        if "subphases" not in self.state["phases"][phase_name]:
            self.state["phases"][phase_name]["subphases"] = {}

        self.state["phases"][phase_name]["subphases"][subphase_name] = status
        self._save_state()

    def update_platform_data(self, platform: str, data: Dict[str, Any]) -> None:
        """
        Update platform-specific data.

        Args:
            platform: Platform name (clickup, github, plane)
            data: Platform data to store
        """
        self.state["metadata"]["platformsData"][platform] = data
        self._save_state()

    def add_metric(self, metric_name: str, value: int or float) -> None:
        """
        Add a metric value.

        Args:
            metric_name: Name of the metric
            value: Numeric value
        """
        self.state["metadata"]["metrics"][metric_name] = value
        self._save_state()

    def increment_metric(self, metric_name: str, increment: int = 1) -> None:
        """
        Increment a metric value.

        Args:
            metric_name: Name of the metric
            increment: Value to add (default: 1)
        """
        current = self.state["metadata"]["metrics"].get(metric_name, 0)
        self.state["metadata"]["metrics"][metric_name] = current + increment
        self._save_state()

    def log_error(self, phase: str, error: str or Dict[str, Any]) -> None:
        """
        Log an error with context.

        Args:
            phase: Phase where error occurred
            error: Error message or dictionary
        """
        error_entry = {
            "phase": phase,
            "error": error,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "workflowId": self.state.get("workflowId")
        }

        if isinstance(error, dict):
            error_entry.update(error)

        self.state["metadata"]["errors"].append(error_entry)
        self._save_state()

    def mark_phase_error(self, phase_name: str, error: str) -> None:
        """
        Mark a phase as error with logging.

        Args:
            phase_name: Name of the phase
            error: Error message
        """
        self.update_phase(phase_name, "error")
        self.log_error(phase_name, error)

    def get_phase_status(self, phase_name: str) -> str:
        """
        Get status of a specific phase.

        Args:
            phase_name: Name of the phase

        Returns:
            Phase status string
        """
        return self.state["phases"].get(phase_name, {}).get("status", "unknown")

    def get_platforms(self) -> List[str]:
        """
        Get list of platforms.

        Returns:
            List of platform names
        """
        return self.state.get("platforms", [])

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.

        Returns:
            Dictionary of metrics
        """
        return self.state.get("metadata", {}).get("metrics", {})

    def get_errors(self) -> List[Dict[str, Any]]:
        """
        Get all logged errors.

        Returns:
            List of error dictionaries
        """
        return self.state.get("metadata", {}).get("errors", [])

    def calculate_execution_time(self) -> float:
        """
        Calculate total execution time in seconds.

        Returns:
            Execution time in seconds
        """
        start_time_str = self.state.get("metadata", {}).get("startTime")
        if not start_time_str:
            return 0

        start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
        current_time = datetime.utcnow().replace(tzinfo=None)

        execution_time = (current_time - start_time).total_seconds()
        self.state["metadata"]["executionTime"] = round(execution_time, 2)
        self._save_state()

        return execution_time

    def is_phase_complete(self, phase_name: str) -> bool:
        """
        Check if a phase is complete.

        Args:
            phase_name: Name of the phase

        Returns:
            True if phase is complete
        """
        return self.get_phase_status(phase_name) == "complete"

    def all_platforms_complete(self, phase_name: str) -> bool:
        """
        Check if all platforms have completed a phase.

        Args:
            phase_name: Phase name with agents sub-dictionary

        Returns:
            True if all agents are complete
        """
        agents = self.state.get("phases", {}).get(phase_name, {}).get("agents", {})
        return all(status == "complete" for status in agents.values())

    def complete_workflow(self) -> None:
        """
        Mark workflow as complete and calculate final metrics.
        """
        self.calculate_execution_time()

        # Update main status
        self.state["status"] = "complete"
        self.state["completedAt"] = datetime.utcnow().isoformat() + "Z"

        # Mark all phases as complete if they haven't errored
        for phase_name, phase_data in self.state["phases"].items():
            if phase_data.get("status") not in ["complete", "error"]:
                self.update_phase(phase_name, "complete")

        self._save_state()

    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current state.

        Returns:
            Dictionary with workflow summary
        """
        return {
            "workflowId": self.state.get("workflowId"),
            "action": self.state.get("action"),
            "platforms": self.state.get("platforms"),
            "status": self.state.get("status"),
            "currentPhase": self.state.get("status"),
            "executionTime": self.calculate_execution_time(),
            "metrics": self.get_metrics(),
            "completedPhases": [
                name for name, data in self.state["phases"].items()
                if data.get("status") == "complete"
            ],
            "pendingPhases": [
                name for name, data in self.state["phases"].items()
                if data.get("status") in ["pending", "in_progress"]
            ],
            "errorCount": len(self.get_errors())
        }

    def export_state(self, output_path: str) -> None:
        """
        Export state to a specific file.

        Args:
            output_path: Path to export file
        """
        with open(output_path, 'w') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def validate_state(self) -> List[str]:
        """
        Validate state file for completeness and consistency.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        required_fields = ["workflowId", "action", "platforms", "status", "phases"]
        for field in required_fields:
            if field not in self.state:
                errors.append(f"Missing required field: {field}")

        # Check workflow ID format
        workflow_id = self.state.get("workflowId", "")
        if not workflow_id.startswith("workflow-"):
            errors.append("Invalid workflow ID format")

        # Check phase statuses
        valid_statuses = ["pending", "in_progress", "complete", "error"]
        for phase_name, phase_data in self.state.get("phases", {}).items():
            status = phase_data.get("status", "")
            if status not in valid_statuses:
                errors.append(f"Invalid status for phase {phase_name}: {status}")

        # Check timestamps
        for phase_name, phase_data in self.state.get("phases", {}).items():
            if "timestamp" in phase_data:
                try:
                    datetime.fromisoformat(phase_data["timestamp"].replace("Z", "+00:00"))
                except ValueError:
                    errors.append(f"Invalid timestamp for phase {phase_name}")

        return errors
