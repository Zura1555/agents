#!/usr/bin/env python3
"""
State Manager - Helper utility for managing workflow state

Provides functions to read, update, and validate workflow state.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

class StateManager:
    """Manages workflow state across blog writing agents."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.state_file = self._get_state_file()

    def _get_state_file(self) -> Path:
        """Get path to state file."""
        return Path(__file__).parent.parent.parent.parent / \
               "blog-workspace" / "active-projects" / self.project_id / "state.json"

    def read_state(self) -> Dict[str, Any]:
        """Read current state."""
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        with open(self.state_file, 'r') as f:
            return json.load(f)

    def update_phase(self, phase: str, status: str, output: Optional[str] = None):
        """Update a phase status."""
        state = self.read_state()

        if phase not in state["phases"]:
            raise ValueError(f"Invalid phase: {phase}")

        state["phases"][phase]["status"] = status
        if output:
            state["phases"][phase]["output"] = output

        state["status"] = phase
        state["updatedAt"] = datetime.now().isoformat()

        self._write_state(state)

    def update_metadata(self, key: str, value: Any):
        """Update metadata field."""
        state = self.read_state()
        state["metadata"][key] = value
        self._write_state(state)

    def add_error(self, phase: str, error: str):
        """Add error to state."""
        state = self.read_state()

        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "error": error
        }

        state["metadata"]["errors"].append(error_entry)
        self._write_state(state)

    def get_phase_output(self, phase: str) -> Optional[str]:
        """Get output file for a phase."""
        state = self.read_state()
        return state["phases"].get(phase, {}).get("output")

    def is_phase_complete(self, phase: str) -> bool:
        """Check if a phase is complete."""
        state = self.read_state()
        status = state["phases"].get(phase, {}).get("status")
        return status == "complete"

    def get_next_phase(self) -> Optional[str]:
        """Get the next phase to execute."""
        state = self.read_state()

        for phase_name, phase_data in state["phases"].items():
            if phase_data["status"] == "pending":
                return phase_name

        return None

    def get_completed_phases(self) -> List[str]:
        """Get list of completed phases."""
        state = self.read_state()
        return [name for name, data in state["phases"].items()
                if data["status"] == "complete"]

    def _write_state(self, state: Dict[str, Any]):
        """Write state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def validate_state(self) -> Dict[str, Any]:
        """Validate state integrity."""
        state = self.read_state()
        errors = []

        # Check required fields
        required_fields = ["projectId", "topic", "contentType", "status", "phases"]
        for field in required_fields:
            if field not in state:
                errors.append(f"Missing required field: {field}")

        # Check phases
        required_phases = ["initialization", "research", "synthesis", "writing", "seo", "review", "publishing"]
        for phase in required_phases:
            if phase not in state["phases"]:
                errors.append(f"Missing phase: {phase}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def archive_project(self):
        """Archive project to completed projects."""
        active_path = self.state_file.parent
        archive_path = Path(__file__).parent.parent.parent.parent / \
                      "blog-workspace" / "archive" / self.project_id

        if archive_path.exists():
            import shutil
            shutil.rmtree(archive_path)

        shutil.move(str(active_path), str(archive_path))
        return archive_path

# Convenience functions

def get_state_manager(project_id: str) -> StateManager:
    """Get a StateManager instance."""
    return StateManager(project_id)

def create_initial_state(project_id: str, topic: str, content_type: str, publishing_mode: str) -> Dict[str, Any]:
    """Create initial state."""
    state = {
        "projectId": project_id,
        "topic": topic,
        "contentType": content_type,
        "publishingMode": publishing_mode,
        "status": "initialization",
        "createdAt": datetime.now().isoformat(),
        "author": "Thuong-Tuan Tran",
        "brandVoice": "Professional & Friendly",
        "phases": {
            "initialization": {"status": "complete", "output": "state.json"},
            "research": {"status": "pending", "output": "research-findings.json"},
            "synthesis": {"status": "pending", "output": "content-outline.md"},
            "writing": {"status": "pending", "output": f"draft-{content_type}.md"},
            "seo": {"status": "pending", "output": "seo-optimized-draft.md"},
            "review": {"status": "pending", "output": "polished-draft.md"},
            "publishing": {"status": "pending", "output": "sanity-ready-post.md"}
        },
        "metadata": {
            "wordCount": 0,
            "seoScore": 0,
            "styleScore": 0,
            "errors": []
        }
    }

    manager = StateManager(project_id)
    state_file = manager.state_file
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

    return state

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python state_manager.py <project_id>")
        sys.exit(1)

    project_id = sys.argv[1]
    manager = StateManager(project_id)

    try:
        state = manager.read_state()
        print(json.dumps(state, indent=2))

        validation = manager.validate_state()
        print("\nValidation:")
        print(json.dumps(validation, indent=2))

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
