# Running Your First Blog Post

A step-by-step walkthrough of creating your first blog post with the 8-agent system.

## 🎯 What You'll Learn

By following this guide, you'll:
- ✅ Run your first complete blog post workflow
- ✅ Understand what happens in each phase
- ✅ Review the quality of output
- ✅ Know where to find the final blog post
- ✅ Be ready to create more posts

## 📋 Prerequisites

- System installed and configured
- Basic understanding of workflow (see [Workflow Guide](../guides/workflow.md))
- Test topic in mind

## 🎨 Step 1: Choose Your Test Topic

For your first post, pick something:

**Simple and Specific:**
- "Getting Started with React Hooks"
- "Building Your First Web App"
- "5 Morning Habits That Changed My Life"
- "Understanding JavaScript Closures"

**Avoid:**
- Too broad: "JavaScript Guide"
- Too obscure: "Obscure Framework X"
- Too technical: Deep dive into compiler design

## 💻 Step 2: Run the Workflow

Open terminal and run:

```bash
# Navigate to project
cd /d/project/tuan

# Start your first post (let's use markdown mode for testing)
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Getting Started with React Hooks" \
  --type tech \
  --mode markdown
```

### What You'll See

**Initialization (30 seconds):**
```
================================================================
BLOG MASTER ORCHESTRATOR - WORKFLOW START
================================================================

Project ID: proj-2025-01-15-143022
Workspace: /d/project/tuan/blog-workspace/active-projects/proj-2025-01-15-143022
Content Type: tech
Publishing Mode: markdown

✓ Initialized project proj-2025-01-15-143022
```

**Research Phase (5 minutes):**
```
============================================================
Phase: research (Attempt 1/3)
Agent: blog-trend-researcher
============================================================
Executing blog-trend-researcher...
✓ Output file already exists, skipping phase
```

**Writing Phase (10 minutes):**
```
============================================================
Phase: writing (Attempt 1/3)
Agent: tech-blogger-writer
============================================================
Executing tech-blogger-writer...
```

## ⏱️ Step 3: Monitor Progress

The workflow takes 20-30 minutes. You can monitor progress:

### Check State File

In another terminal:

```bash
# Check current status
cat blog-workspace/active-projects/PROJECT_ID/state.json | grep -A 5 status

# Watch progress (Linux/Mac)
watch -n 2 'cat blog-workspace/active-projects/proj-2025-01-15-143022/state.json | grep status'

# Check which phase is running
cat state.json | python -m json.tool | grep -A 15 phases
```

### View Project Files

In another terminal:

```bash
# List all files created so far
ls -lh blog-workspace/active-projects/PROJECT_ID/

# Check a specific file
head -30 blog-workspace/active-projects/PROJECT_ID/draft-tech.md
```

## ✅ Step 4: Review Phase Outputs

As each phase completes, you can review the output:

### After Research Phase

```bash
# View research summary
cat blog-workspace/active-projects/PROJECT_ID/research-findings.json | \
  python -m json.tool | grep -A 5 summary

# View research notes
head -50 blog-workspace/active-projects/PROJECT_ID/research-notes.md
```

### After Synthesis Phase

```bash
# View content outline
cat blog-workspace/active-projects/PROJECT_ID/content-outline.md
```

### After Writing Phase

```bash
# View initial draft
head -50 blog-workspace/active-projects/PROJECT_ID/draft-tech.md

# Check word count
wc -w blog-workspace/active-projects/PROJECT_ID/draft-tech.md
```

### After SEO Phase

```bash
# Check SEO score
cat blog-workspace/active-projects/PROJECT_ID/seo-metadata.json | \
  python -m json.tool | grep -A 3 score

# View optimization recommendations
cat blog-workspace/active-projects/PROJECT_ID/seo-metadata.json | \
  python -m json.tool | grep -A 10 recommendations
```

### After Style Review

```bash
# Check style score
cat blog-workspace/active-projects/PROJECT_ID/style-report.md | grep "Total Style Score"

# View style recommendations
tail -50 blog-workspace/active-projects/PROJECT_ID/style-report.md
```

## 🎉 Step 5: Completion!

When the workflow completes, you'll see:

