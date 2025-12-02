# Quick Start Guide

Get your blog writing system up and running in 5 minutes!

## 🎯 What You'll Accomplish

By the end of this guide, you'll:
- ✅ Have the system installed and configured
- ✅ Run your first blog post workflow
- ✅ Understand the basic workflow
- ✅ Know where to find help

## 📋 Prerequisites

- Python 3.8+ installed
- Access to `/d/project/tuan/` directory
- (Optional) Sanity CMS account for API publishing

## 🚀 Step 1: Verify Installation

```bash
# Navigate to project directory
cd /d/project/tuan

# Check if files exist
ls -la

# You should see:
# - .claude/skills/ (agent skills)
# - blog-workspace/ (workspace directories)
# - config/ (configuration files)
# - README.md
# - docs/ (this documentation)
```

## 📝 Step 2: Configure Brand Settings (Optional)

The system works with default settings, but you can customize:

```bash
# View current brand settings
cat config/brand-style.json

# Edit if needed (optional)
# nano config/brand-style.json
```

**Default settings:**
- Author: Thuong-Tuan Tran
- Brand Voice: Professional & Friendly
- Content Types: tech, personal-dev
- Target Quality: SEO ≥70, Style ≥80

## 🎨 Step 3: Choose Your Publishing Mode

You have three options:

### Option A: Markdown Output (Recommended for Testing)
Generates a formatted markdown file you copy-paste into Sanity.

**Pros:**
- No API setup required
- Manual review before publishing
- Perfect for testing

**Cons:**
- Manual copy-paste step

### Option B: Direct API Publishing (Fully Automated)
Publishes directly to Sanity CMS via API.

**Pros:**
- Fully automated
- No manual steps
- Instant publishing

**Cons:**
- Requires Sanity API credentials
- More setup required

### Option C: Ask at Runtime
System asks you which mode to use each time.

**Best for:** Testing both modes

## 💻 Step 4: Run Your First Blog Post

### For Markdown Mode (Testing):

```bash
# Run the orchestrator
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Getting Started with React Hooks" \
  --type tech \
  --mode markdown
```

### For API Mode (Full Automation):

```bash
# First, configure Sanity (see Configuration Guide)
# Then run:
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Building Better Morning Routines" \
  --type personal-dev \
  --mode api
```

### For Ask Mode (Both Options):

```bash
# Run with ask mode
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Your Blog Topic Here" \
  --type tech \
  --mode ask-user
```

## ⏱️ Step 5: Wait for Completion

The workflow takes 20-30 minutes and runs through 6 phases:

```
✓ Phase 1: Research (5 min)
✓ Phase 2: Synthesis (3 min)
✓ Phase 3: Writing (10 min)
✓ Phase 4: SEO Optimization (5 min)
✓ Phase 5: Style Review (5 min)
✓ Phase 6: Publishing (2 min)
```

You'll see progress updates in your terminal.

## 📂 Step 6: Review Output

After completion, find your blog post:

### For Markdown Mode:
```bash
# Find your project
ls blog-workspace/archive/

# View the output
cat blog-workspace/archive/PROJECT_ID/sanity-ready-post.md
```

### For API Mode:
```bash
# Check the publishing response
cat blog-workspace/archive/PROJECT_ID/publishing-response.json

# Visit your Sanity CMS to see the published post
```

## 📊 Step 7: Check Quality Scores

Open the state file to see quality metrics:

```bash
cat blog-workspace/archive/PROJECT_ID/state.json | grep -A 10 metadata
```

You'll see:
- `seoScore` (target: ≥70)
- `styleScore` (target: ≥80)
- `wordCount` (target: 1000-1500)
- Any `errors`

## 🎉 Success!

Your first blog post is ready! Here's what was created:

### Artifacts Generated:
- `research-findings.json` - Research data with sources
- `content-outline.md` - Structured outline
- `draft-tech.md` - Initial draft
- `seo-optimized-draft.md` - SEO-optimized version
- `polished-draft.md` - Final polished version
- `sanity-ready-post.md` - Sanity-formatted output (markdown mode)

### Quality Reports:
- `seo-metadata.json` - SEO metrics and recommendations
- `style-report.md` - Style and brand voice analysis

## 🔄 What Happens Next

### For Markdown Mode:
1. Copy content from `sanity-ready-post.md`
2. Paste into Sanity CMS
3. Review and publish
4. Share your post!

### For API Mode:
1. Post is already published in Sanity
2. Review in Sanity Studio
3. Share your post!

## 🧪 Try Another Post

Run another blog post with different settings:

```bash
# Personal development topic
python orchestrate_workflow.py \
  --topic "5 Productivity Mistakes I Made So You Don't Have To" \
  --type personal-dev \
  --mode markdown

# Different tech topic
python orchestrate_workflow.py \
  --topic "TypeScript vs JavaScript: When to Use Which" \
  --type tech \
  --mode ask-user
```

## 📚 Next Steps

Now that you've created your first post:

1. **Read the Workflow Guide** - Understand how the 8 agents work together
2. **Configure Sanity API** - Enable automated publishing
3. **Review Agent Documentation** - Learn what each agent does
4. **Customize Brand Settings** - Adjust voice and style
5. **Check Troubleshooting Guide** - Be prepared for issues

## ❓ Common Questions

**Q: How long does it take?**
A: 20-30 minutes for a complete blog post.

**Q: Can I stop and restart?**
A: Yes! The system saves state after each phase.

**Q: What if a phase fails?**
A: Check the error in `state.json` and see the Troubleshooting Guide.

**Q: Can I run multiple posts at once?**
A: Yes! Each post gets a unique project ID.

**Q: Where are my posts stored?**
A: In `blog-workspace/archive/PROJECT_ID/`

## 🎯 Tips for Success

1. **Start with markdown mode** for testing
2. **Check quality scores** before publishing
3. **Review the output** before sharing
4. **Keep your topics focused** and specific
5. **Use the state file** to track progress

## 🚀 Ready to Go Deeper?

Continue exploring:
- [Complete Workflow Guide](workflow.md) - Understand the full process
- [Agent Documentation](../agents/) - Learn what each agent does
- [Configuration Guide](configuration.md) - Customize for your needs
- [Troubleshooting Guide](troubleshooting.md) - Solve common issues

**Happy Blogging!** ✍️
