# Parallel Research Workflow

This workflow enables parallel execution of multiple researcher agents for comprehensive, multi-perspective research on blog topics.

## Research Depth Modes

| Mode | Agents | Timeout | Trigger |
|------|--------|---------|---------|
| **Quick** | 1x claude-researcher | 2 min | "quick research", tight deadline |
| **Standard** | 3 agents (claude + perplexity + gemini) | 3 min | Default for blog research |
| **Extensive** | 5-8 agents (multiple per type) | 10 min | "deep dive", "extensive research" |

## Parallel Execution Protocol

### Step 1: Determine Research Depth

Based on user request or topic complexity:
- Simple topic, known domain → Quick
- Standard blog post → Standard (default)
- Complex topic, new domain, competitive analysis → Extensive

### Step 2: Check Agent Availability

Not all researcher agents may be available. Check environment:
- `claude-researcher` - Always available (uses built-in WebSearch)
- `perplexity-researcher` - Requires Perplexity API key
- `gemini-researcher` - Requires Gemini API key

### Step 3: Prepare Query Variations

For effective parallel research, give each agent a different angle:

**Primary Agent (claude-researcher):**
- Focus: Current trends and recent developments
- Query: "{topic} 2024 2025 trends best practices"

**Secondary Agent (perplexity-researcher):**
- Focus: Technical depth and implementation details
- Query: "{topic} technical implementation guide how-to"

**Tertiary Agent (gemini-researcher):**
- Focus: Alternative perspectives and comparisons
- Query: "{topic} alternatives comparison pros cons"

### Step 4: Launch Parallel Task Tools

**CRITICAL**: All Task tool invocations must be in a SINGLE message to execute in parallel.

```markdown
## Parallel Research Launch (Single Message, Multiple Tool Calls)

Task 1:
- subagent_type: "claude-researcher"
- model: "sonnet"
- prompt: "You are claude-researcher. [AGENT:claude-researcher]

Research topic: {topic}
Focus: Current trends and recent developments
Depth: {depthMode}

Search for: '{topic} 2025 trends best practices recent'

Output format:
{
  'source': 'claude-researcher',
  'focus': 'trends',
  'findings': [...],
  'sources': [...],
  'confidence': 0-100
}

COMPLETED: [AGENT:claude-researcher] Research complete - {key finding}"

Task 2:
- subagent_type: "perplexity-researcher"
- model: "sonnet"
- prompt: "You are perplexity-researcher. [AGENT:perplexity-researcher]

Research topic: {topic}
Focus: Technical depth and implementation
Depth: {depthMode}

Search for: '{topic} technical implementation how-to guide'

Output format:
{
  'source': 'perplexity-researcher',
  'focus': 'technical',
  'findings': [...],
  'sources': [...],
  'confidence': 0-100
}

COMPLETED: [AGENT:perplexity-researcher] Research complete - {key finding}"

Task 3:
- subagent_type: "gemini-researcher"
- model: "sonnet"
- prompt: "You are gemini-researcher. [AGENT:gemini-researcher]

Research topic: {topic}
Focus: Alternative perspectives and comparisons
Depth: {depthMode}

Search for: '{topic} alternatives comparison analysis'

Output format:
{
  'source': 'gemini-researcher',
  'focus': 'comparison',
  'findings': [...],
  'sources': [...],
  'confidence': 0-100
}

COMPLETED: [AGENT:gemini-researcher] Research complete - {key finding}"
```

### Step 5: Collect Results with Timeout

Wait for all agents with mode-specific timeout:
- Quick: 2 minutes
- Standard: 3 minutes
- Extensive: 10 minutes

If some agents timeout, proceed with partial results.

### Step 6: Synthesize Results

After all agents complete (or timeout), synthesize findings:

```json
{
  "topic": "Original topic",
  "researchDepth": "standard",
  "agentsUsed": ["claude-researcher", "perplexity-researcher", "gemini-researcher"],
  "agentsCompleted": ["claude-researcher", "perplexity-researcher"],
  "agentsTimedOut": ["gemini-researcher"],
  "synthesizedFindings": {
    "trends": [...],
    "technical": [...],
    "comparisons": [...],
    "challenges": [...],
    "opportunities": [...]
  },
  "sources": [
    { "url": "...", "title": "...", "credibility": "high|medium|low" }
  ],
  "overallConfidence": 85,
  "researchedAt": "ISO timestamp"
}
```

### Step 7: Save Outputs

Write to project workspace:
1. `research-findings.json` - Synthesized findings for blog-insight-synthesizer
2. `research-notes.md` - Detailed markdown notes with sources
3. `research-raw/` - Raw output from each agent (optional)

## Extensive Research: Additional Angles

For extensive research mode, add more specialized queries:

**Agent 4 (claude-researcher #2):**
- Focus: Case studies and real-world examples
- Query: "{topic} case study success story example"

**Agent 5 (perplexity-researcher #2):**
- Focus: Challenges and pitfalls
- Query: "{topic} challenges problems pitfalls mistakes"

**Agent 6 (gemini-researcher #2):**
- Focus: Future predictions and emerging trends
- Query: "{topic} future 2025 2026 predictions emerging"

**Agent 7 (claude-researcher #3):**
- Focus: Community discussions and opinions
- Query: "{topic} reddit discussion opinions forum"

**Agent 8 (perplexity-researcher #3):**
- Focus: Statistics and data
- Query: "{topic} statistics data research study"

## Error Handling

### Agent Unavailable
If a researcher agent is not configured (missing API key):
- Log warning
- Skip that agent
- Proceed with available agents
- Note limitation in research-findings.json

### Agent Timeout
If an agent exceeds timeout:
- Cancel the agent task
- Use partial results if available
- Mark as "timed_out" in results
- Proceed with other agents' findings

### All Agents Fail
If all agents fail or timeout:
- Retry with single claude-researcher (always available)
- Use basic web search as fallback
- Alert user to limited research depth

## Integration with blog-master-orchestrator

When the orchestrator invokes Phase 1 (Research):

```markdown
Task prompt: "You are blog-trend-researcher. [AGENT:researcher]

## Project Context
- Project ID: {projectId}
- Topic: {topic}
- Content Type: {contentType}
- Workspace: {workspacePath}

## Research Instructions
Execute parallel research using the ParallelResearch.md workflow.

Research Depth: {quick|standard|extensive}

1. Determine research depth from topic complexity
2. Check available researcher agents
3. Launch parallel Task tools with different query angles
4. Collect results with appropriate timeout
5. Synthesize findings into unified format
6. Save research-findings.json and research-notes.md

COMPLETED: [AGENT:researcher] Research complete - {summary of sources and key findings}"
```

## Output Schema: research-findings.json

```json
{
  "meta": {
    "topic": "string",
    "contentType": "tech|personal-dev",
    "researchDepth": "quick|standard|extensive",
    "researchedAt": "ISO timestamp",
    "totalSources": 0,
    "overallConfidence": 85
  },
  "agents": {
    "used": ["claude-researcher", "perplexity-researcher"],
    "completed": ["claude-researcher", "perplexity-researcher"],
    "timedOut": [],
    "failed": []
  },
  "findings": {
    "trends": [
      {
        "trend": "Description",
        "evidence": "Supporting data",
        "sources": ["url1", "url2"],
        "confidence": 90
      }
    ],
    "challenges": [...],
    "opportunities": [...],
    "technicalInsights": [...],
    "caseStudies": [...],
    "statistics": [...]
  },
  "sources": [
    {
      "url": "https://...",
      "title": "Source title",
      "domain": "example.com",
      "type": "article|documentation|forum|study",
      "credibility": "high|medium|low",
      "citedBy": ["claude-researcher"]
    }
  ],
  "keyTakeaways": [
    "Takeaway 1",
    "Takeaway 2",
    "Takeaway 3"
  ]
}
```
