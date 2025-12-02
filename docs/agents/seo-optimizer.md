# seo-content-optimizer

Specialized agent for optimizing blog content for search engines while maintaining readability and user value.

## Overview

The **seo-content-optimizer** enhances blog content for search engine discoverability through keyword integration, structural optimization, and technical SEO improvements, all while preserving content quality and readability.

## Core Responsibilities

1. **Keyword Integration**
   - Identify primary and secondary keywords
   - Naturally integrate keywords throughout content
   - Optimize keyword density (1-2% for primary)

2. **On-Page SEO**
   - Optimize title tags and meta descriptions
   - Structure headers with keywords (H1, H2, H3)
   - Optimize URL slugs

3. **Content Structure**
   - Organize content for both users and search engines
   - Improve content flow and hierarchy
   - Add internal and external links

4. **SEO Scoring**
   - Evaluate optimization across multiple dimensions
   - Provide actionable recommendations
   - Track improvements over time

## SEO Strategy

### Phase 1: Keyword Research & Planning
- Identify primary and secondary keywords
- Analyze search intent and competition
- Map keywords to content sections
- Plan keyword distribution

### Phase 2: On-Page Optimization
- Optimize title and meta description
- Structure headers with target keywords
- Create SEO-friendly URLs
- Add internal and external links

### Phase 3: Content Optimization
- Integrate keywords naturally
- Optimize image alt text
- Improve content quality
- Ensure user value

### Phase 4: Technical SEO
- Check structure and formatting
- Optimize for mobile
- Ensure crawlable structure
- Validate SEO elements

## Input Specification

### Required Parameters

```json
{
  "projectId": "proj-YYYY-MM-DD-HHMMSS",
  "contentFile": "draft-[type].md",
  "metadataFile": "draft-metadata.json",
  "seoRequirements": {
    "primaryKeyword": "main target keyword",
    "secondaryKeywords": ["kw1", "kw2", "kw3"],
    "focusKeyword": "most important keyword",
    "targetSearchIntent": "informational|transactional|navigational"
  }
}
```

### Expected Files

- `draft-tech.md` or `draft-personal-dev.md`
- `draft-metadata.json`

### Validation

- Verify draft content exists and is complete
- Check metadata structure
- Confirm SEO requirements provided
- Validate content type alignment

## Output Specification

### seo-optimized-draft.md

Content with SEO optimizations applied while maintaining readability.

**Structure:**

```markdown
---
title: "{SEO-Optimized Title}"
slug: "{url-friendly-slug}"
description: "{Compelling meta description (150-160 chars)}"
keywords: "{primary, secondary, keywords, here}"
publishedAt: "{ISO timestamp}"
author: "Thuong-Tuan Tran"
seoScore: {score}/100
---

# {Optimized H1 with Primary Keyword}

> {Engaging intro with keyword naturally integrated}

## Introduction (keyword in first 100 words)
[Content with natural keyword integration]

## Section 1: {H2 with Keyword}
### Subsection: {H3 with Keyword}

[Content with natural keyword integration]
- Bullet with LSI keyword
- Bullet with related keyword

## Section 2: {H2 with Keyword}

[Continue optimization pattern]

## Conclusion (keywords in summary)

[Recap with primary keyword in first sentence]
```

### seo-metadata.json

Detailed SEO metrics and recommendations.

**Structure:**

```json
{
  "projectId": "proj-YYYY-MM-DD-HHMMSS",
  "seo": {
    "score": 0,
    "scoreBreakdown": {
      "keywordOptimization": 0-100,
      "contentStructure": 0-100,
      "readability": 0-100,
      "technicalSeo": 0-100,
      "userValue": 0-100
    },
    "keywords": {
      "primary": "keyword",
      "secondary": ["kw1", "kw2", "kw3"],
      "longTail": ["long keyword phrase 1", "long keyword phrase 2"],
      "lsi": ["semantically related keyword 1", "related keyword 2"],
      "density": {
        "primary": "X% (optimal: 1-2%)",
        "secondary": "X% (optimal: 0.5-1% each)"
      }
    },
    "titles": {
      "h1": "{Optimized H1}",
      "metaTitle": "{50-60 char SEO title}",
      "titleLength": 0
    },
    "metaDescription": {
      "content": "{Compelling description}",
      "length": 0,
      "includesPrimaryKeyword": true,
      "includesCTA": true
    },
    "headers": {
      "h1Count": 1,
      "h2Count": 0,
      "h3Count": 0,
      "keywordInHeaders": true,
      "headerStructure": "optimal|suboptimal"
    },
    "content": {
      "wordCount": 0,
      "keywordInFirst100Words": true,
      "keywordInLast100Words": true,
      "keywordDistribution": "even|concentrated|sparse"
    },
    "links": {
      "internalLinks": 0,
      "externalLinks": 0,
      "anchorTextOptimization": "good|needs-improvement"
    },
    "images": {
      "total": 0,
      "withAltText": 0,
      "altTextOptimized": 0
    },
    "readability": {
      "score": 0,
      "gradeLevel": "X",
      "avgSentenceLength": "X words",
      "paragraphLength": "avg X sentences"
    }
  },
  "recommendations": [
    {
      "category": "keyword-optimization|content|technical|links|images",
      "issue": "Description of issue",
      "severity": "high|medium|low",
      "recommendation": "Specific action to take",
      "example": "Example of better approach"
    }
  ],
  "searchIntentMatch": {
    "intent": "informational|transactional|navigational",
    "matchScore": 0-100,
    "contentAligns": true
  }
}
```

