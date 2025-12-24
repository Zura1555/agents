# SEO Field Requirements for Skills/Agents

## Character Length Requirements

### Meta Title
- **Recommended Range**: 50-60 characters
- **Minimum**: 50 characters
- **Maximum**: 60 characters
- **Current**: 54 characters ✓

### Meta Description
- **Recommended Range**: 150-160 characters
- **Minimum**: 150 characters
- **Maximum**: 160 characters
- **Current**: 158 characters ✓

### Open Graph Description
- **Recommended Range**: 100-120 characters
- **Maximum**: 120 characters
- **Current**: 115 characters ✓

### Twitter Description
- **Recommended Range**: 150-160 characters
- **Maximum**: 160 characters

## Validation Rules for Skills

### seo-content-optimizer
1. **Validate character counts** before output
2. **Auto-adjust** if outside recommended ranges
3. **Prioritize** keyword inclusion while maintaining length
4. **Log warnings** if adjustments needed

### sanity-publisher
1. **Check** all character limits before publishing
2. **Fail fast** if limits exceeded
3. **Auto-truncate** with ellipsis if necessary
4. **Report** actual vs recommended counts

## Implementation Notes

- Always count characters accurately (including spaces and punctuation)
- Test with actual character count, not byte count
- Ensure readability is maintained after length adjustments
- Prioritize important keywords in available space

## Current Blog Post Status

**Document**: b4343531-a15c-4adb-828c-8d94ef0a60de
- ✅ Meta Title: 54 chars (within 50-60)
- ✅ Meta Description: 158 chars (within 150-160)
- ✅ All SEO fields populated
