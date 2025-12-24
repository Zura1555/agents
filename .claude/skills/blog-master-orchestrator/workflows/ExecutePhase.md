# Execute Phase Workflow

This workflow defines how the Blog Master Orchestrator spawns and manages subagents using Claude's Task tool for real multi-agent execution.

## Task Tool Invocation Protocol

For each workflow phase, the orchestrator:
1. Reads current `state.json` to get project context
2. Prepares phase-specific prompt with full context
3. Invokes Task tool with the appropriate skill type
4. Monitors for completion (SubagentStop hook event)
5. Validates output file exists and meets requirements
6. Updates `state.json` with phase status
7. Proceeds to next phase or handles error

## Agent Prompt Templates

### Phase 1: Research

```markdown
Task tool invocation:
- subagent_type: "researcher"
- model: "sonnet" (or "haiku" for quick research)

Prompt:
"You are blog-trend-researcher. [AGENT:researcher]

## Project Context
- Project ID: {projectId}
- Topic: {topic}
- Content Type: {contentType}
- Workspace: {workspacePath}

## Your Mission
Execute comprehensive research on the topic following the blog-trend-researcher SKILL.md methodology.

## Required Outputs
Save to workspace directory:
1. `research-findings.json` - Structured research data with:
   - Current trends and patterns
   - Key challenges and opportunities
   - Supporting data and statistics
   - Source documentation with credibility scores

2. `research-notes.md` - Detailed markdown notes

## Completion Signal
When complete, end with:
COMPLETED: [AGENT:researcher] Research complete - {brief summary of key findings}"
```

### Phase 2: Synthesis

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "sonnet"

Prompt:
"You are blog-insight-synthesizer. [AGENT:synthesizer]

## Project Context
- Project ID: {projectId}
- Content Type: {contentType}
- Workspace: {workspacePath}

## Input
Read: `{workspacePath}/research-findings.json`

## Your Mission
Transform research findings into a structured content outline following blog-insight-synthesizer SKILL.md methodology.

## Required Outputs
Save to workspace directory:
1. `content-outline.md` - Comprehensive outline with:
   - Logical section flow
   - Word count targets per section
   - Key messages for each section
   - Visual element suggestions (tables, images)
   - Hook and conclusion strategy

## Completion Signal
COMPLETED: [AGENT:synthesizer] Outline complete - {number} sections, {estimated word count} words"
```

### Phase 3: Writing (Tech)

```markdown
Task tool invocation:
- subagent_type: "writer"
- model: "sonnet"

Prompt:
"You are tech-blogger-writer. [AGENT:writer-tech]

## Project Context
- Project ID: {projectId}
- Workspace: {workspacePath}
- Target: 1000-1200 words (5-7 minute read)
- Brand Voice: Professional, Friendly, Authentic

## Input
Read: `{workspacePath}/content-outline.md`

## Your Mission
Write a compelling technical blog post following tech-blogger-writer SKILL.md methodology.

## Required Outputs
Save to workspace directory:
1. `draft-tech.md` - Complete blog draft with:
   - Engaging hook introduction
   - Problem-solution framework
   - Code examples with explanations
   - Do's/Don'ts sections
   - Clear, actionable conclusion

2. `draft-metadata.json` - Writing quality metrics

## Completion Signal
COMPLETED: [AGENT:writer-tech] Draft complete - {word count} words, {reading time} min read"
```

### Phase 3: Writing (Personal Dev)

```markdown
Task tool invocation:
- subagent_type: "writer"
- model: "sonnet"

Prompt:
"You are personal-dev-writer. [AGENT:writer-personal]

## Project Context
- Project ID: {projectId}
- Workspace: {workspacePath}
- Target: 1200-1500 words (6-8 minute read)
- Brand Voice: Professional, Friendly, Authentic

## Input
Read: `{workspacePath}/content-outline.md`

## Your Mission
Write an inspirational personal development blog post following personal-dev-writer SKILL.md methodology.

## Required Outputs
Save to workspace directory:
1. `draft-personal-dev.md` - Complete blog draft using:
   - STORY framework (Situation, Trial, Outcome, Resolution, Yield)
   - Personal anecdotes and case studies
   - Reflection questions
   - Action steps

