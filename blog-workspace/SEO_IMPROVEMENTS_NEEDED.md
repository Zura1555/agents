# SEO Skills/Agents Improvements Needed

## Overview
The blog writing and publishing workflow needs significant improvements to properly populate ALL Sanity schema fields on the first attempt, without requiring manual retries or user input.

## Missing Schema Fields (Current Issues)

### 1. Post Document Schema Fields
**Missing/Currently Not Populated:**
- ✅ Categories (reference to category document) - FIXED
- ❌ Author (reference to person document) - May not be properly set
- ❌ Published At (datetime) - May not be set correctly
- ❌ Cover Image (image with alt text) - Not populated
- ❌ Date (datetime) - Not populated

### 2. SEO Fields Schema (seoFields object)
**Missing/Currently Not Populated:**
- ✅ Meta Title (seo.title) - FIXED but was missing initially
- ✅ Meta Description (seo.description) - FIXED but exceeded length initially
- ❌ Meta Image (seo.metaImage) - Image field not populated
- ❌ Keywords (seo.keywords) - May not be properly set as array
- ❌ Canonical URL (seo.canonicalUrl) - FIXED but was missing initially
- ❌ Robots (seo.robots) - Not populated (index, follow)
- ❌ Additional Meta Attributes (seo.metaAttributes) - Not populated

### 3. Open Graph Schema (openGraph object)
**Missing/Currently Not Populated:**
- ✅ OG Title (seo.openGraph.title) - FIXED
- ✅ OG Description (seo.openGraph.description) - FIXED but exceeded length initially
- ✅ OG Type (seo.openGraph.type) - FIXED
- ✅ OG URL (seo.openGraph.url) - FIXED but was missing initially
- ✅ OG Site Name (seo.openGraph.siteName) - FIXED but was missing initially
- ❌ OG Image (seo.openGraph.image) - Not populated
- ❌ OG Image Width/Height - Not set
- ❌ OG Locale - Not set
- ❌ Article Published Time (seo.openGraph.article.publishedTime) - Not populated
- ❌ Article Modified Time (seo.openGraph.article.modifiedTime) - Not populated
- ❌ Article Author (seo.openGraph.article.author) - Not populated
- ❌ Article Section (seo.openGraph.article.section) - Not populated
- ❌ Article Tags (seo.openGraph.article.tags) - Not populated

### 4. Twitter Schema (twitter object)
**Missing/Currently Not Populated:**
- ✅ Twitter Card (seo.twitter.card) - FIXED
- ✅ Twitter Title (seo.twitter.title) - FIXED
- ✅ Twitter Description (seo.twitter.description) - FIXED
- ❌ Twitter Site (seo.twitter.site) - Not populated (@username)
- ❌ Twitter Creator (seo.twitter.creator) - Not populated (@username)
- ❌ Twitter Image (seo.twitter.image) - Not populated
- ❌ Twitter Image Alt (seo.twitter.image.alt)## Character Limit Issues

### Meta Description - Not populated


- **Current Issue**: 185 characters (exceeds recommended 160)
- **Recommendation**: Keep under 155-160 characters for best SEO
- **Current Fix**: "Discover how Docker MCP solves the Model Context Protocol's context crisis with 98.7% token reduction. Real benchmarks & cost analysis."

### Open Graph Description
- **Current Issue**: 131 characters (exceeds recommended 120 for some platforms)
- **Recommendation**: Keep under 100-120 characters for optimal display
- **Current Fix**: "Docker MCP reduces AI agent token usage by 98.7%. Real benchmarks & cost analysis included."

## Required Improvements to Skills/Agents

### 1. seo-content-optimizer Skill
**Needs Enhancement:**
- ✅ Character limit validation for meta description (under 160 chars)
- ✅ Character limit validation for OG description (under 120 chars)
- ✅ Automatic character counting and shortening
- ❌ **MISSING**: Open Graph image dimension specifications (1200x630px)
- ❌ **MISSING**: Twitter card image optimization
- ❌ **MISSING**: Canonical URL generation from post slug
- ❌ **MISSING**: OG article metadata (publishedTime, modifiedTime, author, section, tags)
- ❌ **MISSING**: Twitter site and creator username handling
- ❌ **MISSING**: Robots meta tags (index, follow)
- ❌ **MISSING**: Additional meta attributes array

