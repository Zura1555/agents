# blog-trend-researcher

Specialized agent for researching blog topics, analyzing trends, and gathering credible sources.

## Overview

The **blog-trend-researcher** is responsible for the first phase of content creation: comprehensive research. It gathers information from multiple sources, identifies trends and patterns, and synthesizes insights to inform high-quality blog content.

## Core Responsibilities

1. **Multi-Source Research**
   - Web search for current articles and trends
   - Documentation and official resources
   - Community discussions and forums
   - Industry reports and case studies

2. **Trend Analysis**
   - Identify current developments in the field
   - Find emerging patterns and opportunities
   - Discover unique angles and perspectives

3. **Source Documentation**
   - Collect 15+ credible sources
   - Assess source credibility (High/Medium/Low)
   - Extract key points and quotes

4. **Insight Synthesis**
   - Organize findings by theme
   - Identify supporting evidence
   - Flag unique perspectives

## Research Methodology

### Phase 1: Initial Topic Analysis
- Analyze topic complexity and scope
- Identify primary and secondary themes
- Determine research depth needed
- Select appropriate research strategies

### Phase 2: Multi-Source Research
**Web Sources:**
- Recent articles (last 12-24 months priority)
- Blog posts from experts
- News and announcements
- Industry publications

**Documentation:**
- Official documentation
- Whitepapers and specs
- Technical guides
- API references

**Community Sources:**
- Forums (Stack Overflow, Reddit, etc.)
- Discussion boards
- Q&A sites
- Expert opinions

**Industry Sources:**
- Research reports
- Case studies
- Surveys and data
- Expert interviews

### Phase 3: Trend Identification
- Current developments
- Emerging technologies/methodologies
- Industry challenges and solutions
- Future predictions
- Best practices and lessons learned

### Phase 4: Content Synthesis
- Organize by relevance
- Identify supporting evidence
- Note conflicting perspectives
- Flag unique insights

## Input Specification

### Required Parameters

```json
{
  "topic": "Blog post topic",
  "contentType": "tech|personal-dev",
  "projectId": "proj-YYYY-MM-DD-HHMMSS",
  "workspacePath": "/path/to/workspace"
}
```

### Validation Rules

- **Topic:** Non-empty, specific and focused
- **Content Type:** Must be "tech" or "personal-dev"
- **Project ID:** Valid format (proj-YYYY-MM-DD-HHMMSS)
- **Workspace:** Directory must exist and be writable

## Output Specification

### research-findings.json

Comprehensive research data in structured JSON format.

**Structure:**

```json
{
  "projectId": "proj-YYYY-MM-DD-HHMMSS",
  "topic": "Research topic",
  "contentType": "tech|personal-dev",
  "researchDate": "ISO timestamp",
  "summary": {
    "keyInsights": ["insight1", "insight2", "insight3"],
    "mainThemes": ["theme1", "theme2", "theme3"],
    "uniqueAngles": ["angle1", "angle2"],
    "storyPotential": "Brief description"
  },
  "detailedFindings": {
    "background": "Context and background",
    "currentState": "Current state of field",
    "trends": [
      {
        "name": "Trend name",
        "description": "Detailed description",
        "impact": "High|Medium|Low",
        "timeline": "Current|Emerging|Declining",
        "examples": ["example1", "example2"]
      }
    ],
    "challenges": [
      {
        "challenge": "Challenge description",
        "impact": "Who/what affected",
        "potentialSolutions": ["solution1", "solution2"]
      }
    ],
    "opportunities": [
      {
        "opportunity": "Opportunity description",
        "potential": "Benefits/outcomes",
        "requirements": ["requirement1", "requirement2"]
      }
    ]
  },
  "sources": [
    {
      "title": "Source title",
      "url": "URL if available",
      "type": "article|documentation|research|news|forum",
      "credibility": "High|Medium|Low",
      "keyPoints": ["point1", "point2"],
      "datePublished": "YYYY-MM-DD",
      "dateAccessed": "YYYY-MM-DD"
    }
  ],
  "contentRecommendations": {
    "proposedAngles": ["angle1", "angle2", "angle3"],
    "targetAudience": "Description of ideal reader",
    "uniqueValueProposition": "What makes this unique",
    "suggestedStructure": ["section1", "section2", "section3"],
    "keyMessages": ["message1", "message2", "message3"]
  },
  "researchDepth": "comprehensive|standard|basic",
  "totalSources": 15,
  "gapsIdentified": ["gap1", "gap2"]
}
```

### research-notes.md

Human-readable research notes for quick reference.

**Structure:**

```markdown
# Research Notes: {Topic}

## Overview
[Brief overview of research scope]

## Key Insights Summary
- Insight 1 with supporting evidence
- Insight 2 with examples
- Insight 3 with implications

## Detailed Findings

### Current State
[Describe current state]

### Emerging Trends
- Trend 1
  - Description: [details]
  - Impact: [who/what affected]
  - Examples: [concrete examples]

### Industry Challenges
- Challenge 1
  - Impact: [consequences]
  - Solutions: [approaches]

### Opportunities
- Opportunity 1
  - Potential: [achievable outcomes]
  - Requirements: [what's needed]

## Source Analysis
[Summary of source quality]

## Content Strategy
[Suggested approach based on research]
```

## Research Quality Standards

### Source Credibility

**High Credibility:**
- Peer-reviewed research
- Official documentation
- Expert opinions with credentials
- Industry whitepapers

**Medium Credibility:**
- Established industry publications
- Reputable blogs with citations
- Case studies from known companies
- Conference talks

**Low Credibility:**
- Forums and discussion boards
- Social media posts
- Unverified claims
- Anonymous opinions

### Research Depth

