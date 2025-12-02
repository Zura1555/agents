# Troubleshooting Guide

Solutions to common issues and how to get help.

## 🆘 Quick Help

**Before diving in:**
1. Check the error in `state.json` → `cat blog-workspace/active-projects/PROJECT_ID/state.json`
2. Verify configuration files are valid JSON → `python -m json.tool config/file.json`
3. Ensure all dependencies are installed
4. Check file permissions in workspace directory

## ❌ Common Errors

### 1. "State file not found"

**Symptoms:**
- Error message about missing state.json
- Can't track project progress

**Causes:**
- Project directory moved or deleted
- Incorrect project ID
- File system error

**Solutions:**
```bash
# Check if project exists
ls blog-workspace/active-projects/

# Check archive if moved there
ls blog-workspace/archive/

# List all projects with timestamps
find blog-workspace -name "state.json" -type f

# Find specific project
find blog-workspace -name "state.json" -exec grep -l "your-topic" {} \;
```

**Prevention:**
- Don't manually move project directories
- Use the orchestrator script to manage projects
- Archive completed projects after publishing

---

### 2. "Invalid JSON in configuration file"

**Symptoms:**
- JSONDecodeError on startup
- Configuration not loading

**Causes:**
- Syntax errors in JSON (trailing commas, quotes)
- Invalid escape characters
- Malformed structure

**Solutions:**
```bash
# Validate JSON syntax
python -m json.tool config/brand-style.json
python -m json.tool config/sanity-config.json

# Fix common issues:
# 1. Remove trailing commas
# 2. Use double quotes, not single
# 3. Escape special characters properly

# Re-validate after fixes
python -m json.tool config/sanity-config.json
```

**Prevention:**
- Use a JSON validator before saving
- Copy-paste from example files
- Use an IDE with JSON validation

---

### 3. "Author reference not found" (Sanity)

**Symptoms:**
- Publishing fails at final step
- Error about missing author

**Causes:**
- Author doesn't exist in Sanity
- Wrong author name or ID
- Author reference not properly linked

**Solutions:**

**Check if author exists:**
1. Open Sanity Studio
2. Go to "Authors" collection
3. Search for "Thuong-Tuan Tran"

**Create author if missing:**
1. In Sanity Studio, click "Create new" in Authors
2. Fill in:
   - Name: "Thuong-Tuan Tran"
   - Bio: (optional)
   - Profile image: (optional)
3. Save the author
4. Note the `_id` generated

**Verify reference:**
```bash
# Check state file for author
cat blog-workspace/archive/PROJECT_ID/state.json | grep author
```

**Manual fix:**
1. Get the author's `_id` from Sanity Studio
2. Update the author reference in your post
3. Re-run publishing phase only

---

### 4. "Category doesn't exist" (Sanity)

**Symptoms:**
- Publishing fails
- Error about invalid category

**Causes:**
- Category not created in Sanity
- Category name mismatch
- Wrong category type

**Solutions:**

**Check existing categories:**
1. Sanity Studio → "Categories" collection
2. List all categories

**Create required categories:**
Create these exact category names:
- "Technology" (for tech posts)
- "Personal Development" (for personal-dev posts)

**Fix category mismatch:**
```bash
# Check state for categories
cat blog-workspace/archive/PROJECT_ID/state.json | grep categories

# Re-run publishing with correct categories
# Update config/brand-style.json if needed
```

**Prevention:**
- Create categories before first publish
- Use exact names (case-sensitive)
- Update config if adding new categories

---

### 5. "Invalid API token" (Sanity)

**Symptoms:**
- Authentication failed error
- 401 Unauthorized response

**Causes:**
- Token expired
- Token doesn't have write permissions
- Token incorrectly copied
- Wrong token for project/dataset

**Solutions:**

**Check token validity:**
1. Go to https://manage.sanity.io/
2. Select your project
3. Settings → API
4. Check token status

**Regenerate token:**
1. Settings → API
2. Delete old token
3. Create new token
4. Name: "Blog Writing System"
5. Permissions: Editor (write access)
6. Copy new token
7. Update `config/sanity-config.json`

**Verify permissions:**
- Token needs "Editor" role
- Must have write access
- Check token hasn't been revoked

**Check token format:**
- Should be a long string starting with "sk..."
- No extra spaces or characters
- Copied completely

---

### 6. "Slug already exists" (Sanity)

**Symptoms:**
- Publishing fails
- Duplicate slug error

**Causes:**
- Post with same title published before
- Similar slug generated

**Solutions:**

