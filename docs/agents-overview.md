# Agents Overview

Quick reference guide to all 8 agents in the blog writing system.

## 📊 Agent Summary

| # | Agent | Purpose | Duration | Output |
|---|-------|---------|----------|--------|
| 0 | blog-master-orchestrator | Coordinates workflow | 30s | state.json |
| 1 | blog-trend-researcher | Research & trends | 5 min | research-findings.json |
| 2 | blog-insight-synthesizer | Outline creation | 3 min | content-outline.md |
| 3 | tech/personal-dev writer | Content writing | 10 min | draft-[type].md |
| 4 | seo-content-optimizer | SEO optimization | 5 min | seo-optimized-draft.md |
| 5 | style-guardian | Brand & quality | 5 min | polished-draft.md |
| 6 | sanity-publisher | CMS publishing | 2 min | Published/Markdown |

## 🤖 Detailed Agent Guide

### 1. blog-master-orchestrator

**Role:** Central workflow coordinator
**Phase:** 0 - Initialization
**Responsibilities:**
- Coordinates all 8 agents
- Manages workflow state
- Handles errors and retries
- Archives completed projects

**Key Files:**
- `orchestrate_workflow.py` - Main execution script
- `state_manager.py` - State management utility

**Links:**
- [Detailed Documentation](agents/orchestrator.md)
- [Workflow Guide](guides/workflow.md)

---

### 2. blog-trend-researcher

**Role:** Topic research and analysis
**Phase:** 1 - Research
**Responsibilities:**
- Multi-source research (15+ sources)
- Trend identification
- Source documentation
- Insight synthesis

**Output:**
- `research-findings.json` - Structured research data
- `research-notes.md` - Human-readable notes

**Key Features:**
- Web search, documentation, forums, reports
- Credibility assessment (High/Medium/Low)
- Unique angle identification
- Content type specific (tech/personal-dev)

**Links:**
- [Detailed Documentation](agents/researcher.md)

---

### 3. blog-insight-synthesizer

**Role:** Research synthesis and outline creation
**Phase:** 2 - Synthesis
**Responsibilities:**
- Analyzes research findings
- Creates structured content outline
- Plans logical flow
- Maps research to sections

**Output:**
- `content-outline.md` - Comprehensive outline

**Key Features:**
- Message prioritization
- Structure development
- Word count distribution
- Engagement element planning

---

### 4. tech-blogger-writer

**Role:** Technology content writing
**Phase:** 3 - Writing (tech content)
**Responsibilities:**
- Creates engaging tech content
- Includes code examples
- Explains complex concepts clearly
- Provides practical guidance

**Output:**
- `draft-tech.md` - Technology post draft

**Specifications:**
- **Length:** 1000-1200 words
- **Tone:** Technical but accessible
- **Features:** Code examples, best practices, troubleshooting
- **Structure:** Problem → Solution → Implementation → Gotchas

**Links:**
- [Detailed Documentation](agents/tech-writer.md)

---

### 5. personal-dev-writer

**Role:** Personal development writing
**Phase:** 3 - Writing (personal-dev content)
**Responsibilities:**
- Creates inspirational content
- Shares personal stories
- Provides actionable advice
- Motivates readers

**Output:**
- `draft-personal-dev.md` - Personal development draft

**Specifications:**
- **Length:** 1200-1500 words
- **Tone:** Inspirational and practical
- **Features:** Stories, actionable advice, reflection questions
- **Structure:** Story → Insight → Application → Encouragement

**Links:**
- [Detailed Documentation](agents/personal-dev-writer.md)

---

### 6. seo-content-optimizer

**Role:** SEO optimization and scoring
**Phase:** 4 - SEO Optimization
**Responsibilities:**
- Integrates keywords naturally
- Optimizes on-page SEO
- Scores SEO quality
- Provides recommendations

**Output:**
- `seo-optimized-draft.md` - SEO-optimized content
- `seo-metadata.json` - SEO metrics

**Key Features:**
- Keyword density optimization
- Title and meta description
- Header structure (H1/H2/H3)
- Internal/external links
- **Score Target:** ≥70/100

**Links:**
- [Detailed Documentation](agents/seo-optimizer.md)

---

### 7. style-guardian

**Role:** Brand consistency and quality assurance
**Phase:** 5 - Style Review
**Responsibilities:**
- Enforces brand voice
- Polishes writing quality
- Improves readability
- Scores style consistency

**Output:**
- `polished-draft.md` - Final polished content
- `style-report.md` - Style analysis report

**Key Features:**
- Brand voice enforcement
- Grammar and spelling
- Clarity improvements
- Engagement optimization
- **Score Target:** ≥80/100

**Links:**
- [Detailed Documentation](agents/style-guardian.md)

---

### 8. sanity-publisher

**Role:** Sanity CMS publishing
**Phase:** 6 - Publishing
**Responsibilities:**
- Formats for Sanity schema
- Handles dual publishing modes
- Publishes to CMS or outputs markdown
- Provides confirmation

**Output (Markdown Mode):**
- `sanity-ready-post.md` - Sanity-formatted markdown