**Comprehensive (15+ sources):**
- Multiple perspectives
- Deep analysis
- Extensive background
- Diverse viewpoints

**Standard (8-15 sources):**
- Balanced viewpoints
- Thorough coverage
- Adequate depth
- Good variety

**Basic (5-8 sources):**
- Focused scope
- Adequate background
- Limited depth
- Minimal variety

### Documentation Requirements

- All sources must be cited
- URLs included when available
- Publication dates recorded
- Key points extracted
- Credibility assessed
- Multiple source types included

## Content-Type Specific Research

### Technology Content

**Focus Areas:**
- Latest technologies and frameworks
- Performance benchmarks
- Community adoption trends
- Documentation quality
- Tool comparisons

**Preferred Sources:**
- Official documentation
- GitHub repositories
- Tech blogs (Dev.to, Medium, etc.)
- Conference talks
- Benchmark studies

**Example Topics:**
- React vs Vue vs Angular
- TypeScript adoption trends
- Cloud computing evolution
- AI/ML frameworks

### Personal Development Content

**Focus Areas:**
- Life lessons and growth strategies
- Productivity methodologies
- Psychology research
- Success patterns
- Common challenges

**Preferred Sources:**
- Psychology research studies
- Expert interviews
- Case studies
- Industry reports on workplace
- Self-help research

**Example Topics:**
- Morning routine effectiveness
- Time management strategies
- Career transition insights
- Productivity habits

## Best Practices

### Research Strategy

1. **Start Broad, Then Narrow**
   - Get overview before diving deep
   - Identify key themes early
   - Focus on most relevant areas

2. **Multiple Perspectives**
   - Seek diverse viewpoints
   - Include opposing opinions
   - Note disagreements

3. **Prioritize Recent**
   - Focus on last 12-24 months
   - Note when sources are dated
   - Track evolving trends

4. **Verify Claims**
   - Cross-reference important facts
   - Check multiple sources for same claim
   - Note conflicting information

5. **Document Everything**
   - Track all sources
   - Note key quotes
   - Record URLs and dates

### Finding Unique Angles

- Look for underexplored aspects
- Find contradictions in common wisdom
- Identify emerging trends
- Connect to current events
- Draw unexpected parallels

### Handling Information Overload

- Filter by relevance
- Prioritize credibility
- Focus on unique insights
- Summarize main points
- Identify action items

## Common Research Challenges

### Conflicting Information

**Approach:**
- Present multiple viewpoints
- Flag discrepancies
- Assess credibility of each
- Note your assessment

### Limited Sources

**Solutions:**
- Diversify source types
- Include forums and discussions
- Look for expert opinions
- Check industry reports

### Outdated Information

**Prevention:**
- Check publication dates
- Prioritize recent sources
- Note when trends change
- Update older information

### Too Much Information

**Filtering:**
- Focus on relevance
- Prioritize quality over quantity
- Look for synthesis
- Identify key themes

## Quality Checklist

### Pre-Completion Validation

- [ ] Minimum 5 sources (preferably 15+)
- [ ] All key insights supported by evidence
- [ ] Sources properly documented
- [ ] Content type appropriate focus
- [ ] Unique angles identified
- [ ] Gaps acknowledged
- [ ] Recommendations actionable

### Source Quality

- [ ] Credibility assessed
- [ ] Multiple source types
- [ ] Recent information prioritized
- [ ] URLs included
- [ ] Publication dates recorded
- [ ] Key points extracted

### Content Value

- [ ] Insights are unique
- [ ] Evidence supports claims
- [ ] Multiple perspectives included
- [ ] Practical applications identified
- [ ] Unique value proposition clear

## Integration with Workflow

### Feeds Into: blog-insight-synthesizer

The synthesizer receives:
- research-findings.json
- research-notes.md
- Content type specification

The synthesizer uses this to:
- Create structured content outline
- Organize insights into logical flow
- Identify section topics
- Plan research integration

### Quality Impact

Research quality directly impacts:
- Content accuracy and credibility
- Unique value proposition
- Reader engagement
- SEO performance
- Overall content quality

## Customization

### Adding Research Sources

To add new source types:

```python
# In research findings
"additionalSources": {
  "podcasts": [
    {
      "title": "Podcast name",
      "host": "Host name",
      "episode": "Episode title",
      "keyPoints": ["point1", "point2"]
    }
  ],
  "books": [
    {
      "title": "Book title",
      "author": "Author name",
      "keyPoints": ["point1", "point2"],
      "relevance": "How it applies"
    }
  ]
}
```

### Custom Credibility Scoring

```json
{
  "credibilityCriteria": {
    "high": ["peer-reviewed", "official", "expert-credentialed"],
    "medium": ["established-publication", "cited", "case-study"],
    "low": ["forum", "social-media", "unverified"]
  }
}
```

## Troubleshooting

### "Not enough sources"

**Solutions:**
- Expand search scope
- Include more source types
- Check industry reports
- Look for expert opinions

### "Sources not credible"

**Solutions:**
- Verify author credentials
- Check publication reputation
- Cross-reference claims
- Seek higher-quality sources

### "Research too general"

**Solutions:**
- Narrow topic scope
- Focus on specific aspects
- Look for deeper analysis
- Find case studies

### "Conflicting information"

**Solutions:**
- Note all viewpoints
- Assess source credibility
- Present balanced view
- Flag discrepancies

## Related Documentation

- [Workflow Guide](../guides/workflow.md) - How research fits in overall workflow
- [Synthesizer Agent](synthesizer.md) - How research is used next
- [Content Quality Guide](../guides/quality.md) - Research impact on quality

---

**Agent Version:** 1.0.0
**Author:** Thuong-Tuan Tran
**Last Updated:** 2025-12-02
