# CreateXThread Workflow

Transform a blog post into an engaging X (Twitter) thread that captures the essence of the content in a conversational, digestible format.

## Input

- Blog post content (from URL, file, or direct)
- Optional: Focus area or specific angle

## Process

### Step 1: Content Analysis

1. Read the full blog post
2. Identify the core message (1 sentence)
3. Extract 5-8 key insights or takeaways
4. Note any memorable quotes or statistics
5. Identify the target audience

### Step 2: Thread Structure

Design the thread with this structure:

```
Tweet 1: Hook (most important - appears in previews)
Tweet 2-3: Problem/Context setup
Tweet 4-7: Key insights (one per tweet)
Tweet 8-9: Summary/Recap
Tweet 10: CTA + Question
```

### Step 3: Write Each Tweet

For each tweet:
1. Draft the content
2. Check character count (max 280)
3. Ensure it can stand alone but flows in sequence
4. Add thread indicator (1/, 2/, etc.) if needed

### Step 4: Hook Tweet Rules

The first tweet MUST:
- Grab attention in first 5 words
- Create curiosity or promise value
- NOT be clickbait
- Use 🧵 emoji to indicate thread

Hook templates:
- "I spent [time] on [thing]. Here's what I learned:"
- "[Surprising insight] that changed how I [action]:"
- "The biggest mistake I see with [topic]:"
- "[Number] things I wish I knew about [topic]:"

### Step 5: Value Tweet Rules

Each value tweet should:
- Present ONE idea clearly
- Use short sentences
- Include specific examples when possible
- Create "aha" moments

Formatting options:
- Numbered lists (1. 2. 3.)
- Short paragraphs with line breaks
- Before → After comparisons
- "The problem: / The solution:"

### Step 6: CTA Tweet Rules

The final tweet should:
- Summarize the main takeaway
- Link to the full post
- End with a question to drive replies
- NOT use hashtags

CTA templates:
- "Full post with all the details: [link]\n\nWhat's your experience with [topic]?"
- "Want the complete guide? [link]\n\nWhich of these surprised you most?"

### Step 7: Validation

Before output:
- [ ] Each tweet under 280 characters
- [ ] First tweet hooks attention
- [ ] Thread flows logically
- [ ] No hashtags used
- [ ] Ends with engagement question
- [ ] Link included (in last tweet or reply)

## Output Format

```markdown
# X Thread: {Post Title}

**Source**: {URL or file}
**Thread Length**: {X} tweets
**Created**: {timestamp}

---

## Tweet 1 (Hook)
🧵 {hook content}

[X/280 characters]

---

## Tweet 2
{content}

[X/280 characters]

---

[... continue for all tweets ...]

---

## Tweet {N} (CTA)
{CTA content with link and question}

[X/280 characters]

---

## Thread Summary
- Total tweets: X
- Focus: {main topic}
- Key insights covered: {list}
- Engagement question: {question}
```

## Example Output

```markdown
# X Thread: Docker MCP - Connect AI to Your Containers

**Source**: sanity://post-docker-mcp-123
**Thread Length**: 8 tweets
**Created**: 2025-01-15T10:00:00Z

---

## Tweet 1 (Hook)
🧵 I just connected Claude to my Docker containers.

It can now spin up databases, check logs, and debug services - all through natural language.

Here's how Docker MCP works:

[187/280 characters]

---

## Tweet 2
First, what is MCP?

Model Context Protocol lets AI assistants use external tools.

Think of it as giving Claude "hands" to interact with your systems.

Docker MCP = Claude + Docker control.

[206/280 characters]

---

## Tweet 3
The setup takes 5 minutes:

1. Install Docker MCP server
2. Add to Claude's config
3. Restart Claude

That's it. No complex configuration needed.

[154/280 characters]

---

[... continues ...]

---

## Tweet 8 (CTA)
Full setup guide with code examples: https://example.com/docker-mcp

What container tasks would you automate with AI?

[123/280 characters]

---

## Thread Summary
- Total tweets: 8
- Focus: Docker MCP introduction and setup
- Key insights: What is MCP, setup process, use cases, benefits
- Engagement question: What container tasks would you automate?
```

## Completion Signal

```
COMPLETED: [AGENT:repurposer] X thread created - {N} tweets, hook: "{first 30 chars}..."
```
