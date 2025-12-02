# blog-master-orchestrator

Central workflow coordinator managing the entire blog writing pipeline.

## Overview

The **blog-master-orchestrator** is the central command center of the blog writing system. It coordinates all 8 agents, manages state, handles errors, and ensures smooth execution from topic to published post.

## Core Responsibilities

1. **Workflow Orchestration**
   - Coordinates 7 specialized subagents in sequence
   - Manages phase transitions and dependencies
   - Validates outputs before proceeding

2. **State Management**
   - Tracks progress through 6 workflow phases
   - Maintains comprehensive metadata
   - Enables resume and retry capabilities

3. **Error Handling**
   - Implements retry logic (3 attempts per phase)
   - Logs errors for debugging
   - Escalates persistent failures

4. **Publishing Control**
   - Manages dual publishing modes (markdown/API)
   - Coordinates with sanity-publisher
   - Archives completed projects

## Workflow Phases

### Phase Sequence

```
Initialization → Research → Synthesis → Writing → SEO → Review → Publishing
```

### Phase Details

| Phase | Agent | Duration | Output |
|-------|-------|----------|--------|
| 0 | Orchestrator | 30s | Project setup, state.json |
| 1 | blog-trend-researcher | 5 min | research-findings.json |
| 2 | blog-insight-synthesizer | 3 min | content-outline.md |
| 3 | tech/personal-dev writer | 10 min | draft-[type].md |
| 4 | seo-content-optimizer | 5 min | seo-optimized-draft.md |
| 5 | style-guardian | 5 min | polished-draft.md |
| 6 | sanity-publisher | 2 min | Published/Sanity-ready |

## Input Specification

### Required Parameters

```json
{
  "topic": "Blog post topic (min 3 characters)",
  "contentType": "tech | personal-dev",
  "publishingMode": "markdown | api | ask-user"
}
```

### Validation Rules

- **Topic:** Non-empty, at least 3 characters
- **Content Type:** Must be "tech" or "personal-dev"
- **Publishing Mode:** Must be "markdown", "api", or "ask-user"

## State Management

### state.json Structure

```json
{
  "projectId": "proj-2025-01-15-143022",
  "topic": "User-specified topic",
  "contentType": "tech|personal-dev",
  "publishingMode": "markdown|api|ask-user",
  "status": "current_phase",
  "createdAt": "ISO timestamp",
  "author": "Thuong-Tuan Tran",
  "brandVoice": "Professional & Friendly",
  "phases": {
    "initialization": {
      "status": "complete|in_progress|pending|error",
      "output": "state.json",
      "timestamp": "ISO timestamp"
    },
    "research": { "status": "...", "output": "research-findings.json" },
    "synthesis": { "status": "...", "output": "content-outline.md" },
    "writing": { "status": "...", "output": "draft-[type].md" },
    "seo": { "status": "...", "output": "seo-optimized-draft.md" },
    "review": { "status": "...", "output": "polished-draft.md" },
    "publishing": { "status": "...", "output": "sanity-ready-post.md" }
  },
  "metadata": {
    "wordCount": 0,
    "seoScore": 0,
    "styleScore": 0,
    "errors": []
  }
}
```

### Phase Status Values

- `pending` - Phase not started
- `in_progress` - Phase currently executing
- `complete` - Phase finished successfully
- `error` - Phase failed with errors

## Error Handling

### Retry Logic

- **Max Attempts:** 3 retries per phase
- **Retry Delay:** 5 seconds between attempts
- **Escalation:** After 3 failures, mark as error and halt

### Error Logging

All errors logged to `state.json.metadata.errors`:

```json
{
  "errors": [
    {
      "timestamp": "2025-01-15T14:30:22.000Z",
      "phase": "writing",
      "error": "KeyError: 'content-type'",
      "attempt": 2
    }
  ]
}
```

### Error Recovery

1. **Phase Failure:**
   - Log error with full context
   - Retry up to 3 times
   - If exhausted, mark as error
   - Halt workflow (requires manual intervention)

2. **Input Validation Failure:**
   - Exit immediately with error code
   - Display helpful error message
   - Provide usage instructions

3. **File System Errors:**
   - Check permissions and disk space
   - Attempt to create directories
   - Retry operation

## Script Usage

### orchestrate_workflow.py

Main workflow execution script.

**Basic Usage:**

```bash
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Your Topic" \
  --type tech \
  --mode ask-user
```

**Parameters:**

- `--topic` (required): Blog post topic
- `--type` (required): Content type (`tech` or `personal-dev`)
- `--mode` (required): Publishing mode (`markdown`, `api`, or `ask-user`)

**Examples:**

```bash
# Tech post with markdown output
python orchestrate_workflow.py \
  --topic "Building Scalable React Applications" \
  --type tech \
  --mode markdown

# Personal dev post with API publishing
python orchestrate_workflow.py \
  --topic "5 Lessons from My First Year" \
  --type personal-dev \
  --mode api

# Ask user for publishing mode
python orchestrate_workflow.py \
  --topic "TypeScript Tips" \
  --type tech \
  --mode ask-user
```

