#!/usr/bin/env bun
/**
 * Blog Agent Stop Hook
 *
 * Triggered when a blog subagent completes (SubagentStop event).
 * Provides voice notifications and captures session to history.
 *
 * Features:
 * - Detects blog agent type from [AGENT:type] tag in transcript
 * - Routes to agent-specific voice
 * - Captures completion to history
 * - Updates observability dashboard
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';

// Voice IDs for different blog agents (ElevenLabs)
const AGENT_VOICES: Record<string, string> = {
  'researcher': 'AXdMgz6evoL7OPd7eU12',
  'claude-researcher': 'AXdMgz6evoL7OPd7eU12',
  'perplexity-researcher': 'AXdMgz6evoL7OPd7eU12',
  'gemini-researcher': '2zRM7PkgwBPiau2jvVXc',
  'synthesizer': 'd3MFdIuCfbAIwiu7jC4a',
  'writer-tech': 'gfRt6Z3Z8aTbpLfexQ7N',
  'writer-personal': 'gfRt6Z3Z8aTbpLfexQ7N',
  'seo': 'fATgBRI8wg5KkDFg8vBd',
  'style': 'ZF6FPAbjXT4488VcRRnw',
  'publisher': 'iLVmqjzCGGvqtMCk6vVQ',
  'promoter': 'muZKMsIDGYtIkjjiUS82',
};

// Friendly names for agents
const AGENT_NAMES: Record<string, string> = {
  'researcher': 'Researcher',
  'claude-researcher': 'Claude Researcher',
  'perplexity-researcher': 'Perplexity Researcher',
  'gemini-researcher': 'Gemini Researcher',
  'synthesizer': 'Insight Synthesizer',
  'writer-tech': 'Tech Writer',
  'writer-personal': 'Personal Dev Writer',
  'seo': 'SEO Optimizer',
  'style': 'Style Guardian',
  'publisher': 'Publisher',
  'promoter': 'Social Promoter',
};

interface HookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
  cwd?: string;
}

interface CompletedInfo {
  agentType: string;
  message: string;
  timestamp: string;
}

// Extract [AGENT:type] and COMPLETED message from transcript
function extractAgentInfo(transcript: string): CompletedInfo | null {
  // Look for [AGENT:type] pattern
  const agentMatch = transcript.match(/\[AGENT:([^\]]+)\]/);
  if (!agentMatch) return null;

  const agentType = agentMatch[1];

  // Look for COMPLETED: message
  const completedMatch = transcript.match(/COMPLETED:\s*\[AGENT:[^\]]+\]\s*(.+?)(?:\n|$)/);
  const message = completedMatch ? completedMatch[1].trim() : `${AGENT_NAMES[agentType] || agentType} completed`;

  return {
    agentType,
    message,
    timestamp: new Date().toISOString(),
  };
}

// Send voice notification
async function sendVoiceNotification(agentType: string, message: string): Promise<void> {
  const voiceId = AGENT_VOICES[agentType] || AGENT_VOICES['researcher'];
  const agentName = AGENT_NAMES[agentType] || agentType;

  const payload = {
    title: `Blog Writing - ${agentName}`,
    message: message,
    voice_enabled: true,
    voice_id: voiceId,
  };

  try {
    await fetch('http://localhost:8888/notify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    // Voice server may not be running - silent fail
  }
}

// Send to observability dashboard
async function sendToObservability(agentType: string, message: string, sessionId: string): Promise<void> {
  const event = {
    type: 'blog_agent_complete',
    agent: agentType,
    message: message,
    session_id: sessionId,
    timestamp: new Date().toISOString(),
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

// Capture to history
function captureToHistory(info: CompletedInfo, sessionId: string): void {
  const now = new Date();
  const month = now.toISOString().slice(0, 7); // YYYY-MM
  const historyDir = join(process.env.PAI_DIR || 'C:/Users/Admin/.claude', 'history', 'blog-sessions', month);

  // Ensure directory exists
  if (!existsSync(historyDir)) {
    mkdirSync(historyDir, { recursive: true });
  }

  const logFile = join(historyDir, 'agent-completions.jsonl');
  const entry = {
    ...info,
    sessionId,
    capturedAt: now.toISOString(),
  };

  try {
    const line = JSON.stringify(entry) + '\n';
    writeFileSync(logFile, line, { flag: 'a' });
  } catch (error) {
    console.error('Failed to capture to history:', error);
  }
}

// Main hook handler
async function main() {
  try {
    // Read hook input from stdin
    const input = await Bun.stdin.text();
    const data: HookInput = JSON.parse(input);

    // Only process SubagentStop events
    if (data.hook_event_name !== 'SubagentStop') {
      process.exit(0);
    }

    // Read transcript
    if (!data.transcript_path || !existsSync(data.transcript_path)) {
      process.exit(0);
    }

    const transcript = readFileSync(data.transcript_path, 'utf-8');

    // Extract agent info
    const info = extractAgentInfo(transcript);
    if (!info) {
      // Not a blog agent - ignore
      process.exit(0);
    }

    // Check if this is a blog-related agent
    const blogAgents = Object.keys(AGENT_VOICES);
    if (!blogAgents.includes(info.agentType)) {
      process.exit(0);
    }

    // Send voice notification
    await sendVoiceNotification(info.agentType, info.message);

    // Send to observability
    await sendToObservability(info.agentType, info.message, data.session_id);

    // Capture to history
    captureToHistory(info, data.session_id);

  } catch (error) {
    console.error('Blog agent stop hook error:', error);
  }

  process.exit(0);
}

main();
