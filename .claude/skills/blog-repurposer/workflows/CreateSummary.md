# CreateSummary Workflow

Generate platform-specific summaries from a blog post, optimized for LinkedIn, YouTube, and Instagram.

## Input

- Blog post content (from URL, file, or direct)
- Target platform: linkedin | youtube | instagram
- Optional: Specific focus or angle

## Process

### Platform-Specific Generation

---

## LinkedIn Summary

### Structure
```
Hook line (question or bold statement)
Personal story/context (2-3 sentences)
Key insight
Supporting points (3 bullets)
Thought-provoking question
```

### Rules
- 150-300 words total
- First 2 lines visible before "see more"
- NO hashtags (they reduce reach)
- Max 2 emojis (optional)
- End with question to drive comments
- Professional but personal voice

### Template
```markdown
{Hook - question or statement that stops the scroll}

{Personal context - how you encountered this}

Here's what I learned:

→ {Point 1}
→ {Point 2}
→ {Point 3}

{Insight or reflection}

{Thought-provoking question to encourage discussion}
```

### Validation
- [ ] Under 300 words
- [ ] Strong hook in first 2 lines
- [ ] No hashtags
- [ ] Ends with question
- [ ] Personal voice maintained

---

## YouTube Description

### Structure
```
1-2 sentence summary
Timestamps (if applicable)
Key topics covered
Links section
Keywords (for SEO)
```

### Rules
- 200-300 words total
- First 100 chars most important (shown in search)
- Include relevant keywords naturally
- Timestamps format: 0:00 - Topic
- Links at the end
- SEO-focused

### Template
```markdown
{1-2 sentence hook/summary}

In this video, I cover:
• {Topic 1}
• {Topic 2}
• {Topic 3}

⏱️ Timestamps:
0:00 - Introduction
0:45 - {First topic}
2:30 - {Second topic}
5:00 - {Key insight}
7:15 - Conclusion

📚 Resources mentioned:
• {Resource 1}: {URL}
• {Resource 2}: {URL}

📖 Read the full blog post: {URL}

🔔 Subscribe for more content on {topic area}

#keywords #for #youtube #seo
```

### Validation
- [ ] Strong first sentence (shows in search)
- [ ] Logical timestamp order
- [ ] Relevant links included
- [ ] Keywords present
- [ ] Under 300 words

---

## Instagram Caption

### Structure
```
Hook (first line most important)
Brief value/insight
Call to action
```

### Rules
- 100-150 words max
- First line = hook (shows before "more")
- Conversational and casual
- 1-2 emojis okay
- End with soft CTA
- Save hashtags for first comment

### Template
```markdown
{Hook line - attention grabber}

{2-3 sentences of value - the key insight from the post}

{Brief personal touch}

{Soft CTA - save this, share with someone who needs it, drop a comment}

.
.
.
Link in bio for full post 👆
```

### Validation
- [ ] Under 150 words
- [ ] Strong hook in first line
- [ ] Clear value proposition
- [ ] Minimal emojis
- [ ] CTA present

---

## Output Format

```markdown
# {Platform} Summary: {Post Title}

**Source**: {URL or file}
**Platform**: {linkedin|youtube|instagram}
**Created**: {timestamp}

---

{Platform-specific content}

---

## Metadata
- Word count: {X}
- Character count: {Y}
- Key topic: {topic}
- CTA type: {question|link|action}
```

## Example: LinkedIn Output

```markdown
# LinkedIn Summary: Docker MCP - AI Meets Containers

**Source**: sanity://post-docker-mcp-123
**Platform**: linkedin
**Created**: 2025-01-15T10:00:00Z

---

What if you could manage Docker containers just by describing what you want?

Last week I spent hours debugging a container issue. Checking logs, restarting services, the usual dance. Then I tried something different—I asked Claude to do it.

Docker MCP connects AI directly to your container environment. Here's what changed:

→ No more memorizing docker command syntax
→ Natural language queries return exactly what I need
→ Claude shows commands before executing (you stay in control)

The setup took 5 minutes. The productivity gain? Hours per week.

What container management tasks would you automate if you could just describe them in plain English?

---

## Metadata
- Word count: 108
- Character count: 672
- Key topic: Docker MCP productivity benefits
- CTA type: question
```

## Completion Signal

```
COMPLETED: [AGENT:repurposer] {Platform} summary created - {X} words
```
