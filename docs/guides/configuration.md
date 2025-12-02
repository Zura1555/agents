# Configuration Guide

Learn how to configure your blog writing system for optimal performance.

## 📋 Configuration Files Overview

The system uses several configuration files:

```
/d/project/tuan/config/
├── brand-style.json           # Brand voice and style guidelines
└── sanity-config.json.example # Sanity CMS integration template
```

## 🎨 Brand Style Configuration

**File:** `config/brand-style.json`

This file defines your brand voice, writing standards, and quality benchmarks.

### Key Sections

#### 1. Brand Information
```json
{
  "brand": {
    "name": "Thuong-Tuan Tran",
    "author": "Thuong-Tuan Tran",
    "voice": "Professional & Friendly",
    "tagline": "Sharing insights on technology and personal growth"
  }
}
```

**Customize:**
- Update author name
- Adjust tagline
- Modify brand voice description

#### 2. Writing Style
```json
{
  "writingStyle": {
    "tone": {
      "professional": {
        "enabled": true,
        "characteristics": [
          "Knowledgeable and credible",
          "Demonstrates expertise",
          "Uses accurate terminology",
          "Provides evidence-based content"
        ]
      },
      "friendly": {
        "enabled": true,
        "characteristics": [
          "Approachable and warm",
          "Conversational but not casual",
          "Inclusive language",
          "Respectful of reader's time"
        ]
      }
    }
  }
}
```

**Customize:**
- Adjust tone characteristics
- Enable/disable professional/friendly elements
- Add custom voice traits

#### 3. Language Preferences
```json
{
  "language": {
    "voice": "second-person",        // "first-person", "second-person", "third-person"
    "perspective": "first-person-plural", // "we", "you", "I"
    "contractions": "use-sparingly", // "always", "use-sparingly", "never"
    "jargon": "define-or-avoid",     // "define-or-avoid", "allow", "avoid"
    "acronyms": "expand-on-first-use" // "expand-on-first-use", "allow", "avoid"
  }
}
```

**Customize:**
- Change narrative voice
- Adjust pronoun usage
- Set jargon policy
- Define acronym handling

#### 4. Content Structure
```json
{
  "structure": {
    "paragraphLength": "3-4 sentences",
    "sentenceLength": "15-20 words average",
    "introductionLength": "150-250 words",
    "conclusionLength": "150-250 words"
  }
}
```

**Customize:**
- Adjust paragraph length
- Set sentence length targets
- Define intro/conclusion length

#### 5. Content Type Guidelines

**Technology Content:**
```json
{
  "technology": {
    "approach": "explanatory and practical",
    "technicalDepth": "intermediate",
    "examples": "abundant and practical",
    "codeFormat": "well-commented and explained"
  }
}
```

**Personal Development Content:**
```json
{
  "personalDevelopment": {
    "approach": "story-driven and inspirational",
    "tone": "encouraging and empathetic",
    "stories": "authentic and relatable",
    "advice": "specific and actionable"
  }
}
```

#### 6. Quality Standards
```json
{
  "qualityStandards": {
    "minimumWordCount": {
      "tech": 1000,
      "personal-dev": 1200
    },
    "maximumWordCount": {
      "tech": 1500,
      "personal-dev": 2000
    },
    "qualityScores": {
      "seo": {
        "minimum": 70,
        "target": 85
      },
      "style": {
        "minimum": 80,
        "target": 90
      }
    }
  }
}
```

**Customize:**
- Adjust word count targets
- Set quality score thresholds
- Modify minimum/maximums

#### 7. Publishing Defaults
```json
{
  "publishing": {
    "authorName": "Thuong-Tuan Tran",
    "defaultCategories": [
      "Technology",
      "Personal Development"
    ],
    "defaultTags": [
      "blog",
      "insights",
      "growth"
    ]
  }
}
```

**Customize:**
- Change author name
- Set default categories
- Add/modify default tags

## 🔌 Sanity CMS Configuration

**File:** `config/sanity-config.json` (create from example)

### Step 1: Copy Example File

```bash
cd /d/project/tuan/config
cp sanity-config.json.example sanity-config.json
```

### Step 2: Get Sanity Credentials

1. **Go to Sanity Manage:** https://manage.sanity.io/

2. **Select your project** (or create a new one)

3. **Get Project ID:**
   - Go to Settings → General
   - Copy Project ID

4. **Get Dataset:**
   - Usually "production" (default)
   - Or your custom dataset name

5. **Create API Token:**
   - Go to Settings → API
   - Click "Create Token"
   - Name it "Blog Writing System"
   - Select "Editor" permissions (write access)
   - Copy the token

### Step 3: Configure the File

Edit `config/sanity-config.json`:

```json
{
  "project": {
    "id": "your-actual-project-id-here",
    "name": "Your Project Name",
    "dataset": "production"
  },
  "api": {
    "version": "2024-12-02",
    "token": "your-actual-api-token-here"
  }
}
```

⚠️ **Important Security Notes:**
- Never commit `sanity-config.json` to version control
- Add it to `.gitignore` if using git
- Use environment variables for production
- Regenerate tokens if compromised

### Step 4: Configure Publishing Mode

Choose your default publishing mode:

```json
{
  "publishing": {
    "defaultMode": "api",  // or "markdown" or "ask-user"
    "fallbackMode": "markdown"
  }
}
```

**Publishing Mode Options:**