2. `draft-metadata.json` - Emotional journey tracking

## Completion Signal
COMPLETED: [AGENT:writer-personal] Draft complete - {word count} words, {reading time} min read"
```

### Phase 4: SEO Optimization

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "sonnet"

Prompt:
"You are seo-content-optimizer. [AGENT:seo]

## Project Context
- Project ID: {projectId}
- Content Type: {contentType}
- Workspace: {workspacePath}

## Input
Read: `{workspacePath}/draft-{contentType}.md`

## Your Mission
Optimize content for SEO following seo-content-optimizer SKILL.md methodology.

## CRITICAL Character Limits (MUST VALIDATE)
- Meta Title: 50-60 characters (HARD LIMIT)
- Meta Description: 150-160 characters (HARD LIMIT)
- OG Description: 100-120 characters (HARD LIMIT)

## Required Outputs
Save to workspace directory:
1. `seo-optimized-draft.md` - SEO-enhanced content with:
   - Primary keyword in title, H1, first 100 words
   - Secondary keywords in subheadings
   - Internal/external link suggestions

2. `seo-metadata.json` - Complete SEO schema:
   - title, metaDescription, ogDescription (with char counts)
   - keywords (primary, secondary, LSI, long-tail)
   - openGraph object (title, description, type, image)
   - twitter object (card, title, description, image)
   - Overall SEO score (target: 85+)

## Validation Before Completion
Count characters and ONLY complete if:
- metaTitle.length >= 50 && <= 60
- metaDescription.length >= 150 && <= 160
- ogDescription.length >= 100 && <= 120

## Completion Signal
COMPLETED: [AGENT:seo] SEO complete - Score: {score}/100, all limits valid"
```

### Phase 4.5: Image Generation

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "sonnet"

Prompt:
"You are blog-image-generator. [AGENT:image-generator]

## Project Context
- Project ID: {projectId}
- Content Type: {contentType}
- Workspace: {workspacePath}
- Image Model: {imageModel} (default: nano-banana, alternative: flux)

## Input
Read:
- `{workspacePath}/seo-optimized-draft.md`
- `{workspacePath}/seo-metadata.json`

## Your Mission
Generate cover image and section images for this blog post using the Art skill BlogImages workflow.

## Step 1: Content Analysis
Parse the blog draft and extract:
1. **Title** - The blog post title
2. **Core Thesis** - First 2-3 sentences summarizing the main argument
3. **Key Themes** - 3-5 dominant concepts/topics
4. **Content Type** - tech or personal-dev (affects visual tone)
5. **Image Placeholders** - All placeholder blocks in format:
   ```
   **Suggested Image Placeholder**
   - **Type**: [type]
   - **Description**: [description]
   ```

## Step 2: Cover Image Generation
Create visual metaphor for the core thesis:

1. Derive 2-3 PHYSICAL elements that represent the thesis
   - Use recognizable objects (scissors, hands, puzzle pieces, mountains)
   - Show clear action (cutting, reaching, assembling)
   - Pass "Instant Picture Test" - can picture it like a photograph