**Output (API Mode):**
- `publishing-response.json` - API response

**Publishing Modes:**
- **Markdown:** Output for manual copy-paste
- **API:** Direct publish to Sanity
- **Ask-User:** Prompt for mode choice

**Links:**
- [Detailed Documentation](agents/publisher.md)

---

## 🔄 Workflow Pipeline

```
User Request
     ↓
Orchestrator (Phase 0)
     ↓
Researcher (Phase 1) → research-findings.json
     ↓
Synthesizer (Phase 2) → content-outline.md
     ↓
Writer (Phase 3) → draft-[type].md
     ↓
SEO Optimizer (Phase 4) → seo-optimized-draft.md
     ↓
Style Guardian (Phase 5) → polished-draft.md
     ↓
Sanity Publisher (Phase 6) → Published/Markdown
```

## 📁 File Dependencies

Each agent reads output from the previous phase:

| Phase | Reads | Writes |
|-------|-------|--------|
| 0 (Orchestrator) | User input | state.json |
| 1 (Researcher) | topic, contentType | research-findings.json |
| 2 (Synthesizer) | research files | content-outline.md |
| 3 (Writer) | outline, research | draft-[type].md |
| 4 (SEO) | draft, metadata | seo-optimized-draft.md |
| 5 (Style) | seo-draft, seo-metadata | polished-draft.md |
| 6 (Publisher) | polished-draft, reports | Final output |

## 🎯 Quality Targets

| Agent | Target Metric |
|-------|---------------|
| Researcher | 15+ credible sources |
| Synthesizer | Clear outline structure |
| Tech Writer | 1000-1200 words |
| Personal Dev Writer | 1200-1500 words |
| SEO Optimizer | Score ≥70/100 |
| Style Guardian | Score ≥80/100 |
| Publisher | 100% schema compliance |

## 🔧 Customization Points

### Adding New Content Type

1. Create new writer agent (copy existing)
2. Update orchestrator phase mapping
3. Add to brand-style.json
4. Update category mappings

### Modifying Brand Voice

- Edit `config/brand-style.json`
- Update style-guardian criteria
- Adjust writing guidelines

### Customizing SEO

- Modify seo-content-optimizer scoring
- Adjust keyword strategy
- Update recommendations

### Changing Publishing Format

- Modify sanity-publisher schema mapping
- Update output format
- Adjust validation rules

## 📊 Performance Optimization

### Speed Improvements

**Current Times:**
- Research: 5 min (parallel possible)
- Writing: 10 min (largest bottleneck)
- SEO: 5 min
- Style: 5 min
- **Total:** 20-30 min

**Optimization Strategies:**
- Parallel research sources
- Caching common research
- Template-based writing
- Batch SEO optimization
- Incremental style updates

### Quality Improvements

**Ways to Improve:**
- Increase research depth
- Add more code examples
- Enhance SEO analysis
- Refine style criteria
- Better publishing validation

## 🐛 Error Handling

### Retry Logic

Each agent (except orchestrator):
- **Max Retries:** 3 attempts
- **Retry Delay:** 5 seconds
- **Escalation:** Mark as error after 3 failures

### Common Errors

**Research Phase:**
- Network errors
- No sources found
- Invalid topic

**Writing Phase:**
- Invalid outline
- Missing research
- Content type mismatch

**SEO Phase:**
- Missing keywords
- Invalid metadata
- Content too short

**Style Phase:**
- Invalid SEO draft
- Missing style guide
- Brand voice issues

**Publisher:**
- Invalid Sanity config
- Missing author reference
- Schema validation errors

## 📚 Documentation Links

### Getting Started
- [Quick Start Guide](guides/quick-start.md)
- [Workflow Guide](guides/workflow.md)
- [Running First Post](examples/first-post.md)

### Configuration
- [Configuration Guide](guides/configuration.md)
- [Brand Style](../config/brand-style.json)
- [Sanity Config](../config/sanity-config.json.example)

### Troubleshooting
- [Troubleshooting Guide](guides/troubleshooting.md)
- [Common Errors](guides/troubleshooting.md#common-errors)
- [Getting Help](guides/troubleshooting.md#getting-help)

### Advanced
- [Customization Guide](guides/customization.md)
- [API Integration](guides/api-integration.md)
- [State Management](guides/state-management.md)

## 🎯 Quick Reference

### Run a Blog Post

```bash
python orchestrate_workflow.py \
  --topic "Your Topic" \
  --type tech|personal-dev \
  --mode markdown|api|ask-user
```

### Check Status

```bash
cat blog-workspace/active-projects/PROJECT_ID/state.json
```

### View State

```bash
python .claude/skills/blog-master-orchestrator/scripts/state_manager.py PROJECT_ID
```

### Check Logs

```bash
cat blog-workspace/archive/PROJECT_ID/state.json | grep errors
```

---

**All agents documented in detail at:** `/d/project/tuan/docs/agents/`

**Ready to create your first post?** Start with the [Quick Start Guide](guides/quick-start.md)!