## Keyword Strategy

### Primary Keyword Selection

**Criteria:**
- Single, specific keyword or phrase
- Moderate to high search volume
- Reasonable competition level
- Matches user search intent
- Natural integration possible

**Examples:**
- Tech: "react hooks tutorial", "typescript best practices"
- Personal Dev: "morning routine habits", "productivity tips"

### Secondary Keywords

**Purpose:**
- Support primary keyword
- Cover topic comprehensively
- Include variations and synonyms

**Count:** 3-5 secondary keywords

**Types:**
- Related terms
- Long-tail variations
- LSI (Latent Semantic Indexing) keywords

### Keyword Placement

1. **Title Tag (H1)** - Include primary keyword near beginning
2. **First 100 Words** - Natural integration early
3. **Headers (H2/H3)** - Distribute keywords across headers
4. **Body Text** - 1-2% density for primary
5. **Meta Description** - Include and entice clicks
6. **URL Slug** - Short, keyword-rich
7. **Alt Text** - Descriptive with keywords

### Keyword Density

- **Primary Keyword:** 1-2% (optimal)
- **Secondary Keywords:** 0.5-1% each
- **LSI Keywords:** Throughout naturally
- **Total:** Don't over-optimize (>3%)

## Optimization Techniques

### Title Optimization

**Best Practices:**
- Include primary keyword near beginning
- Keep under 60 characters
- Make compelling and clickable
- Avoid keyword stuffing
- Match search intent

**Examples:**
- ❌ "React Hooks Guide Tutorial Best Practices Complete"
- ✅ "React Hooks: A Complete Guide for Developers"

### Header Structure

**Guidelines:**
- Only one H1 per page
- Use H2 for major sections
- Use H3 for subsections
- Include keywords in 60% of headers
- Make headers descriptive

**Example Structure:**
```
# React Hooks: Complete Guide (H1 - Primary keyword)

## Understanding React Hooks (H2 - Primary keyword)
### useState Hook Explained (H3 - Secondary keyword)

## Advanced Hook Patterns (H2)
### Custom Hook Creation (H3)
```

### Meta Description

**Requirements:**
- 150-160 characters
- Include primary keyword
- Create compelling call-to-action
- Summarize page value
- Avoid duplicate meta descriptions

**Example:**
```
Master React Hooks with this comprehensive guide. Learn useState, useEffect, and custom hooks with practical examples. Start building better React apps today!
(155 characters)
```

### Content Optimization

**Natural Integration:**
- Write for humans first
- Use keyword variations
- Include synonyms and related terms
- Avoid keyword stuffing
- Maintain readability

**Example Transformation:**

❌ **Stuffed:** "React hooks are hooks that you use in React to manage state and lifecycle. React hooks make React development easier."

✅ **Natural:** "React hooks revolutionized state management in React applications. These functions simplify handling component state and side effects."

## Technical SEO

### URL Structure

**Best Practices:**
- Short and descriptive
- Include primary keyword
- Use hyphens to separate words
- Avoid dates (unless relevant)
- Keep lowercase

**Examples:**
- ❌ `/posts/2024/01/15/post123`
- ✅ `/posts/react-hooks-complete-guide`

### Image Optimization

**Requirements:**
- Descriptive filenames with keywords
- Alt text describing image content
- Compressed file sizes
- Relevant to content
- Appropriate formats (WebP, JPEG, PNG)

### Internal Linking

**Strategy:**
- Link to related content
- Use descriptive anchor text
- Don't over-optimize anchor text
- Create logical site structure
- Link deep within content

**Example:**
- ❌ "Click here"
- ✅ "Learn more about useState in our React hooks guide"

### External Linking

**Guidelines:**
- Link to authoritative sources
- Support claims with citations
- Use "nofollow" for untrusted sources
- Include diverse, relevant domains
- Don't link to competitors

## SEO Scoring System

### Scoring Categories (100 points total)

#### Keyword Optimization (25 points)
- Primary keyword in title: 5 pts
- Keyword density 1-2%: 5 pts
- Keywords in headers: 5 pts
- Keyword in first/last 100 words: 5 pts
- LSI keywords included: 5 pts

#### Content Structure (25 points)
- Single H1 tag: 5 pts
- Proper header hierarchy: 5 pts
- Logical content flow: 5 pts
- Readable paragraph length: 5 pts
- Clear sections and transitions: 5 pts

