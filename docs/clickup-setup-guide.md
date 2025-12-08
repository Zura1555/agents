# ClickUp MCP Server Setup Guide

## Overview

This guide explains how to set up the ClickUp MCP server for the workflow management system.

## Prerequisites

1. **Node.js v18.0.0 or higher**
   ```bash
   node --version
   # Should output v18.x.x or higher
   ```

2. **ClickUp API Access**
   - Valid ClickUp account
   - API key with appropriate permissions
   - Team ID for your workspace

## Step 1: Obtain ClickUp Credentials

### Get API Key

1. Log in to your ClickUp account
2. Go to **Settings** → **Apps** (or **Integrations**)
3. Click **Generate API Token** or **Create Token**
4. Copy the token (save it securely - you won't see it again)

### Get Team ID

**Option 1: From URL**
1. Open your ClickUp workspace in browser
2. Look at the URL: `https://app.clickup.com/{TEAM_ID}/...`
3. The `TEAM_ID` is the first part after `app.clickup.com/`

**Option 2: From API**
```bash
curl -H "Authorization: pk_..." https://api.clickup.com/api/v2/team
```

## Step 2: Configure MCP Server

### Copy Configuration Template

```bash
cp config/clickup-mcp-config.json ~/.claude/mcp-config.json
```

### Edit Configuration

Open `~/.claude/mcp-config.json` and add your credentials:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "npx",
      "args": ["-y", "@taazkareem/clickup-mcp-server@latest"],
      "env": {
        "CLICKUP_API_KEY": "pk_...",  // Your API key here
        "CLICKUP_TEAM_ID": "12345678",  // Your Team ID here
        "ENABLED_TOOLS": "get_workspace_hierarchy,get_tasks,get_task,create_task,update_task,create_task_comment,get_task_comments,get_task_time_entries,get_workspace_members,find_member_by_name,create_list,get_list,start_time_tracking,stop_time_tracking,add_time_entry",
        "DOCUMENT_SUPPORT": "true"
      }
    }
  }
}
```

### Alternative: Environment Variables

You can also set credentials via environment variables:

```bash
export CLICKUP_API_KEY="pk_..."
export CLICKUP_TEAM_ID="12345678"
```

## Step 3: Test MCP Server

### List Available Tools

```bash
# This will show all 36 ClickUp tools
mcp__list_mcp_resources --server clickup
```

### Run a Test Query

```bash
# Get workspace hierarchy
mcp__clickup__get_workspace_hierarchy

# Get team members
mcp__clickup__get_workspace_members

# Get tasks from a list
mcp__clickup__get_tasks --list_id "your-list-id"
```

## Step 4: Verify Integration

### Test Task Operations

```bash
# Create a test task
mcp__clickup__create_task \
  --list_id "test-list" \
  --name "Test Task from MCP" \
  --description "Testing MCP integration"

# Retrieve the task
mcp__clickup__get_task --task_id "returned-task-id"

# Add a comment
mcp__clickup__create_task_comment \
  --task_id "task-id" \
  --comment_text "Test comment from MCP"

# Clean up - delete test task
mcp__clickup__delete_task --task_id "task-id"
```

## Step 5: Configure Workflow Management System

### Update Project Configuration

Edit `config/clickup-config.json`:

```json
{
  "api_token": "env:CLICKUP_API_KEY",
  "team_id": "env:CLICKUP_TEAM_ID",
  "mcp_server": "clickup",
  "enabled_tools": [
    "get_workspace_hierarchy",
    "get_tasks",
    "create_task",
    "update_task",
    "get_task_comments",
    "create_task_comment",
    "get_task_time_entries",
    "get_workspace_members"
  ]
}
```

## Step 6: Integration with Orchestrator

The orchestrator will automatically detect and use the MCP server for ClickUp operations.

### Verify Orchestrator Detection

The orchestrator checks for:
1. MCP server "clickup" available
2. Required tools enabled
3. Valid API credentials

To test:

```bash
python .claude/skills/project-master-orchestrator/scripts/orchestrate_workflow.py \
  --action monitor \
  --platforms clickup \
  --project test-project