### 2. sanity-publisher Skill
**Needs Enhancement:**
- ❌ **CRITICAL**: Must populate ALL schema fields on first attempt
- ❌ **CRITICAL**: Must separate SEO metadata from content (currently mixing them)
- ❌ **CRITICAL**: Must validate schema compliance before publishing
- ❌ **MISSING**: Category reference handling (array of references)
- ❌ **MISSING**: Author reference validation
- ❌ **MISSING**: Cover image handling with alt text
- ❌ **MISSING**: PublishedAt and Date field population
- ❌ **MISSING**: Open Graph image upload and asset creation
- ❌ **MISSING**: Twitter image handling
- ❌ **MISSING**: Meta image handling for SEO

### 3. blog-master-orchestrator Skill
**Needs Enhancement:**
- ❌ **MISSING**: Schema validation step before publishing
- ❌ **MISSING**: Complete metadata checklist
- ❌ **MISSING**: Error handling for missing required fields
- ❌ **MISSING**: Auto-retry logic with proper field population

## Ideal Workflow (First Attempt Success)

### Phase 4: SEO Optimization (seo-content-optimizer)
**MUST populate:**
```
seo = {
  title: "Optimized meta title (50-60 chars)",
  description: "Optimized meta description (under 160 chars)",
  keywords: ["keyword1", "keyword2", "keyword3"],
  canonicalUrl: "https://site.com/post-slug",
  robots: { noFollow: false, noIndex: false },
  openGraph: {
    title: "OG title (60-90 chars)",
    description: "OG description (under 120 chars)",
    type: "article",
    url: "https://site.com/post-slug",
    siteName: "Site Name",
    image: { url: "image-url", width: 1200, height: 630, alt: "alt text" },
    article: {
      publishedTime: "ISO timestamp",
      modifiedTime: "ISO timestamp",
      author: "Author Name",
      section: "Category",
      tags: ["tag1", "tag2"]
    }
  },
  twitter: {
    card: "summary_large_image",
    site: "@twitterhandle",
    creator: "@twitterhandle",
    title: "Twitter title (under 70 chars)",
    description: "Twitter description (150-160 chars)",
    image: { url: "image-url", alt: "alt text" }
  },
  metaImage: { url: "image-url", alt: "alt text" },
  metaAttributes: []
}
```

### Phase 6: Publishing (sanity-publisher)
**MUST populate ALL schema fields:**
```
post = {
  title: "Post Title",
  slug: { _type: "slug", current: "post-slug" },
  markdownContent: "Full content...",
  excerpt: "Brief excerpt (max 200 chars)",
  author: { _type: "reference", _ref: "author-id" },
  categories: [{ _type: "reference", _ref: "category-id" }],
  tags: ["tag1", "tag2", "tag3"],
  coverImage: { _type: "image", asset: { _ref: "image-id" }, alt: "alt text" },
  publishedAt: "ISO timestamp",
  date: "ISO timestamp",
  seo: { /* all SEO fields from Phase 4 */ }
}
```

**Validation Checklist:**
- [ ] All required fields populated
- [ ] References are valid (author, categories)
- [ ] SEO fields are properly structured (not in content)
- [ ] Character limits respected
- [ ] Images have alt text
- [ ] Timestamps are valid ISO format

## Success Criteria

### First Attempt Success Rate: 100%
- No manual field population required
- No character limit violations
- All schema fields properly populated
- Content and SEO metadata properly separated
- Valid references and assets

## Summary of Critical Issues

1. **SEO fields mixed with content** instead of proper schema fields
2. **Character limits exceeded** (meta description: 185/160, OG description: 131/120)
3. **Missing schema fields** (categories, canonical URL, OG URL, site name, etc.)
4. **No schema validation** before publishing
5. **References not properly handled** (author, categories)

These improvements will ensure the workflow succeeds on the first attempt without requiring user intervention or manual fixes.