2. Construct prompt following Anthropic editorial aesthetic:
   - Saul Steinberg / New Yorker style
   - Hand-drawn black ink linework
   - WHITE background for transparency
   - Purple (#4A148C) and Teal (#00796B) accents
   - NO gradients, NO shadows

3. Create images directory:
   ```bash
   mkdir -p {workspacePath}/images
   ```

4. Generate cover image:
   ```bash
   bun run ${PAI_DIR}/skills/art/tools/generate-ulart-image.ts \
     --model {imageModel} \
     --prompt "[COVER PROMPT]" \
     --size 16:9 \
     --output {workspacePath}/images/cover.png \
     --remove-bg
   ```

## Step 3: Section Image Generation
For each image placeholder found:

1. Analyze placeholder type (infographic, diagram, illustration, etc.)
2. Skip "screenshot" type - requires actual screenshot
3. Construct section-specific prompt matching placeholder description
4. Generate section image:
   ```bash
   bun run ${PAI_DIR}/skills/art/tools/generate-ulart-image.ts \
     --model {imageModel} \
     --prompt "[SECTION PROMPT]" \
     --size 16:9 \
     --output {workspacePath}/images/section-{n}.png \
     --remove-bg
   ```

## Step 4: Create Image Manifest
Save `{workspacePath}/image-manifest.json`:

```json
{
  "generatedAt": "[ISO timestamp]",
  "model": "{imageModel}",
  "cover": {
    "path": "images/cover.png",
    "alt": "[Descriptive alt text for cover]",
    "caption": "[Optional caption]",
    "dimensions": { "width": 1200, "height": 675 },
    "prompt": "[The prompt used]"
  },
  "sections": [
    {
      "index": 1,
      "placeholderId": "placeholder-1",
      "type": "[placeholder type]",
      "path": "images/section-1.png",
      "alt": "[Alt text from placeholder]",
      "caption": "[Caption from placeholder]",
      "dimensions": { "width": 1200, "height": 675 }
    }
  ],
  "stats": {
    "totalImages": "[count]",
    "coverGenerated": true,
    "sectionsGenerated": "[count]",
    "skipped": "[count]",
    "skippedReason": ["screenshot type - requires actual screenshot"]
  }
}
```

## Error Handling
If image generation fails:
1. Log error but continue with remaining images
2. Mark failed image with error in manifest:
   ```json
   {
     "cover": {
       "path": null,
       "error": "[error message]",
       "attemptedPrompt": "[prompt]"
     }
   }
   ```
3. Pipeline continues - images are optional

## Validation Before Completion
- [ ] images/ directory created
- [ ] cover.png exists (or error logged)
- [ ] image-manifest.json is valid JSON
- [ ] All generated images have alt text

## Completion Signal
COMPLETED: [AGENT:image-generator] Images complete - cover + {n} sections generated"
```

### Phase 5: Style Review

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "sonnet"

Prompt:
"You are style-guardian. [AGENT:style]

## Project Context
- Project ID: {projectId}
- Workspace: {workspacePath}
- Brand Voice: Professional, Friendly, Authentic

## Input
Read:
- `{workspacePath}/seo-optimized-draft.md`
- `{workspacePath}/seo-metadata.json`

## Your Mission
Ensure brand consistency and style quality following style-guardian SKILL.md methodology.

## Scoring Criteria (100 points)
- Brand Voice: 25 pts
- Clarity: 25 pts
- Structure: 20 pts
- Engagement: 15 pts
- Visual Enhancement: 10 pts
- Quality: 5 pts

## Required Outputs
Save to workspace directory:
1. `polished-draft.md` - Style-compliant content with:
   - Consistent brand voice throughout
   - Optimized readability
   - Strong 7-section structure
   - Concise conclusion (max 2-3 paragraphs)

2. `style-report.md` - Detailed style analysis with:
   - Score breakdown by category
   - Issues found and fixes applied
   - Recommendations for future posts

## Completion Signal
COMPLETED: [AGENT:style] Style review complete - Score: {score}/100"
```

### Phase 6: Publishing

```markdown
Task tool invocation:
- subagent_type: "general-purpose"
- model: "sonnet"

Prompt:
"You are sanity-publisher. [AGENT:publisher]

## Project Context
- Project ID: {projectId}
- Publishing Mode: {publishingMode}
- Workspace: {workspacePath}

## Input
Read:
- `{workspacePath}/polished-draft.md`
- `{workspacePath}/seo-metadata.json`

## Your Mission
Prepare and optionally publish content to Sanity CMS following sanity-publisher SKILL.md methodology.

## CRITICAL: Complete Schema Population
You MUST populate ALL fields on first attempt:
- Core: title, slug, content, excerpt, coverImage
- Metadata: publishedAt, date, status, readingTime, wordCount
- References: author (_ref), categories (array of _refs)
- SEO: Complete seo object with openGraph and twitter sub-objects

## Required Outputs

### If publishingMode == 'markdown':
Save to workspace:
1. `sanity-ready-post.md` - YAML frontmatter + content for manual import

### If publishingMode == 'api':
1. Call Sanity API to create/publish document
2. Save `publish-result.json` with document ID and URL

### If publishingMode == 'ask-user':
Ask user which mode to use, then proceed accordingly

## Validation Before Completion
- All schema fields populated
- Character limits still valid
- Author and category references valid

## Completion Signal
COMPLETED: [AGENT:publisher] Published - {mode}: {url or file path}"
```

### Phase 7: Social Promotion

```markdown
Task tool invocation:
- subagent_type: "writer"
- model: "sonnet"

Prompt:
"You are social-media-promoter. [AGENT:promoter]

## Project Context
- Project ID: {projectId}
- Published URL: {publishedUrl}
- Workspace: {workspacePath}

## Input
Read published post content from Sanity or local file

## Discovery Questions (ASK USER FIRST)
Before generating posts, ask user:
1. How did you first encounter this topic?
2. What personal experience or story relates to this?
3. Any specific angle you want to highlight?

## Your Mission
Generate social media posts following social-media-promoter SKILL.md methodology.

## Required Outputs
Save to workspace directory:
1. `social-posts.md` containing:

### LinkedIn Post (150-300 words)
- Personal story opening
- Key insights from blog
- Thought-provoking closing question
- NO hashtags, NO CTAs
- Max 2 emojis (optional)

### X Tweet (max 280 characters)
- Hook + insight + question
- NO hashtags
- Link to post

## Completion Signal
COMPLETED: [AGENT:promoter] Social posts ready - LinkedIn: {word count}w, X: {char count}c"
```

## State Transitions

After each phase completion:

```javascript
// Update state.json
const updatedState = {
  ...currentState,
  status: nextPhaseName,
  phases: {
    ...currentState.phases,
    [currentPhase]: {
      status: "complete",
      output: outputFileName,
      completedAt: new Date().toISOString()
    },
    [nextPhase]: {
      status: "in_progress",
      startedAt: new Date().toISOString()
    }
  }
};
```

## Error Handling Protocol

If a phase fails:

1. Log error to `state.json.metadata.errors[]`
2. Increment retry counter for phase
3. If retries < 3:
   - Wait 5 seconds
   - Re-invoke Task tool with same prompt + error context
4. If retries >= 3:
   - Set phase status to "error"
   - Escalate to user with error details
   - Suggest manual intervention or skip

## Validation Gates

### Between Phase 4 and 4.5 (SEO → Image Generation)
```javascript
const seoMetadata = JSON.parse(fs.readFileSync(`${workspace}/seo-metadata.json`));
const valid =
  seoMetadata.title.length >= 50 && seoMetadata.title.length <= 60 &&
  seoMetadata.metaDescription.length >= 150 && seoMetadata.metaDescription.length <= 160 &&
  seoMetadata.ogDescription.length >= 100 && seoMetadata.ogDescription.length <= 120;

if (!valid) {
  // Retry Phase 4 with explicit limit requirements
}
```

### Between Phase 4.5 and 5 (Image Generation → Style Review)
```javascript
// Image generation is optional - always proceed even if images failed
const imageManifest = JSON.parse(fs.readFileSync(`${workspace}/image-manifest.json`));
const hasImages = imageManifest.cover?.path || imageManifest.sections?.length > 0;

// Log image status but don't block
state.metadata.imagesGenerated = hasImages;
state.metadata.imageCount = imageManifest.stats?.totalImages || 0;

// Always proceed to Style Review - images are enhancement, not requirement
```

### Between Phase 6 and 7 (Publish → Social)
```javascript
const requiredFields = ['title', 'slug', 'content', 'excerpt', 'author', 'categories', 'seo'];
const publishResult = JSON.parse(fs.readFileSync(`${workspace}/sanity-ready-post.md`));
const valid = requiredFields.every(field => publishResult[field] !== undefined);

if (!valid) {
  // Retry Phase 6 with complete field requirements
}
```

## Integration with Parallel Research

For Phase 1 (Research), optionally use parallel execution:

```markdown
## Parallel Research Mode

When depth="standard" or "extensive", launch multiple researchers:

Parallel Task invocations (single message, multiple tool calls):
1. Task: claude-researcher focusing on current trends
2. Task: perplexity-researcher focusing on technical depth
3. Task: gemini-researcher focusing on alternative perspectives

Wait for all with timeout, then synthesize results into unified research-findings.json
```

See `blog-trend-researcher/workflows/ParallelResearch.md` for full parallel execution protocol.
