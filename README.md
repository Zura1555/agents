# Blog Writing Subagents System

An 8-agent blog writing automation system built with Claude Agent SDK for creating high-quality, SEO-optimized blog posts with Sanity CMS publishing.

**Author**: Thuong-Tuan Tran
**Version**: 1.0.0

---

## 🎯 Overview

This system automates the entire blog writing workflow from research to published post. It features 8 specialized subagents working in a sequential pipeline to produce professional, engaging, and SEO-optimized blog content for technology and personal development topics.

### Key Features

- ✅ **8 Specialized Agents** - Each focused on a specific aspect of blog creation
- ✅ **Dual Publishing Modes** - Manual markdown output OR direct API publishing
- ✅ **SEO Optimization** - Built-in keyword integration and optimization
- ✅ **Brand Voice Consistency** - "Professional & Friendly" tone maintained throughout
- ✅ **Sanity CMS Integration** - Native support for Sanity headless CMS
- ✅ **State Management** - File-based tracking with comprehensive artifact preservation
- ✅ **Quality Assurance** - Multiple validation and quality scoring phases

---

## 🏗️ System Architecture

### Workflow Pipeline

```
User Request → Orchestrator → Research → Synthesis → Writing → SEO → Review → Publish
```

### 8 Specialized Agents

1. **blog-master-orchestrator** - Central workflow coordinator
2. **blog-trend-researcher** - Topic research and trend analysis
3. **blog-insight-synthesizer** - Research synthesis and outline creation
4. **tech-blogger-writer** - Technology content writing (800-1200 words)
5. **personal-dev-writer** - Personal development writing (1000-1500 words)
6. **seo-content-optimizer** - SEO optimization and keyword integration
7. **style-guardian** - Brand voice and quality assurance
8. **sanity-publisher** - Sanity CMS publishing (dual-mode support)

---

## 📁 Project Structure

```
/d/project/tuan/
├── .claude/skills/                    # 8 Agent Skills
│   ├── blog-master-orchestrator/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── orchestrate_workflow.py
│   │       └── state_manager.py
│   ├── blog-trend-researcher/
│   │   └── SKILL.md
│   ├── blog-insight-synthesizer/
│   │   └── SKILL.md
│   ├── tech-blogger-writer/
│   │   └── SKILL.md
│   ├── personal-dev-writer/
│   │   └── SKILL.md
│   ├── seo-content-optimizer/
│   │   └── SKILL.md
│   ├── style-guardian/
│   │   └── SKILL.md
│   └── sanity-publisher/
│       └── SKILL.md
│
├── blog-workspace/                     # Active Projects & Archives
│   ├── active-projects/               # In-progress blog posts
│   └── archive/                       # Completed blog posts
│
├── config/                             # Configuration Files
│   ├── brand-style.json              # Brand voice & style guidelines
│   └── sanity-config.json.example    # Sanity API configuration template
│
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1. Configure Sanity (Optional - for API Publishing)

If you want automated publishing:

```bash
# Copy example config
cp config/sanity-config.json.example config/sanity-config.json

# Edit with your Sanity credentials
# Get these from https://manage.sanity.io/
```

**Required Credentials:**
- `project.id` - Your Sanity project ID
- `dataset` - Usually "production"
- `api.token` - API token with write permissions

**Security Note**: Never commit `sanity-config.json` to version control!

### 2. Run the Orchestrator

```bash
# Basic usage
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Your Blog Topic" \
  --type tech \
  --mode ask-user

# Examples
python orchestrate_workflow.py \
  --topic "Building Scalable React Applications" \
  --type tech \
  --mode markdown

python orchestrate_workflow.py \
  --topic "5 Lessons from My First Year as a Developer" \
  --type personal-dev \
  --mode api
```

### 3. Choose Publishing Mode

When `--mode ask-user`, the system will prompt:
1. **Markdown Output** - Generates formatted file for manual copy-paste
2. **Direct API Publishing** - Automatically publishes to Sanity (requires credentials)

---

## 📖 Detailed Usage

### Running Individual Agents

Each agent can be run independently:

```bash
# Research phase only
python -m blog_master_orchestrator.scripts.research --topic "Your Topic"

# Writing phase only
python -m blog_master_orchestrator.scripts.write \
  --content-type tech \
  --outline path/to/outline.md

# View state
python .claude/skills/blog-master-orchestrator/scripts/state_manager.py proj-2025-01-15-001
```

### Checking Project Status

```bash
# View project state
cat blog-workspace/active-projects/PROJECT_ID/state.json