**Check existing posts:**
1. Sanity Studio → "Posts" collection
2. Search by slug or title

**Delete duplicate:**
- Delete old post if accidental
- Or keep and modify new one

**Generate unique slug:**
The system should auto-generate unique slugs by adding:
- Timestamp suffix
- Random string
- Incrementing number

**Manual override:**
1. Modify slug in state file
2. Re-run publishing phase

**Prevention:**
- Use unique titles
- System auto-generates unique slugs
- Check for duplicates before publishing

---

### 7. "Phase failed with error"

**Symptoms:**
- Workflow stops at specific phase
- Error logged in state.json

**Causes:**
- Input file corrupted or missing
- Agent execution error
- Invalid data format
- Resource limitations

**Solutions:**

**Check error details:**
```bash
# View error log
cat blog-workspace/active-projects/PROJECT_ID/state.json | grep -A 10 errors

# Check specific phase output
ls -la blog-workspace/active-projects/PROJECT_ID/
```

**Common fixes:**

**Research phase fails:**
- Verify topic is specific and valid
- Check internet connectivity
- Ensure research sources are accessible

**Synthesis phase fails:**
- Verify research-findings.json exists
- Check JSON is valid
- Ensure research is complete

**Writing phase fails:**
- Verify content-outline.md exists
- Check outline is valid markdown
- Ensure content type is supported

**SEO phase fails:**
- Verify draft file exists
- Check file is readable
- Ensure SEO requirements provided

**Review phase fails:**
- Verify seo-optimized draft exists
- Check SEO metadata is valid
- Ensure brand style config is valid

**Publishing phase fails:**
- Check Sanity credentials
- Verify schema compliance
- Ensure required fields present

**Retry failed phase:**
```bash
# The system auto-retries 3 times
# If still failing, check errors and fix input
# Then manually re-run phase:
python .claude/skills/blog-master-orchestrator/scripts/retry_phase.py \
  --project proj-2025-01-15-143022 \
  --phase writing
```

---

### 8. "Permission denied" on workspace

**Symptoms:**
- Can't create project directories
- Can't write output files

**Causes:**
- Insufficient file permissions
- Read-only file system
- Wrong workspace path

**Solutions:**

**Check permissions:**
```bash
# Check workspace directory permissions
ls -la /d/project/tuan/blog-workspace/

# Check if writable
touch /d/project/tuan/blog-workspace/test.txt && rm /d/project/tuan/blog-workspace/test.txt
```

**Fix permissions:**
```bash
# Make workspace writable
chmod -R 755 /d/project/tuan/blog-workspace/

# Make config writable (if editing)
chmod -R 644 /d/project/tuan/config/*.json
```

**Check disk space:**
```bash
# Check available space
df -h /d/project/tuan/

# Clean old projects if needed
find blog-workspace/archive -type d -mtime +30 -exec rm -rf {} \;
```

---

### 9. "Module not found" errors

**Symptoms:**
- ImportError for Python modules
- Script execution fails

**Causes:**
- Missing dependencies
- Python path issues
- Incorrect module imports

**Solutions:**

**Check Python version:**
```bash
python --version
# Should be 3.8 or higher
```

**Install dependencies:**
```bash
# Install required packages
pip install --upgrade pip
pip install -r requirements.txt  # if exists

# Or install basic requirements
pip install pathlib typing-extensions
```

**Check module path:**
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="/d/project/tuan:$PYTHONPATH"

# Or run from project root
cd /d/project/tuan
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py ...
```

---

### 10. "Output file is empty"

**Symptoms:**
- Phase completes but file is 0 bytes
- Next phase fails due to missing content

**Causes:**
- Agent produced no output
- File write failed silently
- Disk space issues

**Solutions:**

**Check file size:**
```bash
# List all files with sizes
ls -lh blog-workspace/active-projects/PROJECT_ID/

# Check specific file
wc -l blog-workspace/active-projects/PROJECT_ID/draft-tech.md
```

**Verify output:**
- Check if file exists
- Verify file has content
- Check for partial writes

**Re-run phase:**
- Delete empty output file
- Retry phase from orchestrator
- Or run agent manually

**Prevention:**
- Monitor phase outputs
- Check file sizes after each phase
- Validate outputs before proceeding

---

## 🔍 Debugging Techniques

### 1. Enable Verbose Logging

```python
# Add to orchestrator script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Inspect State File

```bash
# Pretty-print state
cat blog-workspace/active-projects/PROJECT_ID/state.json | python -m json.tool

# Check current phase
cat state.json | grep status

# View errors
cat state.json | grep -A 5 errors
```

