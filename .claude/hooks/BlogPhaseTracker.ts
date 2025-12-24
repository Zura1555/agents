#!/usr/bin/env bun
/**
 * Blog Phase Tracker Hook
 *
 * Triggered on PostToolUse events to track blog workflow phase transitions.
 * Monitors Task tool invocations for blog agents and updates state.
 *
 * Features:
 * - Tracks phase transitions in blog workflow
 * - Updates state.json in active project directory
 * - Sends events to observability dashboard
 * - Logs phase metrics for analytics
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { join } from 'path';

interface HookInput {
  session_id: string;
  tool_name: string;
  tool_input?: {
    subagent_type?: string;
    prompt?: string;
    description?: string;
  };
  tool_output?: string;
  hook_event_name: string;
  cwd?: string;
}

interface PhaseInfo {
  phase: string;
  agentType: string;
  startTime?: string;
  endTime?: string;
  status: 'started' | 'completed' | 'failed';
}

// Map agent types to workflow phases
const AGENT_TO_PHASE: Record<string, string> = {
  'researcher': 'research',
  'claude-researcher': 'research',
  'perplexity-researcher': 'research',
  'gemini-researcher': 'research',
  'synthesizer': 'synthesis',
  'writer-tech': 'writing',
  'writer-personal': 'writing',
  'writer': 'writing',
  'seo': 'seo',
  'style': 'review',
  'publisher': 'publishing',
  'promoter': 'social',
};

// Detect blog agent from Task tool input
function detectBlogAgent(input: HookInput['tool_input']): string | null {
  if (!input) return null;

  // Check subagent_type
  if (input.subagent_type && Object.keys(AGENT_TO_PHASE).includes(input.subagent_type)) {
    return input.subagent_type;
  }

  // Check prompt for [AGENT:type] pattern
  if (input.prompt) {
    const match = input.prompt.match(/\[AGENT:([^\]]+)\]/);
    if (match && Object.keys(AGENT_TO_PHASE).includes(match[1])) {
      return match[1];
    }

    // Check for "You are blog-*" pattern
    const blogMatch = input.prompt.match(/You are (blog-[a-z-]+)/);
    if (blogMatch) {
      const agentName = blogMatch[1].replace('blog-', '').replace('-researcher', 'researcher');
      if (Object.keys(AGENT_TO_PHASE).includes(agentName)) {
        return agentName;
      }
    }
  }

  return null;
}

// Find active blog project directory
function findActiveProject(cwd?: string): string | null {
  const baseDir = cwd || process.cwd();
  const workspaceDir = join(baseDir, 'blog-workspace', 'active-projects');

  if (!existsSync(workspaceDir)) {
    return null;
  }

  // Find most recent project
  try {
    const projects = readdirSync(workspaceDir)
      .filter(d => d.startsWith('proj-'))
      .sort()
      .reverse();

    if (projects.length > 0) {
      return join(workspaceDir, projects[0]);
    }
  } catch (error) {
    return null;
  }

  return null;
}

// Update state.json with phase info
function updateState(projectDir: string, phaseInfo: PhaseInfo): void {
  const statePath = join(projectDir, 'state.json');

  if (!existsSync(statePath)) {
    return;
  }

  try {
    const state = JSON.parse(readFileSync(statePath, 'utf-8'));
    const phaseName = AGENT_TO_PHASE[phaseInfo.agentType] || phaseInfo.phase;

    if (!state.phases) {
      state.phases = {};
    }

    if (!state.phases[phaseName]) {
      state.phases[phaseName] = {};
    }

    if (phaseInfo.status === 'started') {
      state.phases[phaseName].status = 'in_progress';
      state.phases[phaseName].startedAt = phaseInfo.startTime;
      state.phases[phaseName].agent = phaseInfo.agentType;
      state.status = phaseName;
    } else if (phaseInfo.status === 'completed') {
      state.phases[phaseName].status = 'complete';
      state.phases[phaseName].completedAt = phaseInfo.endTime;
    } else if (phaseInfo.status === 'failed') {
      state.phases[phaseName].status = 'error';
      state.phases[phaseName].failedAt = phaseInfo.endTime;
    }

    writeFileSync(statePath, JSON.stringify(state, null, 2));
  } catch (error) {
    console.error('Failed to update state:', error);
  }
}

// Send to observability dashboard
async function sendToObservability(phaseInfo: PhaseInfo, sessionId: string): Promise<void> {
  const event = {
    type: 'blog_phase_transition',
    phase: AGENT_TO_PHASE[phaseInfo.agentType] || phaseInfo.phase,
    agent: phaseInfo.agentType,
    status: phaseInfo.status,
    session_id: sessionId,
    timestamp: phaseInfo.status === 'started' ? phaseInfo.startTime : phaseInfo.endTime,
  };

  try {
    await fetch('http://localhost:4000/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
    });
  } catch (error) {
    // Observability server may not be running - silent fail
  }
}

// Log phase metrics for analytics
function logPhaseMetrics(phaseInfo: PhaseInfo, sessionId: string): void {
  const now = new Date();
  const month = now.toISOString().slice(0, 7);
  const metricsDir = join(process.env.PAI_DIR || 'C:/Users/Admin/.claude', 'history', 'blog-metrics', month);

  // We don't create the directory here to avoid side effects
  // The directory should be created by the analytics system
  try {
    const metricsFile = join(metricsDir, 'phase-transitions.jsonl');
    if (existsSync(metricsDir)) {
      const entry = {
        ...phaseInfo,
        sessionId,
        loggedAt: now.toISOString(),
      };
      writeFileSync(metricsFile, JSON.stringify(entry) + '\n', { flag: 'a' });
    }
  } catch (error) {
    // Silent fail - metrics are optional
  }
}

// Main hook handler
async function main() {
  try {
    // Read hook input from stdin
    const input = await Bun.stdin.text();
    const data: HookInput = JSON.parse(input);

    // Only process PostToolUse events for Task tool
    if (data.hook_event_name !== 'PostToolUse' || data.tool_name !== 'Task') {
      process.exit(0);
    }

    // Detect if this is a blog agent
    const agentType = detectBlogAgent(data.tool_input);
    if (!agentType) {
      process.exit(0);
    }

    const now = new Date().toISOString();
    const phase = AGENT_TO_PHASE[agentType] || 'unknown';

    // Determine if this is a start or completion
    // PostToolUse means the tool has completed
    const phaseInfo: PhaseInfo = {
      phase,
      agentType,
      endTime: now,
      status: 'completed', // PostToolUse indicates completion
    };

    // Check if output indicates failure
    if (data.tool_output && data.tool_output.toLowerCase().includes('error')) {
      phaseInfo.status = 'failed';
    }

    // Find and update active project state
    const projectDir = findActiveProject(data.cwd);
    if (projectDir) {
      updateState(projectDir, phaseInfo);
    }

    // Send to observability
    await sendToObservability(phaseInfo, data.session_id);

    // Log metrics
    logPhaseMetrics(phaseInfo, data.session_id);

  } catch (error) {
    console.error('Blog phase tracker hook error:', error);
  }

  process.exit(0);
}

main();