# List active projects
ls blog-workspace/active-projects/

# List archived projects
ls blog-workspace/archive/
```

### Understanding Workflow Artifacts

Each project generates these files:

```
blog-workspace/active-projects/PROJECT_ID/
├── state.json                    # Workflow state & metadata
├── research-findings.json        # Research data & sources
├── research-notes.md             # Detailed research notes
├── content-outline.md            # Structured content outline
├── draft-tech.md or draft-personal-dev.md  # Initial draft
├── seo-metadata.json            # SEO optimization data
├── seo-optimized-draft.md       # SEO-optimized content
├── style-report.md              # Quality & style analysis
├── polished-draft.md            # Final polished content
└── sanity-ready-post.md         # Sanity-formatted output
```

---

## ⚙️ Configuration

### Brand Style (`config/brand-style.json`)

Defines your brand voice, writing standards, and quality benchmarks.

**Key Settings:**
- **Author**: Thuong-Tuan Tran
- **Voice**: Professional & Friendly
- **Content Types**: tech, personal-dev
- **Quality Scores**: SEO ≥70, Style ≥80

### Sanity Config (`config/sanity-config.json`)

Configure Sanity CMS integration.

**For Manual Publishing:**
```json
{
  "publishing": {
    "defaultMode": "markdown"
  }
}
```

**For API Publishing:**
```json
{
  "project": {
    "id": "your-project-id",
    "dataset": "production"
  },
  "api": {
    "token": "your-token-here"
  },
  "publishing": {
    "defaultMode": "api"
  }
}
```

---

## 📊 Workflow Phases

### Phase 1: Research (`blog-trend-researcher`)
- **Input**: Topic, content type
- **Output**: `research-findings.json`, `research-notes.md`
- **Duration**: ~5 minutes
- **Quality**: 15+ credible sources

### Phase 2: Synthesis (`blog-insight-synthesizer`)
- **Input**: Research findings
- **Output**: `content-outline.md`
- **Duration**: ~3 minutes
- **Quality**: Logical structure, clear messaging

### Phase 3: Writing
- **Input**: Content outline
- **Output**: `draft-tech.md` or `draft-personal-dev.md`
- **Agent**: tech-blogger-writer OR personal-dev-writer
- **Duration**: ~10 minutes
- **Quality**: 1000-1500 words, engaging content

### Phase 4: SEO Optimization (`seo-content-optimizer`)
- **Input**: Draft content
- **Output**: `seo-optimized-draft.md`, `seo-metadata.json`
- **Duration**: ~5 minutes
- **Quality**: Score ≥70/100

### Phase 5: Style Review (`style-guardian`)
- **Input**: SEO-optimized content
- **Output**: `polished-draft.md`, `style-report.md`
- **Duration**: ~5 minutes
- **Quality**: Score ≥80/100

### Phase 6: Publishing (`sanity-publisher`)
- **Input**: Polished content
- **Output**: Published post OR `sanity-ready-post.md`
- **Duration**: ~2 minutes
- **Quality**: Schema-compliant, error-free

---

## 🎨 Content Types

### Technology Content
- **Length**: 1000-1200 words (5-6 min read)
- **Tone**: Technical but accessible
- **Features**: Code examples, best practices, troubleshooting
- **Structure**: Problem → Solution → Implementation → Gotchas

### Personal Development Content
- **Length**: 1200-1500 words (6-8 min read)
- **Tone**: Inspirational and practical
- **Features**: Personal stories, actionable advice, reflection questions
- **Structure**: Story → Insight → Application → Encouragement

---

## 📈 Quality Metrics

### SEO Score (seo-content-optimizer)
**Target: ≥70/100**
- Keyword optimization (25 pts)
- Content structure (25 pts)
- Technical SEO (25 pts)
- User value (25 pts)

### Style Score (style-guardian)
**Target: ≥80/100**
- Brand voice (25 pts)
- Clarity (25 pts)
- Structure (20 pts)
- Engagement (15 pts)
- Quality (15 pts)

### Overall Success Criteria
- Time to publish: <30 minutes
- Quality scores: Both ≥ target
- No critical errors
- Schema compliance verified

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "State file not found"
**Solution**: Project directory may have been moved or deleted. Check archive folder.

#### 2. "Author reference not found" (Sanity)
**Solution**:
1. Open Sanity Studio
2. Go to "Authors" collection
3. Create author with name "Thuong-Tuan Tran"
4. Note the _id
5. Update author reference

#### 3. "Category doesn't exist" (Sanity)
**Solution**:
1. Create category in Sanity Studio
2. Use exact name: "Technology" or "Personal Development"
3. Or update config to use existing categories

#### 4. "Invalid API token" (Sanity)
**Solution**:
1. Check token hasn't expired
2. Verify token has write permissions
3. Regenerate token in Sanity manage panel

#### 5. Phase failed with error
**Solution**:
- Check error logs in `state.json.metadata.errors`
- Review input files for corruption
- Verify all dependencies present
- Retry phase manually

### Getting Help

1. Check state file for detailed error information
2. Review agent SKILL.md files for specifications
3. Validate configuration files (JSON syntax)
4. Ensure all dependencies are installed
5. Check file permissions for workspace directory

---

## 🛠️ Development

### Extending the System

#### Adding a New Content Type

1. Create new writer agent in `.claude/skills/`
2. Update `orchestrate_workflow.py` to include new agent
3. Add content type to `brand-style.json`
4. Update category mappings in `sanity-publisher`

#### Customizing Brand Voice

Edit `config/brand-style.json`:
- Modify `tone` characteristics
- Adjust `language` preferences
- Update `contentGuidelines`

#### Adding New Agents

1. Create agent directory in `.claude/skills/`
2. Create `SKILL.md` with agent specification
3. Add agent to workflow pipeline
4. Update dependencies and inputs

### Agent SKILL.md Format

Each agent must include:

```yaml
---
name: agent-name
description: Brief description
version: 1.0.0
author: Thuong-Tuan Tran
tags: [tag1, tag2]
---