#### Technical SEO (25 points)
- Meta description optimized: 5 pts
- URL slug optimized: 5 pts
- Image alt text: 5 pts
- Internal/external links: 5 pts
- Schema markup (if applicable): 5 pts

#### User Value (25 points)
- Content depth and quality: 10 pts
- Unique insights or perspectives: 5 pts
- Actionable takeaways: 5 pts
- Engagement elements: 5 pts

### Score Interpretation

- **90-100:** Excellent SEO optimization
- **80-89:** Good optimization with minor improvements
- **70-79:** Adequate optimization (MINIMUM TARGET)
- **60-69:** Basic optimization, needs work
- **Below 60:** Poor optimization, significant improvements needed

## Content-Type Considerations

### Technology Content SEO

**Focus:**
- Technology-specific keywords
- Version numbers in URLs
- Documentation links
- Code-related LSI keywords
- Developer search intent

**Example Keywords:**
- "React hooks tutorial"
- "TypeScript vs JavaScript"
- "Next.js performance optimization"

### Personal Development SEO

**Focus:**
- Emotional and aspirational keywords
- "How to" and "guide" modifiers
- Research-backed resources
- Life improvement intent
- Long-tail variations

**Example Keywords:**
- "how to build better habits"
- "morning routine for success"
- "productivity tips for developers"

## Best Practices

### Optimization Balance

1. **User-First Approach**
   - SEO should enhance, not harm readability
   - Natural language over keyword stuffing
   - User value over search manipulation

2. **Quality Preservation**
   - Don't compromise content for SEO
   - Maintain engaging writing
   - Preserve brand voice

3. **Sustainable Optimization**
   - Focus on long-term gains
   - Avoid black-hat techniques
   - Build for user satisfaction

### Readability Maintenance

**Reader-Friendly Practices:**
- Short paragraphs (3-4 sentences)
- Bullet points and lists
- White space for scanning
- Bold key phrases (sparingly)
- Clear transitions

## Quality Checklist

### Pre-Publishing Validation

- [ ] Primary keyword targeted and integrated
- [ ] Secondary keywords support primary
- [ ] Keywords naturally integrated (no stuffing)
- [ ] Keyword density within optimal range
- [ ] LSI keywords included
- [ ] Meta title under 60 characters
- [ ] Meta description 150-160 characters
- [ ] URL slug short and descriptive
- [ ] Single H1 tag
- [ ] Proper header hierarchy
- [ ] Images have descriptive alt text
- [ ] Internal and external links present
- [ ] Readability maintained
- [ ] User value not compromised

### SEO Score Validation

- [ ] Score ≥ 70/100 (minimum target)
- [ ] All categories above 60%
- [ ] Recommendations addressed
- [ ] No critical issues

## Common Issues

### Keyword Stuffing

**Problem:** Overuse of keywords makes content unreadable

**Solution:**
- Prioritize natural language
- Use keyword variations
- Focus on user value
- Maintain readability

### Thin Content

**Problem:** Not enough substance to rank

**Solution:**
- Add valuable insights
- Include examples and data
- Provide comprehensive coverage
- Address user intent fully

### Poor Header Structure

**Problem:** Missing hierarchy confuses users and search engines

**Solution:**
- Use single H1
- Organize with H2 and H3
- Make headers descriptive
- Include keywords naturally

## Integration with Workflow

### Feeds Into: style-guardian

The style guardian receives:
- seo-optimized-draft.md
- seo-metadata.json

The style guardian uses this to:
- Maintain SEO structure while polishing
- Ensure brand voice consistency
- Preserve optimization efforts
- Enhance readability

### Impact on Overall Quality

SEO optimization affects:
- Search engine rankings
- Click-through rates
- Organic traffic
- Content discoverability
- Reader engagement

## Customization

### Custom Keyword Sources

```json
{
  "seoRequirements": {
    "primaryKeyword": "user-provided or auto-detected",
    "secondaryKeywords": ["user", "identified", "keywords"],
    "competitorKeywords": ["from competitor analysis"],
    "searchVolume": {
      "primary": "monthly search volume",
      "secondary": ["volume for each"]
    }
  }
}
```

### Custom Scoring Weights

Adjust category weights based on priorities:

```json
{
  "scoringWeights": {
    "keywordOptimization": 0.30,
    "contentStructure": 0.25,
    "technicalSeo": 0.20,
    "userValue": 0.25
  }
}
```

## Related Documentation

- [Workflow Guide](../guides/workflow.md) - How SEO fits in overall workflow
- [Style Guardian](style-guardian.md) - Next phase in pipeline
- [SEO Best Practices](https://moz.com/beginners-guide-to-seo) - External resource

---

**Agent Version:** 1.0.0
**Author:** Thuong-Tuan Tran
**Last Updated:** 2025-12-02
