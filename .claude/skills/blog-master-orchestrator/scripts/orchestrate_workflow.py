#!/usr/bin/env python3
"""
Blog Master Orchestrator - Workflow Script

This script orchestrates the entire blog writing workflow by:
1. Initializing a new blog project
2. Coordinating all 7 subagents in sequence
3. Managing state and tracking progress
4. Handling errors and retries
5. Producing final published output

Usage:
    python orchestrate_workflow.py --topic "Your Topic" --type tech --mode ask-user
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def generate_project_id() -> str:
    """Generate unique project ID based on date and sequence."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    sequence = datetime.now().strftime("%H%M%S")
    return f"proj-{date_str}-{sequence}"

def create_project_structure(project_id: str) -> Path:
    """Create project directory structure."""
    workspace = PROJECT_ROOT / "blog-workspace" / "active-projects" / project_id
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace

def initialize_state(project_id: str, topic: str, content_type: str, publishing_mode: str, workspace: Path) -> Dict[str, Any]:
    """Initialize workflow state."""
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

    state_file = workspace / "state.json"
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

    print(f"[OK] Initialized project {project_id}")
    return state

def validate_input(topic: str, content_type: str, publishing_mode: str) -> bool:
    """Validate user input."""
    if not topic or len(topic.strip()) < 3:
        print("[ERROR] Topic must be at least 3 characters")
        return False

    if content_type not in ["tech", "personal-dev"]:
        print("[ERROR] Content type must be 'tech' or 'personal-dev'")
        return False

    if publishing_mode not in ["markdown", "api", "ask-user"]:
        print("[ERROR] Publishing mode must be 'markdown', 'api', or 'ask-user'")
        return False

    return True

def update_phase_status(state: Dict[str, Any], phase: str, status: str, output: Optional[str] = None):
    """Update phase status in state."""
    state["phases"][phase]["status"] = status
    if output:
        state["phases"][phase]["output"] = output
    state["status"] = phase

    state_file = PROJECT_ROOT / "blog-workspace" / "active-projects" / state["projectId"] / "state.json"
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def log_error(state: Dict[str, Any], phase: str, error: str):
    """Log error to state."""
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "error": error
    }
    state["metadata"]["errors"].append(error_entry)

    state_file = PROJECT_ROOT / "blog-workspace" / "active-projects" / state["projectId"] / "state.json"
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def run_phase(state: Dict[str, Any], phase: str, agent_name: str, input_data: Dict[str, Any], max_retries: int = 3) -> bool:
    """Run a single workflow phase with retry logic."""
    workspace = PROJECT_ROOT / "blog-workspace" / "active-projects" / state["projectId"]

    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n{'='*60}")
            print(f"Phase: {phase} (Attempt {attempt}/{max_retries})")
            print(f"Agent: {agent_name}")
            print(f"{'='*60}")

            update_phase_status(state, phase, "in_progress")

            # Check if output file already exists (skip if complete)
            expected_output = state["phases"][phase].get("output")
            if expected_output:
                output_path = workspace / expected_output
                if output_path.exists() and output_path.stat().st_size > 0:
                    print(f"[OK] Output file already exists, skipping phase")
                    update_phase_status(state, phase, "complete")
                    return True

            # Execute agent (in real implementation, this would call the actual agent)
            print(f"Executing {agent_name}...")
            print(f"Input: {json.dumps(input_data, indent=2)}")

            # Simulate agent execution
            # TODO: Replace with actual agent execution
            # This would typically involve:
            # 1. Loading the agent skill
            # 2. Providing it with the input data
            # 3. Capturing its output
            # 4. Validating the output

            update_phase_status(state, phase, "complete")
            print(f"[OK] Phase {phase} completed successfully")
            return True

        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Error in phase {phase} (attempt {attempt}): {error_msg}")
            log_error(state, phase, error_msg)

            if attempt < max_retries:
                print(f"Retrying in 5 seconds...")
                import time
                time.sleep(5)
            else:
                print(f"[ERROR] Phase {phase} failed after {max_retries} attempts")
                update_phase_status(state, phase, "error")
                return False

    return False

def execute_workflow(topic: str, content_type: str, publishing_mode: str) -> bool:
    """Execute the complete blog writing workflow."""
    print("\n" + "="*60)
    print("BLOG MASTER ORCHESTRATOR - WORKFLOW START")
    print("="*60)

    # Initialize
    project_id = generate_project_id()
    workspace = create_project_structure(project_id)
    state = initialize_state(project_id, topic, content_type, publishing_mode, workspace)

    print(f"\nProject ID: {project_id}")
    print(f"Workspace: {workspace}")
    print(f"Content Type: {content_type}")
    print(f"Publishing Mode: {publishing_mode}")

    # Ask user for publishing mode if needed
    if publishing_mode == "ask-user":
        print("\nChoose publishing mode:")
        print("1. Markdown Output (manual copy-paste)")
        print("2. Direct API Publishing (automated)")
        choice = input("\nEnter choice (1 or 2): ").strip()
        publishing_mode = "api" if choice == "2" else "markdown"
        update_phase_status(state, "initialization", "complete")

    # Workflow phases
    phases = [
        ("research", "blog-trend-researcher", {"topic": topic, "contentType": content_type}),
        ("synthesis", "blog-insight-synthesizer", {"contentType": content_type}),
        ("writing", f"{'tech-blogger-writer' if content_type == 'tech' else 'personal-dev-writer'}", {}),
        ("seo", "seo-content-optimizer", {}),
        ("review", "style-guardian", {}),
        ("publishing", "sanity-publisher", {"publishingMode": publishing_mode})
    ]

    # Execute phases sequentially
    for phase_name, agent_name, phase_input in phases:
        success = run_phase(state, phase_name, agent_name, phase_input)
        if not success:
            print(f"\n[ERROR] Workflow failed at phase: {phase_name}")
            print(f"Check {workspace}/state.json for details")
            return False

    # Archive completed project
    archive_path = PROJECT_ROOT / "blog-workspace" / "archive" / project_id
    workspace.rename(archive_path)

    print("\n" + "="*60)
    print("WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nProject archived to: {archive_path}")
    print(f"\nFinal deliverables:")
    for phase_name in ["research", "synthesis", "writing", "seo", "review", "publishing"]:
        output_file = state["phases"][phase_name].get("output", "N/A")
        print(f"  - {phase_name}: {output_file}")

    return True

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Orchestrate blog writing workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python orchestrate_workflow.py --topic "React Hooks Guide" --type tech --mode ask-user
    python orchestrate_workflow.py --topic "Morning Routines" --type personal-dev --mode markdown
    python orchestrate_workflow.py --topic "TypeScript Tips" --type tech --mode api
        """
    )

    parser.add_argument("--topic", required=True, help="Blog post topic")
    parser.add_argument("--type", required=True, choices=["tech", "personal-dev"], help="Content type")
    parser.add_argument("--mode", required=True, choices=["markdown", "api", "ask-user"], help="Publishing mode")

    args = parser.parse_args()

    # Validate input
    if not validate_input(args.topic, args.type, args.mode):
        sys.exit(1)

    # Execute workflow
    success = execute_workflow(args.topic.strip(), args.type, args.mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