# Agent Name

## Core Responsibilities
- Responsibility 1
- Responsibility 2

## Input Requirements
- Expected inputs
- Validation rules

## Output Specifications
- Output format
- File structure
- Quality standards
```

---

## 📝 Workflow State Tracking

The system uses `state.json` to track progress:

```json
{
  "projectId": "proj-2025-01-15-001",
  "topic": "Your Topic",
  "status": "writing",
  "phases": {
    "research": {"status": "complete", "output": "research-findings.json"},
    "writing": {"status": "in_progress", "output": "draft-tech.md"}
  },
  "metadata": {
    "seoScore": 0,
    "styleScore": 0,
    "errors": []
  }
}
```

**Phase States:**
- `pending` - Not started
- `in_progress` - Currently executing
- `complete` - Finished successfully
- `error` - Failed with errors

---

## 🔐 Security Notes

### API Credentials
- Store Sanity token in `sanity-config.json` (gitignored)
- Use environment variables for production
- Never commit credentials to version control
- Rotate tokens regularly

### Workspace Security
- Project directories contain drafts and unpublished content
- Restrict file permissions appropriately
- Archive completed projects to separate directory
- Consider encryption for sensitive topics

---

## 📚 References

### Technologies Used
- **Claude Agent SDK** - Multi-agent orchestration
- **Sanity CMS** - Headless CMS backend
- **Python 3.8+** - Agent scripting
- **JSON** - State management and metadata
- **Markdown** - Content formatting

### Documentation
- Agent SKILL.md files - Detailed agent specifications
- `config/brand-style.json` - Brand guidelines
- `config/sanity-config.json.example` - Integration guide

### Support
- Check agent SKILL.md files for detailed specifications
- Review state.json for error tracking
- Validate configuration files for errors

---

## 🎯 Success Metrics

Expected performance when system is properly configured:

- ⚡ **Speed**: <30 minutes from topic to published post
- 📊 **Quality**: SEO ≥70, Style ≥80, Zero critical errors
- 🎯 **Consistency**: 95%+ posts meet quality standards
- 📈 **Volume**: 3-5 high-quality posts per week
- 🔄 **Automation**: 90%+ of workflow automated

---

## 📄 License

Created by Thuong-Tuan Tran for personal blog automation.

---

## 🚀 Next Steps

1. **Configure Sanity** credentials (optional)
2. **Test with one blog post** using markdown mode
3. **Review quality** of output and adjust brand style if needed
4. **Enable API mode** for automated publishing
5. **Scale up** to regular posting schedule

**Questions?** Review the SKILL.md files for detailed agent specifications or check the troubleshooting section above.

---

**Built with ❤️ by Thuong-Tuan Tran**