```

## Troubleshooting

### Issue: "MCP server not found"

**Solution:**
1. Verify Node.js is installed: `node --version`
2. Install npx: `npm install -g npx`
3. Test MCP server manually:
   ```bash
   npx -y @taazkareem/clickup-mcp-server@latest
   ```

### Issue: "Authentication failed"

**Solution:**
1. Verify API key is correct (no extra spaces)
2. Verify Team ID is correct
3. Check API key permissions in ClickUp
4. Regenerate API key if needed

### Issue: "Rate limit exceeded"

**Solution:**
1. This is handled automatically by the MCP server
2. Wait 1-2 minutes and retry
3. Reduce frequency of API calls if persistent

### Issue: "Tool not found" or "Tool not enabled"

**Solution:**
1. Verify ENABLED_TOOLS includes the required tool
2. Check spelling of tool name
3. Restart MCP server after configuration changes

### Issue: "Network error" or "Connection timeout"

**Solution:**
1. Check internet connection
2. Verify ClickUp API is accessible:
   ```bash
   curl -I https://api.clickup.com/api/v2/team
   ```
3. Check firewall/proxy settings

### Issue: "Permission denied"

**Solution:**
1. Verify API key has necessary permissions
2. Check your ClickUp role in the workspace
3. Some operations require Admin/Manager role

## Advanced Configuration

### Enable Additional Tools

To enable more tools, add them to `ENABLED_TOOLS`:

```json
{
  "env": {
    "ENABLED_TOOLS": "get_workspace_hierarchy,get_tasks,create_task,update_task,create_bulk_tasks,update_bulk_tasks,move_task,duplicate_task,get_space_tags,create_space_tag,start_time_tracking,stop_time_tracking"
  }
}
```

### Disable Specific Tools

```json
{
  "env": {
    "DISABLED_TOOLS": "delete_task,delete_list,delete_folder"
  }
}
```

### HTTP Server Mode

For HTTP transport (alternative to STDIO):

```json
{
  "env": {
    "ENABLE_SSE": "true",
    "PORT": "3231"
  }
}
```

Then access via: `http://localhost:3231/mcp`

### Document Support

Enable document management tools:

```json
{
  "env": {
    "DOCUMENT_SUPPORT": "true"
  }
}
```

## Security Best Practices

### Protect Credentials

1. **Never commit API keys to version control**
   - Add `*.json` with credentials to `.gitignore`
   - Use environment variables when possible

2. **Restrict API key permissions**
   - Only grant necessary permissions
   - Use separate keys for different environments

3. **Rotate API keys regularly**
   - Every 90 days minimum
   - Immediately if compromised

4. **Monitor API usage**
   - Check ClickUp for unusual activity
   - Set up alerts for high usage

### File Permissions

Secure configuration files:

```bash
chmod 600 ~/.claude/mcp-config.json
chmod 600 config/clickup-config.json
```

## Environment-Specific Setup

### Development Environment

```json
{
  "env": {
    "CLICKUP_API_KEY": "pk_dev_...",
    "CLICKUP_TEAM_ID": "dev-team-id",
    "CLICKUP_DEBUG": "true"
  }
}
```

### Production Environment

```json
{
  "env": {
    "CLICKUP_API_KEY": "pk_live_...",
    "CLICKUP_TEAM_ID": "prod-team-id",
    "CLICKUP_DEBUG": "false"
  }
}
```

## Monitoring MCP Server

### Check Server Status

```bash
# List MCP resources
mcp__list_mcp_resources --server clickup

# Get available tools
mcp__list_mcp_resources
```

### View Logs

MCP server logs are typically available via:
- STDIO: Logs in terminal output
- HTTP: Logs via endpoint (e.g., `http://localhost:3231/logs`)

### Performance Metrics

Monitor:
- API call frequency
- Rate limit usage
- Response times
- Error rates

## Backup and Recovery

### Backup Configuration

```bash
# Backup MCP config (without secrets)
cp ~/.claude/mcp-config.json ~/.claude/mcp-config.json.template
# Edit to remove CLICKUP_API_KEY and CLICKUP_TEAM_ID
```

### Restore Configuration

```bash
cp ~/.claude/mcp-config.json.template ~/.claude/mcp-config.json
# Edit to add back credentials
```

## Support Resources

### ClickUp MCP Server
- GitHub: https://github.com/taazkareem/clickup-mcp-server
- Issues: Submit issues on GitHub
- Documentation: Repository README

### ClickUp API
- Official Docs: https://clickup.com/api
- API Reference: https://clickup.com/api/reference
- Status Page: https://status.clickup.com/

### Workflow Management System
- Documentation: `/docs/`
- Configuration: `/config/`
- Examples: `/examples/`

## Next Steps

After setup:

1. ✅ Test all required tools
2. ✅ Verify with sample tasks
3. ✅ Configure monitoring alerts
4. ✅ Set up backup procedures
5. ✅ Document workspace-specific settings

## Quick Reference

**Required Tools:**
- `get_workspace_hierarchy` - Get workspace structure
- `get_tasks` - List tasks
- `create_task` - Create new tasks
- `update_task` - Update tasks
- `get_task_comments` - View comments
- `create_task_comment` - Add comments
- `get_task_time_entries` - Time tracking
- `get_workspace_members` - Team members

**Useful Commands:**
```bash
# Test connection
mcp__clickup__get_workspace_hierarchy

# Get team info
mcp__clickup__get_workspace_members

# Test task operations
mcp__clickup__create_task --list_id "..." --name "Test"

# View available tools
mcp__list_mcp_resources --server clickup
```

---

**Author:** Thuong-Tuan Tran
**Version:** 1.0.0
**Last Updated:** 2025-12-02
