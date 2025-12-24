# CreateNewsletter Workflow

Transform a blog post into an engaging email newsletter that delivers value directly to subscribers' inboxes.

## Input

- Blog post content (from URL, file, or direct)
- Optional: Subscriber segment or personalization

## Process

### Step 1: Content Analysis

1. Read the full blog post
2. Identify THE one big idea (newsletter focus)
3. Extract 3 key takeaways
4. Find the most actionable insight
5. Note any personal stories or examples

### Step 2: Newsletter Structure

```
Subject Line (3 options)
Preview Text (50-90 chars)
---
Personal Opening (1-2 sentences)
The Big Idea (2-3 sentences)
Key Takeaways (3 bullet points)
Your Action Step (1 clear action)
Personal Sign-off
P.S. (soft CTA)
---
Link to full post
```

### Step 3: Subject Line Rules

Write 3 subject line options using these formulas:

1. **Curiosity**: "The [thing] that changed how I [action]"
2. **Value**: "[Number] [things] for better [outcome]"
3. **Personal**: "I was wrong about [topic]"

Requirements:
- 30-50 characters (mobile-friendly)
- No spam triggers (FREE, ACT NOW, etc.)
- Creates curiosity without clickbait
- Personal and specific

### Step 4: Preview Text

The text that shows after subject line in inbox:
- 50-90 characters
- Complements (not repeats) subject line
- Creates additional curiosity
- Often starts with "Plus:" or continues the thought

### Step 5: Opening Rules

Start with a personal, relatable opening:
- Address reader directly ("Hey {FirstName}")
- Share a brief story or observation
- Connect to reader's experience
- Lead naturally into the topic

Templates:
- "I've been thinking about [topic] lately..."
- "Last week, something happened that changed my view on..."
- "You know that feeling when [relatable situation]?"

### Step 6: Big Idea Section

Present the core insight:
- One clear message
- Why it matters
- How you discovered it
- Keep to 2-3 sentences

### Step 7: Key Takeaways

Extract 3 actionable takeaways:
- Bold the key point
- Brief explanation
- Practical, applicable

Format:
```markdown
1. **[Takeaway]**: [1-2 sentence explanation]
2. **[Takeaway]**: [1-2 sentence explanation]
3. **[Takeaway]**: [1-2 sentence explanation]
```

### Step 8: Action Step

Give ONE specific action:
- Doable today
- Specific and clear
- Connected to the main insight
- Low friction to start

Templates:
- "Try this today: [specific action]"
- "Your homework: [simple task]"
- "One thing you can do right now: [action]"

### Step 9: Sign-off and P.S.

Personal sign-off:
- Keep your voice
- Warm but professional
- Your name

P.S. is highly read:
- Soft CTA to full post
- Additional value teaser
- Question to invite replies

### Step 10: Validation

Before output:
- [ ] Subject line under 50 characters
- [ ] Preview text 50-90 characters
- [ ] Personal opening connects to reader
- [ ] ONE clear big idea
- [ ] 3 concise takeaways
- [ ] ONE specific action step
- [ ] P.S. adds value
- [ ] Total length 300-500 words

## Output Format

```markdown
# Newsletter: {Post Title}

**Source**: {URL or file}
**Word Count**: {X} words
**Created**: {timestamp}

---

## Subject Line Options

1. {Option 1} [{X} chars]
2. {Option 2} [{X} chars]
3. {Option 3} [{X} chars]

## Preview Text

{Preview text} [{X} chars]

---

Hey {{FirstName}},

{Personal opening paragraph}

## The Big Idea

{Core insight from the post}

## Key Takeaways

1. **{Takeaway 1}**: {Explanation}

2. **{Takeaway 2}**: {Explanation}

3. **{Takeaway 3}**: {Explanation}

## Your Action Step

{One specific thing reader can do today}

{Personal sign-off},

{Name}

P.S. {Soft CTA or additional value} [Read the full post here]({URL})

---

## Newsletter Metadata
- Word count: {X}
- Reading time: ~{X} minutes
- Key topic: {topic}
- Call to action: {CTA description}
```

## Example Output

```markdown
# Newsletter: Docker MCP - AI Meets Containers

**Source**: sanity://post-docker-mcp-123
**Word Count**: 380 words
**Created**: 2025-01-15T10:00:00Z

---

## Subject Line Options

1. I gave Claude access to my Docker containers [45 chars]
2. The 5-minute setup that changed my workflow [42 chars]
3. What happens when AI controls your containers [46 chars]

## Preview Text

Plus: the exact commands I use daily [38 chars]

---

Hey {{FirstName}},

I spent way too long last week debugging a container issue. Checking logs, restarting services, inspecting configurations—you know the drill.

Then I remembered: I could just ask Claude to do it.

## The Big Idea

Docker MCP connects Claude directly to your Docker environment. Instead of typing commands, you describe what you want. "Show me the logs from the last hour" or "restart the database container." Claude handles the rest.

## Key Takeaways

1. **Setup takes 5 minutes**: Install the MCP server, add one config line, restart Claude. That's the entire process.

2. **Natural language > memorizing commands**: Forget the exact docker logs syntax. Just describe what you need.

3. **It's safer than you think**: Claude shows you what it's about to do before executing. You stay in control.

## Your Action Step

Try this today: Install Docker MCP (link in the full post) and ask Claude to list your running containers. See how it feels to manage Docker with conversation.

Talk soon,

Tuan

P.S. I put together a complete setup guide with all the commands and configuration examples. [Read the full post here](https://example.com/docker-mcp)

---

## Newsletter Metadata
- Word count: 380
- Reading time: ~2 minutes
- Key topic: Docker MCP setup and benefits
- Call to action: Install and try Docker MCP
```

## Completion Signal

```
COMPLETED: [AGENT:repurposer] Newsletter created - {X} words, subject: "{subject line}"
```