### 3. Check All Artifacts

```bash
# List all files in project
find blog-workspace/active-projects/PROJECT_ID -type f -exec ls -lh {} \;

# Check file contents
head -20 blog-workspace/active-projects/PROJECT_ID/draft-tech.md
```

### 4. Validate JSON Files

```bash
# Validate all JSON files
find blog-workspace -name "*.json" -exec python -m json.tool {} \; > /dev/null

# Check specific file
python -m json.tool blog-workspace/active-projects/PROJECT_ID/research-findings.json
```

### 5. Test Individual Phases

```bash
# Run just one phase
python .claude/skills/blog-master-orchestrator/scripts/run_phase.py \
  --project PROJECT_ID \
  --phase research

# Skip to specific phase
python .claude/skills/blog-master-orchestrator/scripts/skip_to_phase.py \
  --project PROJECT_ID \
  --phase writing
```

---

## 🚨 When All Else Fails

### 1. Check Documentation

- **[Agent Documentation](../agents/)** - Detailed agent specs
- **[Workflow Guide](workflow.md)** - How the system works
- **[Configuration Guide](configuration.md)** - Setup issues

### 2. Review Error Logs

```bash
# View complete error log
cat blog-workspace/active-projects/PROJECT_ID/state.json | \
  python -m json.tool | grep -A 10 errors

# Check system logs
tail -50 /var/log/syslog | grep -i error
```

### 3. Validate Configuration

```bash
# Test configuration loading
python -c "
import json
with open('config/brand-style.json') as f:
    config = json.load(f)
print('Brand style valid')
with open('config/sanity-config.json') as f:
    config = json.load(f)
print('Sanity config valid')
"
```

### 4. Start Fresh

If issues persist:

```bash
# Archive problematic project
mv blog-workspace/active-projects/PROJECT_ID blog-workspace/failed-PROJECT_ID

# Start new project
python .claude/skills/blog-master-orchestrator/scripts/orchestrate_workflow.py \
  --topic "New Test Post" \
  --type tech \
  --mode markdown
```

### 5. Simplify and Test

```bash
# Test with simple topic
python orchestrate_workflow.py \
  --topic "Test" \
  --type tech \
  --mode markdown

# Use minimal settings
# Start with markdown mode (no API)
# Use short topic
```

---

## 📞 Getting Help

### Information to Gather

Before asking for help:

1. **Project ID:** `proj-YYYY-MM-DD-HHMMSS`
2. **Error phase:** Which phase failed?
3. **Error message:** Exact error text
4. **State file:** Output of `cat state.json | python -m json.tool`
5. **Configuration:** Confirmed JSON is valid
6. **Steps taken:** What you tried already

### Example Help Request

```
Project ID: proj-2025-01-15-143022
Failed Phase: writing
Error: "KeyError: 'content-type'"

State file output:
{
  "status": "writing",
  "phases": {
    "writing": {"status": "error", "output": "draft-tech.md"}
  },
  "metadata": {
    "errors": [
      {"timestamp": "...", "phase": "writing", "error": "KeyError: 'content-type'"}
    ]
  }
}

Tried:
- Restarted the script
- Checked JSON validity
- Verified configuration

How to proceed?
```

### Self-Help Resources

1. **README.md** - System overview
2. **docs/guides/** - Detailed guides
3. **docs/agents/** - Agent specifications
4. **config/** - Example configurations
5. **Agent SKILL.md files** - Detailed agent docs

### Prevention Tips

1. **Keep JSON files valid** - Always validate after editing
2. **Don't manually edit project files** - Use the orchestrator
3. **Check Sanity setup first** - Verify credentials and schema
4. **Test with markdown mode** - Before using API mode
5. **Monitor phase outputs** - Check files after each phase
6. **Archive old projects** - Keep workspace clean
7. **Use version control** - Track configuration changes

---

## 🛠️ Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Archive completed projects older than 1 week
- Check for failed projects and clean up
- Validate all configuration files

**Monthly:**
- Update Sanity API tokens (optional, for security)
- Review and adjust quality thresholds
- Clean old workspace directories

**As Needed:**
- Update brand voice settings
- Add new categories
- Create new content types

### Performance Optimization

**Speed up workflow:**
- Use SSD storage for workspace
- Keep adequate free disk space
- Monitor system resources

**Quality improvement:**
- Adjust quality score thresholds
- Refine brand voice characteristics
- Update SEO requirements

---

**Remember:** Most issues are configuration-related. Double-check your setup before diving into complex debugging! 🔧
