# Complete Workflow Guide

Understanding how the 8-agent blog writing system works from start to finish.

## 🔄 Workflow Overview

The blog writing system uses a **sequential pipeline** with 8 specialized agents:

```
User Request
     ↓
Orchestrator (Coordinates workflow)
     ↓
Phase 1: Research → Phase 2: Synthesis → Phase 3: Writing → Phase 4: SEO → Phase 5: Review → Phase 6: Publishing
```

Each phase:
- ✅ Takes output from the previous phase
- ✅ Validates input before processing
- ✅ Produces output for the next phase
- ✅ Updates workflow state
- ✅ Can retry on failure (3 attempts)

## 📊 Phase-by-Phase Breakdown

### Phase 0: Initialization
**Agent:** Orchestrator
**Duration:** ~30 seconds
**Purpose:** Set up the project and workflow state

#### What Happens:
1. Validates user input (topic, content type, publishing mode)
2. Generates unique project ID (format: `proj-YYYY-MM-DD-HHMMSS`)
3. Creates project directory structure
4. Initializes `state.json` with workflow metadata

#### Output:
- Project directory created in `blog-workspace/active-projects/PROJECT_ID/`
- `state.json` file with initial status

#### State Update:
```json
{
  "projectId": "proj-2025-01-15-143022",
  "status": "initialization",
  "phases": {
    "initialization": {"status": "complete"},
    "research": {"status": "pending"}
  }
}
```

---

### Phase 1: Research
**Agent:** `blog-trend-researcher`
**Duration:** ~5 minutes
**Purpose:** Gather comprehensive research on the topic

#### Input:
- Topic (e.g., "Building Scalable React Applications")
- Content type (tech or personal-dev)

#### What Happens:
1. **Multi-source research:**
   - Web search for current articles and trends
   - Documentation and official resources
   - Community discussions and forums
   - Industry reports and case studies

2. **Trend analysis:**
   - Identifies current developments
   - Finds emerging patterns
   - Discovers unique angles

3. **Source documentation:**
   - Collects 15+ credible sources
   - Assesses source credibility (High/Medium/Low)
   - Extracts key points and quotes

4. **Insight synthesis:**
   - Organizes findings by theme
   - Identifies supporting evidence
   - Flags unique perspectives

#### Output Files:
1. **`research-findings.json`**
   - Structured research data
   - Key insights and themes
   - Source list with credibility ratings
   - Content recommendations

2. **`research-notes.md`**
   - Human-readable research notes
   - Detailed findings
   - Source analysis

#### Validation:
- Minimum 5 sources (preferably 15+)
- Research depth appropriate for content type
- Sources properly documented
- Unique angles identified

#### Quality Targets:
- Comprehensive coverage: 15+ sources
- Recent information: Priority on last 12-24 months
- Multiple perspectives: Balanced viewpoints
- Actionable insights: Practical value for readers

---

### Phase 2: Synthesis
**Agent:** `blog-insight-synthesizer`
**Duration:** ~3 minutes
**Purpose:** Transform research into a structured content outline

#### Input:
- `research-findings.json` (from Phase 1)
- `research-notes.md`
- Content type (tech or personal-dev)

#### What Happens:
1. **Research analysis:**
   - Reviews all research findings
   - Identifies primary themes and insights
   - Assesses content depth and breadth

2. **Message prioritization:**
   - Extracts most important insights
   - Identifies unique value propositions
   - Determines reader take-aways

3. **Structure development:**
   - Designs logical section flow
   - Plans transitions between sections
   - Balances depth and readability

4. **Content mapping:**
   - Assigns research points to sections
   - Identifies evidence and examples needed
   - Plans engagement elements

#### Output:
**`content-outline.md`** - Comprehensive content structure

Includes:
- Executive summary of the post
- Core message architecture (primary + supporting messages)
- Detailed outline with:
  - Introduction (150-250 words)
  - 2-4 main sections (300-500 words each)
  - Conclusion (150-250 words)
- Word count distribution
- Research integration plan
- Engagement elements (questions, examples, takeaways)

#### Validation:
- Research thoroughly analyzed
- Clear primary message established
- Logical section progression
- Research well-integrated
- Content type appropriate approach

#### Quality Targets:
- Clear narrative flow from problem to solution
- Each section supports overall message
- Unique value proposition evident
- Reader journey is smooth and logical

---

### Phase 3: Writing
**Agent:** `tech-blogger-writer` OR `personal-dev-writer`
**Duration:** ~10 minutes
**Purpose:** Create the initial draft based on the outline

#### Input:
- `content-outline.md`
- `research-findings.json`
- Content type (tech or personal-dev)

#### Content Type Selection:

**For Technology Content:**
- **Agent:** `tech-blogger-writer`
- **Length:** 1000-1200 words
- **Tone:** Technical but accessible
- **Features:**
  - Code examples with explanations
  - Best practices and gotchas
  - Real-world applications
  - Troubleshooting guidance

**For Personal Development Content:**
- **Agent:** `personal-dev-writer`
- **Length:** 1200-1500 words
- **Tone:** Inspirational and practical
- **Features:**
  - Personal stories and anecdotes
  - Actionable advice
  - Reflection questions
  - Emotional connection

#### What Happens:
1. **Content creation:**
   - Follows the outline structure
   - Integrates research findings
   - Maintains brand voice (Professional & Friendly)

2. **Engagement elements:**
   - Hook in introduction
   - Questions for reflection
   - Practical examples
   - Actionable takeaways

3. **Technical quality:**
   - Grammar and spelling check
   - Sentence structure optimization
   - Transition improvements
   - Consistency verification

#### Output:
**`draft-tech.md` or `draft-personal-dev.md`** - Initial complete draft

Includes:
- Engaging introduction with hook
- Well-structured body sections
- Practical examples and illustrations
- Clear transitions
- Inspiring/conclusive ending
- Call-to-action

#### Validation:
- Follows outline structure
- Brand voice maintained
- Appropriate length for content type
- Engaging from start to finish
- Technical accuracy (for tech posts)

#### Quality Targets:
- Tech: 1000-1200 words, code examples, best practices
- Personal Dev: 1200-1500 words, stories, actionable advice
- Professional yet friendly tone
- Clear, engaging writing
- Logical flow and structure

---

### Phase 4: SEO Optimization
**Agent:** `seo-content-optimizer`
**Duration:** ~5 minutes
**Purpose:** Optimize content for search engines while maintaining readability

#### Input:
- `draft-tech.md` or `draft-personal-dev.md`
- `draft-metadata.json`
- SEO requirements (keywords, search intent)

#### What Happens:
1. **Keyword integration:**
   - Identifies primary and secondary keywords
   - Naturally integrates keywords (1-2% density)
   - Distributes keywords across headers and content

2. **On-page SEO:**
   - Optimizes title tag and meta description
   - Structures headers (H1, H2, H3) with keywords
   - Optimizes URL slug
   - Adds internal and external links

3. **Technical SEO:**
   - Image alt text optimization
   - Content structure for crawlability
   - Readability optimization
   - Schema markup suggestions

4. **SEO scoring:**
   - Evaluates keyword optimization (25 pts)
   - Assesses content structure (25 pts)
   - Reviews technical SEO (25 pts)
   - Measures user value (25 pts)

#### Output Files:
1. **`seo-optimized-draft.md`**
   - Content with keywords integrated
   - Optimized headers and structure
   - Meta tags and descriptions
   - SEO-friendly formatting

2. **`seo-metadata.json`**
   - SEO score (0-100)
   - Score breakdown by category
   - Keyword density analysis
   - Optimization recommendations
   - Technical SEO details

#### Validation:
- Keywords naturally integrated
- Keyword density within optimal range (1-2%)
- SEO structure in place
- Readability maintained

#### Quality Targets:
- **SEO Score:** ≥70/100
- Keyword in title and first 100 words
- Proper header hierarchy
- Meta description 150-160 characters
- Internal/external links present

---

### Phase 5: Style Review
**Agent:** `style-guardian`
**Duration:** ~5 minutes
**Purpose:** Ensure brand consistency and polish the final draft

#### Input:
- `seo-optimized-draft.md`
- `seo-metadata.json`
- `brand-style.json`
- Content type

#### What Happens:
1. **Brand voice enforcement:**
   - Verifies "Professional & Friendly" tone
   - Ensures consistency throughout
   - Adjusts language and tone

2. **Quality assurance:**
   - Grammar and spelling check
   - Sentence structure improvement
   - Paragraph flow optimization
   - Transition enhancement

3. **Engagement optimization:**
   - Strengthens hooks
   - Improves examples
   - Enhances takeaways
   - Polishes call-to-action

4. **Style scoring:**
   - Brand voice compliance (25 pts)
   - Clarity and readability (25 pts)
   - Content structure (20 pts)
   - Engagement elements (15 pts)
   - Quality and polish (15 pts)

#### Output Files:
1. **`polished-draft.md`**
   - Final, publication-ready content
   - Brand voice consistent
   - Grammar and style polished
   - Enhanced engagement elements

2. **`style-report.md`**
   - Style score (0-100)
   - Brand voice analysis
   - Quality metrics
   - Before/after examples
   - Recommendations

#### Validation:
- Brand voice consistent
- Grammar and spelling correct
- Clear, engaging flow
- Professional polish applied
- Quality benchmarks met