### state_manager.py

Utility for managing workflow state.

**View State:**

```bash
python .claude/skills/blog-master-orchestrator/scripts/state_manager.py proj-2025-01-15-143022
```

**StateManager Class:**

```python
from state_manager import StateManager, get_state_manager

# Create manager
manager = get_state_manager("proj-2025-01-15-143022")

# Read state
state = manager.read_state()

# Update phase
manager.update_phase("writing", "in_progress")

# Check completion
is_complete = manager.is_phase_complete("research")

# Get next phase
next_phase = manager.get_next_phase()

# Archive project
archive_path = manager.archive_project()
```

## Output Artifacts

### Project Structure

```
blog-workspace/
├── active-projects/PROJECT_ID/
│   ├── state.json
│   ├── research-findings.json
│   ├── research-notes.md
│   ├── content-outline.md
│   ├── draft-tech.md or draft-personal-dev.md
│   ├── seo-metadata.json
│   ├── seo-optimized-draft.md
│   ├── style-report.md
│   ├── polished-draft.md
│   └── sanity-ready-post.md (or publishing-response.json)
└── archive/PROJECT_ID/ (after completion)
```

### Primary Outputs

1. **state.json** - Complete workflow state and metadata
2. **sanity-ready-post.md** - Final formatted output (markdown mode)
3. **publishing-response.json** - API publishing confirmation (API mode)

### Quality Reports

- **seo-metadata.json** - SEO optimization metrics
- **style-report.md** - Style and brand voice analysis

## Dependencies

The orchestrator depends on these agents:

1. **blog-trend-researcher** - Research phase
2. **blog-insight-synthesizer** - Synthesis phase
3. **tech-blogger-writer** - Writing phase (tech content)
4. **personal-dev-writer** - Writing phase (personal dev content)
5. **seo-content-optimizer** - SEO optimization phase
6. **style-guardian** - Style review phase
7. **sanity-publisher** - Publishing phase

## Validation Checkpoints

### Before Each Phase

1. Check previous phase output exists
2. Validate output file format
3. Verify required data present
4. Update state.json status

### After Each Phase

1. Mark phase as complete
2. Set next phase to pending
3. Log completion timestamp
4. Check for errors

## Monitoring & Metrics

### Tracked Metrics

- **Execution Time** - Per phase and total
- **Quality Scores** - SEO and style scores
- **Error Rate** - Phase failures and types
- **Word Count** - Final content length
- **Publishing Mode** - User preferences

### Success Criteria

- All 6 phases complete successfully
- SEO score ≥ 70
- Style score ≥ 80
- No critical errors
- Content meets word count targets

## Customization

### Extending Workflow

To add a new phase:

1. Define phase in state.json structure
2. Add to phase sequence
3. Create agent for phase
4. Add validation checkpoint
5. Update error handling

### Modifying Error Handling

```python
# In orchestrate_workflow.py

# Custom retry logic
if attempt < max_retries:
    if error_type == "network":
        sleep_time = 10  # Longer retry for network
    else:
        sleep_time = 5
    time.sleep(sleep_time)
```

### Adding Validation Rules

```python
# Custom input validation
def validate_topic(topic):
    if len(topic) < 10:
        raise ValueError("Topic should be more descriptive (min 10 chars)")
    if topic.isdigit():
        raise ValueError("Topic should not be just numbers")
    return True
```

## Best Practices

### State Management

1. Always update state after phase completion
2. Log timestamps for all state changes
3. Validate state before resuming
4. Archive projects after completion

### Error Handling

1. Log errors with full context
2. Provide helpful error messages
3. Retry transient failures
4. Escalate persistent issues

### Performance

1. Parallel validation where possible
2. Minimize file I/O operations
3. Cache frequently accessed data
4. Clean up temporary files

### Reliability

1. Validate inputs before processing
2. Check outputs before proceeding
3. Implement comprehensive logging
4. Test all error paths

## Troubleshooting

### Common Issues

**"State file not found"**
- Check project directory exists
- Verify project ID is correct
- Look in archive if completed

**"Phase already in progress"**
- Project may be running in another session
- Check for stale lock files
- Manually reset state if needed

**"Workflow won't proceed"**
- Check previous phase is marked complete
- Verify output file exists and is valid
- Review errors in state.json

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Related Documentation

- [Workflow Guide](../guides/workflow.md) - Complete workflow overview
- [State Management](../guides/state-management.md) - Detailed state tracking
- [Troubleshooting](../guides/troubleshooting.md) - Common issues and solutions

---

**Agent Version:** 1.0.0
**Author:** Thuong-Tuan Tran
**Last Updated:** 2025-12-02