- `"markdown"` - Output files for manual copy-paste
- `"api"` - Direct automated publishing
- `"ask-user"` - Ask which mode each time

### Step 5: Validate Configuration

Test your configuration:

```bash
# Check JSON syntax
python -m json.tool config/sanity-config.json

# Validate schema (if you have validation script)
python scripts/validate_config.py
```

## 📁 Sanity Schema Requirements

### Required Fields

Make sure your Sanity schema has these fields:

```javascript
// In your Sanity Studio schema

export default {
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: Rule => Rule.required().min(5).max(100)
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96
      },
      validation: Rule => Rule.required()
    },
    {
      name: 'content',
      title: 'Content',
      type: 'array',
      of: [
        {
          type: 'block'
        },
        {
          type: 'code'
        }
      ],
      validation: Rule => Rule.required()
    },
    {
      name: 'excerpt',
      title: 'Excerpt',
      type: 'text',
      rows: 3,
      validation: Rule => Rule.required().max(200)
    },
    {
      name: 'author',
      title: 'Author',
      type: 'reference',
      to: [{ type: 'author' }],
      validation: Rule => Rule.required()
    },
    {
      name: 'categories',
      title: 'Categories',
      type: 'array',
      of: [{ type: 'reference', to: [{ type: 'category' }] }],
      validation: Rule => Rule.required().min(1).max(5)
    },
    {
      name: 'publishedAt',
      title: 'Published At',
      type: 'datetime',
      validation: Rule => Rule.required()
    }
  ]
}
```

### Creating Required References

**1. Author Reference:**

In Sanity Studio:
1. Go to "Authors" collection
2. Create new author
3. Name: "Thuong-Tuan Tran"
4. Save and note the `_id`

**2. Categories:**

Create these categories:
- "Technology"
- "Personal Development"

In Sanity Studio:
1. Go to "Categories" collection
2. Create new category
3. Name: "Technology"
4. Save
5. Repeat for "Personal Development"

## 🔧 Advanced Configuration

### Custom Content Types

Add new content types:

1. **Update brand-style.json:**
```json
{
  "contentGuidelines": {
    "business": {
      "approach": "data-driven and strategic",
      "tone": "authoritative and informative",
      "examples": "case studies and research"
    }
  }
}
```

2. **Update publishing categories:**
```json
{
  "publishing": {
    "defaultCategories": [
      "Technology",
      "Personal Development",
      "Business"
    ]
  }
}
```

3. **Create new writer agent** (see Customization Guide)

### Custom Quality Thresholds

Adjust quality scores:

```json
{
  "qualityStandards": {
    "qualityScores": {
      "seo": {
        "minimum": 60,    // Lower threshold
        "target": 90      // Higher target
      },
      "style": {
        "minimum": 75,
        "target": 95
      }
    }
  }
}
```

### Custom Tags

Set topic-specific tags:

```json
{
  "publishing": {
    "defaultTags": [
      "blog",
      "insights",
      "growth",
      "productivity",
      "technology"
    ]
  }
}
```

### Environment Variables (Production)

For production deployment, use environment variables:

```bash
# .env file
export SANITY_PROJECT_ID="your-project-id"
export SANITY_DATASET="production"
export SANITY_API_TOKEN="your-token"
```

Then in config:

```json
{
  "project": {
    "id": "${SANITY_PROJECT_ID}",
    "dataset": "${SANITY_DATASET}"
  },
  "api": {
    "token": "${SANITY_API_TOKEN}"
  }
}
```

## ✅ Configuration Checklist

### Brand Style
- [ ] Author name updated
- [ ] Brand voice defined
- [ ] Tone characteristics set
- [ ] Word count targets configured
- [ ] Quality thresholds set
- [ ] Categories defined

### Sanity CMS
- [ ] Project ID added
- [ ] Dataset specified
- [ ] API token configured
- [ ] Author reference created
- [ ] Categories created
- [ ] Schema validated
- [ ] Test publish successful

### Security
- [ ] Config file not in git
- [ ] API token secure
- [ ] Permissions limited
- [ ] Token has write access only

## 🧪 Testing Configuration

### Test Markdown Mode

```bash
# Run without API credentials
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "Testing Configuration" \
  --type tech \
  --mode markdown
```

### Test API Mode

```bash
# Test with API publishing
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "API Publishing Test" \
  --type personal-dev \
  --mode api
```

### Check State File

```bash
# View configuration in state
cat blog-workspace/archive/PROJECT_ID/state.json | grep -A 5 "brandVoice"
```

## 🚨 Troubleshooting Configuration

### Invalid JSON Syntax
**Error:** `JSONDecodeError`
**Solution:** Validate with `python -m json.tool config/file.json`

### Missing Author Reference
**Error:** "Author not found"
**Solution:** Create author in Sanity Studio first

### Invalid Category
**Error:** "Category doesn't exist"
**Solution:** Create category in Sanity or update config

### API Token Invalid
**Error:** "Authentication failed"
**Solution:** Check token hasn't expired and has write permissions

### Schema Mismatch
**Error:** "Field validation failed"
**Solution:** Update Sanity schema to match requirements

## 📚 Next Steps

Now that configuration is complete:

1. **[Run a Test Post](quick-start.md)** - Verify everything works
2. **[Understand the Workflow](workflow.md)** - Learn how it all works
3. **[Customize Further](customization.md)** - Adapt to your needs
4. **[Check Agent Docs](../agents/)** - Understand each agent

**Configuration complete!** You're ready to create blog posts! 🎉