```
================================================================
WORKFLOW COMPLETED SUCCESSFULLY!
================================================================

Project archived to: /d/project/tuan/blog-workspace/archive/proj-2025-01-15-143022

Final deliverables:
  - research: research-findings.json
  - synthesis: content-outline.md
  - writing: draft-tech.md
  - seo: seo-optimized-draft.md
  - review: polished-draft.md
  - publishing: sanity-ready-post.md
```

## 📂 Step 6: Review Final Output

### Find Your Post

```bash
# Navigate to archived project
cd blog-workspace/archive/PROJECT_ID

# List all files
ls -lh
```

### View Final Sanity-Ready Post

```bash
# Display the final blog post
cat sanity-ready-post.md
```

You should see:
```markdown
---
title: "Getting Started with React Hooks: A Complete Guide"
slug: "getting-started-react-hooks-guide"
excerpt: "Learn React Hooks from scratch with practical examples..."
author: "Thuong-Tuan Tran"
publishedAt: "2025-01-15T14:30:22.000Z"
status: "published"
categories:
  - "Technology"
tags:
  - "react"
  - "hooks"
  - "javascript"
seo:
  metaTitle: "React Hooks Guide: Complete Beginner's Tutorial"
  metaDescription: "Master React Hooks with this step-by-step guide..."
  score: 85/100
readingTime: "6 minutes"
wordCount: 1180
---

# Getting Started with React Hooks: A Complete Guide

> Learn how to use React Hooks to build better components...

{Content continues...}
```

## 📊 Step 7: Check Quality Scores

### Review SEO Metrics

```bash
# View SEO score and breakdown
cat blog-workspace/archive/PROJECT_ID/seo-metadata.json | \
  python -m json.tool | grep -A 20 seo

# Typical output:
{
  "seo": {
    "score": 85,
    "scoreBreakdown": {
      "keywordOptimization": 88,
      "contentStructure": 85,
      "readability": 82,
      "technicalSeo": 90,
      "userValue": 85
    }
  }
}
```

### Review Style Metrics

```bash
# View style score
cat blog-workspace/archive/PROJECT_ID/style-report.md | grep -A 5 "Final Style Score"

# Output:
## Final Style Score Breakdown

- **Clarity**: 22/25 points
- **Brand Voice**: 24/25 points
- **Structure**: 18/20 points
- **Engagement**: 14/15 points
- **Quality**: 14/15 points

**Total Style Score**: 92/100
```

## 📋 Step 8: Review State File

```bash
# View complete state with metadata
cat blog-workspace/archive/PROJECT_ID/state.json | \
  python -m json.tool | grep -A 30 metadata

# Look for:
# - wordCount (target: 1000-1500)
# - seoScore (target: ≥70)
# - styleScore (target: ≥80)
# - errors (should be empty)
```

## 🔍 Step 9: Validate Output

### Content Quality

**Check the draft:**
- Does it follow the outline structure?
- Is the writing clear and engaging?
- Are there code examples (for tech posts)?
- Does it match brand voice?

**Example checks:**
```bash
# Count paragraphs
grep -c "^##" blog-workspace/archive/PROJECT_ID/polished-draft.md

# Check for code blocks (tech posts)
grep -c "```" blog-workspace/archive/PROJECT_ID/polished-draft.md

# Verify brand voice
grep -i "we\|you\|let's" blog-workspace/archive/PROJECT_ID/polished-draft.md | head -5
```

### SEO Quality

**Check keyword integration:**
```bash
# View headers
grep "^#" blog-workspace/archive/PROJECT_ID/sanity-ready-post.md

# Check meta description length
grep "metaDescription:" -A 1 blog-workspace/archive/PROJECT_ID/sanity-ready-post.md
```

## 📝 Step 10: Publish Your Post

### For Markdown Mode

1. **Copy the formatted content:**
```bash
# Copy to clipboard (Linux)
cat blog-workspace/archive/PROJECT_ID/sanity-ready-post.md | xclip -selection clipboard

# Or save to file for manual review
cp blog-workspace/archive/PROJECT_ID/sanity-ready-post.md ~/my-blog-post.md
```

2. **Import to Sanity:**
   - Open Sanity Studio
   - Go to "Posts" collection
   - Click "Create new post"
   - Fill in fields from YAML frontmatter
   - Paste content (after removing YAML)
   - Publish!

### For API Mode

```bash
# If you used API mode, check the response
cat blog-workspace/archive/PROJECT_ID/publishing-response.json | \
  python -m json.tool

