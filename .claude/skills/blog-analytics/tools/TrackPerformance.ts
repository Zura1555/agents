#!/usr/bin/env bun
/**
 * Track Performance CLI
 *
 * Track and log blog post performance metrics.
 *
 * Usage:
 *   track-performance log <post-id> [options]    Log metrics for a post
 *   track-performance import <json-file>         Import metrics from JSON
 *   track-performance list [options]             List tracked posts
 *   track-performance help                       Show this help message
 *
 * Options for 'log':
 *   --views <number>          Total views
 *   --day1-views <number>     Day 1 views
 *   --day7-views <number>     Day 7 views
 *   --day30-views <number>    Day 30 views
 *   --engagement <number>     Engagement score (0-100)
 *   --comments <number>       Number of comments
 *   --shares <number>         Number of shares
 *   --title <string>          Post title
 *   --content-type <string>   Content type (tech|personal-dev)
 *
 * Examples:
 *   bun run TrackPerformance.ts log post-123 --views 1500 --engagement 85
 *   bun run TrackPerformance.ts list --month 2025-01
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE_DIR = process.env.BLOG_WORKSPACE || 'D:/project/agents/blog-workspace';
const ANALYTICS_DIR = join(WORKSPACE_DIR, 'analytics');

interface PostMetrics {
  postId: string;
  title?: string;
  publishedAt?: string;
  contentType?: string;
  contentAttributes?: {
    topic?: string;
    wordCount?: number;
    readingTime?: number;
    seoScore?: number;
    styleScore?: number;
  };
  metrics: {
    views: {
      day1?: number;
      day7?: number;
      day30?: number;
      total?: number;
    };
    engagement: {
      avgTimeOnPage?: number;
      scrollDepth?: number;
      bounceRate?: number;
      comments?: number;
      shares?: number;
      likes?: number;
    };
    seo?: {
      organicTraffic?: number;
      clickThroughRate?: number;
      impressions?: number;
    };
    social?: {
      linkedinViews?: number;
      linkedinEngagement?: number;
      twitterImpressions?: number;
      twitterEngagement?: number;
    };
  };
  trackedAt: string;
  dataSource: string;
}

// Ensure analytics directory exists
function ensureAnalyticsDir(month?: string): string {
  const targetMonth = month || new Date().toISOString().slice(0, 7);
  const monthDir = join(ANALYTICS_DIR, targetMonth);

  if (!existsSync(monthDir)) {
    mkdirSync(monthDir, { recursive: true });
  }

  return monthDir;
}

// Parse command line arguments
function parseArgs(args: string[]): Record<string, string | number | boolean> {
  const result: Record<string, string | number | boolean> = {};
  let i = 0;

  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-/g, '_');
      const nextArg = args[i + 1];

      if (nextArg && !nextArg.startsWith('--')) {
        // Check if it's a number
        const num = Number(nextArg);
        result[key] = isNaN(num) ? nextArg : num;
        i += 2;
      } else {
        result[key] = true;
        i += 1;
      }
    } else {
      i += 1;
    }
  }

  return result;
}

// Log metrics for a post
function logMetrics(postId: string, options: Record<string, string | number | boolean>): void {
  const monthDir = ensureAnalyticsDir();
  const metricsFile = join(monthDir, 'post-metrics.jsonl');

  const metrics: PostMetrics = {
    postId,
    title: options.title as string,
    contentType: options.content_type as string,
    metrics: {
      views: {
        day1: options.day1_views as number,
        day7: options.day7_views as number,
        day30: options.day30_views as number,
        total: options.views as number,
      },
      engagement: {
        comments: options.comments as number,
        shares: options.shares as number,
        likes: options.likes as number,
      },
    },
    trackedAt: new Date().toISOString(),
    dataSource: 'manual',
  };

  // Add engagement score if provided
  if (options.engagement) {
    metrics.metrics.engagement.scrollDepth = options.engagement as number;
  }

  // Append to JSONL file
  const line = JSON.stringify(metrics) + '\n';
  writeFileSync(metricsFile, line, { flag: 'a' });

  console.log(JSON.stringify({
    success: true,
    postId,
    savedTo: metricsFile,
    metrics: metrics.metrics,
  }, null, 2));
}

// Import metrics from JSON file
function importMetrics(jsonFile: string): void {
  if (!existsSync(jsonFile)) {
    console.error(`File not found: ${jsonFile}`);
    process.exit(1);
  }

  const data = JSON.parse(readFileSync(jsonFile, 'utf-8'));
  const metrics: PostMetrics[] = Array.isArray(data) ? data : [data];

  const monthDir = ensureAnalyticsDir();
  const metricsFile = join(monthDir, 'post-metrics.jsonl');

  let imported = 0;
  for (const metric of metrics) {
    if (metric.postId) {
      metric.trackedAt = metric.trackedAt || new Date().toISOString();
      metric.dataSource = metric.dataSource || 'import';
      writeFileSync(metricsFile, JSON.stringify(metric) + '\n', { flag: 'a' });
      imported++;
    }
  }

  console.log(JSON.stringify({
    success: true,
    imported,
    savedTo: metricsFile,
  }, null, 2));
}

// List tracked posts
function listPosts(options: Record<string, string | number | boolean>): void {
  const month = (options.month as string) || new Date().toISOString().slice(0, 7);
  const monthDir = join(ANALYTICS_DIR, month);

  if (!existsSync(monthDir)) {
    console.log(JSON.stringify({ posts: [], month, message: 'No analytics data for this month' }));
    return;
  }

  const metricsFile = join(monthDir, 'post-metrics.jsonl');
  if (!existsSync(metricsFile)) {
    console.log(JSON.stringify({ posts: [], month, message: 'No post metrics file' }));
    return;
  }

  const lines = readFileSync(metricsFile, 'utf-8').split('\n').filter(l => l.trim());
  const posts = lines.map(line => {
    try {
      const data = JSON.parse(line);
      return {
        postId: data.postId,
        title: data.title || 'Untitled',
        contentType: data.contentType,
        views: data.metrics?.views?.total || 0,
        trackedAt: data.trackedAt,
      };
    } catch {
      return null;
    }
  }).filter(Boolean);

  console.log(JSON.stringify({ posts, month, count: posts.length }, null, 2));
}

// Main CLI handler
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const target = args[1];

  switch (command) {
    case 'log': {
      if (!target) {
        console.error('Usage: track-performance log <post-id> [options]');
        process.exit(1);
      }
      const options = parseArgs(args.slice(2));
      logMetrics(target, options);
      break;
    }

    case 'import': {
      if (!target) {
        console.error('Usage: track-performance import <json-file>');
        process.exit(1);
      }
      importMetrics(target);
      break;
    }

    case 'list': {
      const options = parseArgs(args.slice(1));
      listPosts(options);
      break;
    }

    case 'help':
    default:
      console.log(`
Track Performance CLI - Log and manage blog post metrics

Commands:
  log <post-id> [options]    Log metrics for a post
  import <json-file>         Import metrics from JSON file
  list [options]             List tracked posts
  help                       Show this help message

Options for 'log':
  --views <number>           Total views
  --day1-views <number>      Day 1 views
  --day7-views <number>      Day 7 views
  --day30-views <number>     Day 30 views
  --engagement <number>      Engagement score (0-100)
  --comments <number>        Number of comments
  --shares <number>          Number of shares
  --title <string>           Post title
  --content-type <string>    Content type (tech|personal-dev)

Options for 'list':
  --month <YYYY-MM>          Month to list (default: current)

Examples:
  bun run TrackPerformance.ts log post-123 --views 1500 --engagement 85
  bun run TrackPerformance.ts log post-456 --title "Docker MCP" --content-type tech
  bun run TrackPerformance.ts import ./metrics.json
  bun run TrackPerformance.ts list --month 2025-01
`);
      process.exit(command === 'help' ? 0 : 1);
  }
}

main();