#### Quality Targets:
- **Style Score:** ≥80/100
- Professional yet friendly tone maintained
- Clear, readable writing
- Engaging from start to finish
- Actionable takeaways provided

---

### Phase 6: Publishing
**Agent:** `sanity-publisher`
**Duration:** ~2 minutes
**Purpose:** Format and publish content to Sanity CMS

#### Input:
- `polished-draft.md`
- `seo-metadata.json`
- `style-report.md`
- Publishing mode (markdown, api, or ask-user)

#### What Happens:

**For Markdown Mode:**
1. Converts content to Sanity-compatible format
2. Adds YAML frontmatter with all required fields
3. Generates `sanity-ready-post.md`
4. Provides import instructions

**For API Mode:**
1. Connects to Sanity CMS via API
2. Converts content to Sanity Portable Text format
3. Creates document with all metadata
4. Publishes document
5. Returns publishing confirmation

#### Output Files:

**Markdown Mode:**
- **`sanity-ready-post.md`**
  - Sanity-formatted content
  - YAML frontmatter with:
    - title, slug, excerpt
    - author, categories, tags
    - seo metadata
    - quality scores
  - Import instructions
  - Publishing checklist

**API Mode:**
- **`publishing-response.json`**
  - Publishing status
  - Document IDs
  - URLs
  - Validation results
  - Any errors or warnings

#### Validation:
- All required fields present
- Schema compliance verified
- Categories and tags valid
- Author reference exists

#### Quality Targets:
- Schema-compliant output
- All metadata present
- Error-free publishing (API mode)
- Clear instructions (markdown mode)

---

## 🔄 State Management

### State File Structure

The `state.json` file tracks everything:

```json
{
  "projectId": "proj-2025-01-15-143022",
  "topic": "Building Scalable React Applications",
  "contentType": "tech",
  "publishingMode": "markdown",
  "status": "publishing",
  "phases": {
    "initialization": {"status": "complete", "output": "state.json"},
    "research": {"status": "complete", "output": "research-findings.json"},
    "synthesis": {"status": "complete", "output": "content-outline.md"},
    "writing": {"status": "complete", "output": "draft-tech.md"},
    "seo": {"status": "complete", "output": "seo-optimized-draft.md"},
    "review": {"status": "complete", "output": "polished-draft.md"},
    "publishing": {"status": "in_progress", "output": "sanity-ready-post.md"}
  },
  "metadata": {
    "wordCount": 1150,
    "seoScore": 85,
    "styleScore": 92,
    "errors": []
  }
}
```

### Phase Status Values

- `pending` - Not started yet
- `in_progress` - Currently executing
- `complete` - Finished successfully
- `error` - Failed with errors

### Error Handling

Each phase:
1. Retries up to 3 times on failure
2. Waits 5 seconds between retries
3. Logs all errors to `state.json.metadata.errors`
4. Escalates after max retries

### Project Archiving

After successful completion:
- Project moves from `active-projects/` to `archive/`
- All artifacts preserved for reference
- State file updated with completion timestamp

---

## 📊 Quality Metrics

### SEO Score (Phase 4)
**Target: ≥70/100**
- Keyword Optimization (25 pts)
- Content Structure (25 pts)
- Technical SEO (25 pts)
- User Value (25 pts)

### Style Score (Phase 5)
**Target: ≥80/100**
- Brand Voice (25 pts)
- Clarity (25 pts)
- Structure (20 pts)
- Engagement (15 pts)
- Quality (15 pts)

### Overall Success
- Time: <30 minutes
- Both quality scores ≥ targets
- No critical errors
- Schema compliance verified

---

## 🎯 Understanding the Pipeline

### Why Sequential?

**Quality Control:** Each phase validates the previous output before proceeding.

**Debugging:** Easy to identify where issues occur.

**Flexibility:** Can skip or re-run individual phases if needed.

**Transparency:** Clear progress tracking at each stage.

### File-Based Communication

Each phase reads input files and writes output files:

```
Phase 1 writes → Phase 2 reads → Phase 2 writes → Phase 3 reads → ...
```

### Workflow Orchestration

The orchestrator:
1. Manages state between phases
2. Validates outputs before proceeding
3. Handles errors and retries
4. Coordinates all agents
5. Archives completed projects

---

## 🚀 Next Steps

Now you understand the workflow:

1. **[Run Your First Post](examples/first-post.md)** - See it in action
2. **[Configure Sanity](configuration.md)** - Enable API publishing
3. **[Agent Documentation](../agents/)** - Deep dive into each agent
4. **[Customization Guide](customization.md)** - Adapt to your needs

**Ready to create your first blog post?** Check out the [Quick Start Guide](quick-start.md)!