# You'll see something like:
{
  "status": "success",
  "sanityResponse": {
    "documentId": "post-abc123",
    "url": "https://your-site.com/posts/getting-started-react-hooks-guide"
  }
}
```

## 🎓 What You Learned

### Technical Understanding

1. **Workflow Phases:** You saw how 6 agents work together sequentially
2. **State Management:** Project state tracked through state.json
3. **Artifacts:** Each phase produces files for the next phase
4. **Quality Scores:** SEO and style metrics ensure quality
5. **Publishing:** Two modes (markdown and API)

### Quality Achievement

**Target Metrics:**
- ✅ SEO Score: ≥70 (you likely got 80+)
- ✅ Style Score: ≥80 (you likely got 90+)
- ✅ Word Count: 1000-1500 words
- ✅ Time: <30 minutes
- ✅ Brand Voice: Professional & Friendly

## 🚀 Step 11: Try Another Post

Now that you understand the process:

### Personal Development Post

```bash
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "5 Morning Habits That Changed My Life" \
  --type personal-dev \
  --mode markdown
```

### API Publishing

```bash
# After configuring Sanity credentials
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "TypeScript Best Practices" \
  --type tech \
  --mode api
```

### Different Publishing Mode

```bash
# Ask which mode to use
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Building Better Habits" \
  --type personal-dev \
  --mode ask-user
```

## 📚 Understanding the Output

### Key Files Created

| File | Purpose | Phase |
|------|---------|-------|
| `state.json` | Workflow tracking | Orchestrator |
| `research-findings.json` | Research data | Research |
| `research-notes.md` | Human-readable notes | Research |
| `content-outline.md` | Structure | Synthesis |
| `draft-[type].md` | Initial content | Writing |
| `seo-metadata.json` | SEO metrics | SEO |
| `seo-optimized-draft.md` | SEO-optimized content | SEO |
| `style-report.md` | Style analysis | Review |
| `polished-draft.md` | Final content | Review |
| `sanity-ready-post.md` | CMS-ready output | Publishing |

### Quality Reports

**SEO Report (`seo-metadata.json`):**
- Overall score
- Breakdown by category
- Keyword density
- Recommendations

**Style Report (`style-report.md`):**
- Brand voice compliance
- Clarity metrics
- Before/after examples
- Final score

## 🎯 Tips for Success

### Choosing Topics

**Good Topics:**
- Specific and focused
- Has recent developments
- Practical value for readers
- Not overly saturated

**Bad Topics:**
- Too broad ("All of JavaScript")
- Too narrow ("Obscure edge case")
- No recent relevance
- Purely opinion without substance

### Getting Better Results

1. **Review research** - Check if sources are credible
2. **Refine outline** - Can be edited between phases
3. **Adjust brand style** - Modify voice if needed
4. **Check quality scores** - Aim for higher scores
5. **Review final output** - Always proofread before publishing

## ❓ Common Questions

**Q: Can I stop and restart?**
A: Yes! State is saved after each phase. Simply re-run the orchestrator and it will resume.

**Q: What if a phase fails?**
A: Check the error in `state.json`. The system retries 3 times automatically.

**Q: Can I modify content between phases?**
A: Yes! You can edit any file and the next phase will use your changes.

**Q: How do I check progress?**
A: Watch the state.json file: `watch cat state.json | grep status`

**Q: Where is my post if using API mode?**
A: Check Sanity Studio directly, or view `publishing-response.json`

## 🎉 Congratulations!

You've successfully:
- ✅ Created your first automated blog post
- ✅ Understood the complete workflow
- ✅ Reviewed quality metrics
- ✅ Learned where to find outputs
- ✅ Ready to create more posts!

## 📖 Next Steps

Now that you've created your first post:

1. **[Read the Workflow Guide](../guides/workflow.md)** - Deep dive into how it all works
2. **[Configure Sanity API](../guides/configuration.md)** - Enable automated publishing
3. **[Try Different Content Types](content-types.md)** - Personal development posts
4. **[Customize Brand Voice](../guides/configuration.md)** - Make it truly yours
5. **[Check Troubleshooting](../guides/troubleshooting.md)** - Be prepared for issues

**Happy blogging!** 🚀

---

**Tutorial Complete!** You've successfully run your first blog post through the 8-agent system.
