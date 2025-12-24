# BatchRepurpose Workflow

Generate all content formats from a single blog post in one operation.

## Input

- Blog post content (from URL, file, or direct)
- Formats to generate (default: all)
- Optional: Platform-specific customizations

## Process

### Step 1: Content Analysis

1. Read the full blog post
2. Extract core message and key insights
3. Identify best hooks and examples
4. Note any visual elements or data points
5. Determine content type (tech vs personal-dev)

### Step 2: Parallel Generation

Generate all formats (can be done in parallel):

| Format | Workflow | Output File |
|--------|----------|-------------|
| X Thread | CreateXThread.md | `x-thread.md` |
| Newsletter | CreateNewsletter.md | `newsletter.md` |
| LinkedIn | CreateSummary.md | `linkedin.md` |
| YouTube Description | CreateSummary.md | `youtube-desc.md` |
| Instagram Caption | CreateSummary.md | `instagram.md` |

### Step 3: Execute Each Workflow

For each format, follow the respective workflow:
- Apply format-specific rules
- Validate output requirements
- Save to repurposed/ directory

### Step 4: Create Summary Report

Generate `repurpose-summary.json`:

```json
{
  "source": {
    "type": "url|file|content",
    "value": "source identifier",
    "title": "Post title",
    "wordCount": 1150
  },
  "generated": {
    "timestamp": "ISO timestamp",
    "formats": [
      {
        "format": "x-thread",
        "file": "x-thread.md",
        "status": "success|failed",
        "metadata": {
          "tweetCount": 8,
          "hookPreview": "First 50 chars..."
        }
      },
      {
        "format": "newsletter",
        "file": "newsletter.md",
        "status": "success",
        "metadata": {
          "wordCount": 380,
          "subjectLine": "Subject line..."
        }
      }
    ],
    "totalFormats": 5,
    "successCount": 5,
    "failedCount": 0
  },
  "distribution": {
    "platforms": ["X", "LinkedIn", "Newsletter", "YouTube", "Instagram"],
    "estimatedReach": "Calculated based on typical platform reach",
    "recommendedPostingOrder": [
      "1. LinkedIn (professional audience first)",
      "2. X Thread (engagement focused)",
      "3. Newsletter (direct to subscribers)",
      "4. YouTube (if video exists)",
      "5. Instagram (visual summary)"
    ]
  }
}
```

### Step 5: Save All Outputs

Directory structure:
```
blog-workspace/active-projects/{projectId}/repurposed/
├── x-thread.md
├── newsletter.md
├── linkedin.md
├── youtube-desc.md
├── instagram.md
└── repurpose-summary.json
```

## Validation Checklist

Before completing:
- [ ] All requested formats generated
- [ ] Each format passes its specific validation
- [ ] Summary JSON is valid
- [ ] All files saved to correct directory
- [ ] No format exceeds platform limits

## Output

Final output includes:
1. All format files in repurposed/ directory
2. Summary JSON with metadata
3. Recommended distribution order
4. Character/word counts for each format

## Example Execution

```markdown
Task: "Batch repurpose Docker MCP post to all formats"

Generating:
1. X Thread (8 tweets)... ✓
2. Newsletter (380 words)... ✓
3. LinkedIn (250 words)... ✓
4. YouTube Description (200 words)... ✓
5. Instagram Caption (120 words)... ✓

All formats saved to: blog-workspace/active-projects/proj-2025-01-15-001/repurposed/

Recommended posting order:
1. LinkedIn - Professional audience, high engagement window
2. X Thread - Best for weekday mornings
3. Newsletter - Send Tuesday-Thursday
4. YouTube - If video version exists
5. Instagram - Visual summary for broader reach
```

## Completion Signal

```
COMPLETED: [AGENT:repurposer] Batch repurpose complete - {N} formats generated, saved to repurposed/
```
