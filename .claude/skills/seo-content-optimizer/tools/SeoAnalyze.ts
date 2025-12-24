#!/usr/bin/env bun
/**
 * SEO Analysis CLI
 *
 * Deterministic SEO validation and analysis tool for blog content.
 * Part of the enhanced blog writing system.
 *
 * Usage:
 *   seo-analyze validate <file>        Validate SEO metadata against schema
 *   seo-analyze score <file>           Calculate comprehensive SEO score
 *   seo-analyze check-limits <file>    Check character limits compliance
 *   seo-analyze suggestions <file>     Generate improvement suggestions
 *   seo-analyze help                   Show this help message
 *
 * Examples:
 *   bun run seo-analyze.ts validate ./seo-metadata.json
 *   bun run seo-analyze.ts check-limits ./seo-metadata.json
 */

import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

// Character limit definitions
const CHAR_LIMITS = {
  metaTitle: { min: 50, max: 60, field: 'title' },
  metaDescription: { min: 150, max: 160, field: 'metaDescription' },
  ogDescription: { min: 100, max: 120, field: 'openGraph.description' },
  twitterDescription: { min: 100, max: 200, field: 'twitter.description' },
};

// Required SEO schema fields
const REQUIRED_FIELDS = [
  'title',
  'metaDescription',
  'keywords',
  'openGraph',
  'openGraph.title',
  'openGraph.description',
  'openGraph.type',
  'twitter',
  'twitter.card',
  'twitter.title',
  'twitter.description',
];

interface SEOMetadata {
  title: string;
  metaDescription: string;
  keywords: {
    primary: string[];
    secondary: string[];
    lsi?: string[];
    longTail?: string[];
  };
  openGraph: {
    title: string;
    description: string;
    type: string;
    image?: string;
    url?: string;
  };
  twitter: {
    card: string;
    title: string;
    description: string;
    image?: string;
  };
  score?: number;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

interface LimitCheckResult {
  field: string;
  value: number;
  min: number;
  max: number;
  valid: boolean;
  status: 'ok' | 'too_short' | 'too_long';
}

// Helper to get nested property
function getNestedValue(obj: any, path: string): any {
  return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

// Validate SEO metadata against schema
function validate(filePath: string): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };

  if (!existsSync(filePath)) {
    result.valid = false;
    result.errors.push(`File not found: ${filePath}`);
    return result;
  }

  let metadata: SEOMetadata;
  try {
    metadata = JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch (e) {
    result.valid = false;
    result.errors.push(`Invalid JSON: ${(e as Error).message}`);
    return result;
  }

  // Check required fields
  for (const field of REQUIRED_FIELDS) {
    const value = getNestedValue(metadata, field);
    if (value === undefined || value === null || value === '') {
      result.valid = false;
      result.errors.push(`Missing required field: ${field}`);
    }
  }

  // Check keywords array
  if (metadata.keywords) {
    if (!metadata.keywords.primary || metadata.keywords.primary.length === 0) {
      result.valid = false;
      result.errors.push('At least one primary keyword required');
    }
    if (!metadata.keywords.secondary || metadata.keywords.secondary.length === 0) {
      result.warnings.push('Consider adding secondary keywords');
    }
  }

  // Check character limits
  const limitResults = checkLimits(filePath);
  for (const check of limitResults) {
    if (!check.valid) {
      result.valid = false;
      result.errors.push(`${check.field}: ${check.value} chars (${check.status}, should be ${check.min}-${check.max})`);
    }
  }

  return result;
}

// Check character limits
function checkLimits(filePath: string): LimitCheckResult[] {
  const results: LimitCheckResult[] = [];

  if (!existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return results;
  }

  const metadata: SEOMetadata = JSON.parse(readFileSync(filePath, 'utf-8'));

  for (const [key, limit] of Object.entries(CHAR_LIMITS)) {
    const value = getNestedValue(metadata, limit.field);
    if (typeof value === 'string') {
      const length = value.length;
      let status: 'ok' | 'too_short' | 'too_long' = 'ok';
      let valid = true;

      if (length < limit.min) {
        status = 'too_short';
        valid = false;
      } else if (length > limit.max) {
        status = 'too_long';
        valid = false;
      }

      results.push({
        field: key,
        value: length,
        min: limit.min,
        max: limit.max,
        valid,
        status,
      });
    }
  }

  return results;
}

// Calculate SEO score
function calculateScore(filePath: string): { score: number; breakdown: Record<string, number> } {
  if (!existsSync(filePath)) {
    return { score: 0, breakdown: {} };
  }

  const metadata: SEOMetadata = JSON.parse(readFileSync(filePath, 'utf-8'));
  const breakdown: Record<string, number> = {};
  let totalScore = 0;

  // Keyword Optimization (25 points)
  let keywordScore = 0;
  if (metadata.keywords?.primary?.length > 0) keywordScore += 10;
  if (metadata.keywords?.secondary?.length >= 2) keywordScore += 5;
  if (metadata.keywords?.lsi?.length > 0) keywordScore += 5;
  if (metadata.keywords?.longTail?.length > 0) keywordScore += 5;
  breakdown['keywordOptimization'] = keywordScore;
  totalScore += keywordScore;

  // Content Structure (25 points)
  let structureScore = 0;
  if (metadata.title && metadata.title.length >= 50 && metadata.title.length <= 60) structureScore += 10;
  if (metadata.metaDescription && metadata.metaDescription.length >= 150 && metadata.metaDescription.length <= 160) structureScore += 10;
  if (metadata.openGraph?.description) structureScore += 5;
  breakdown['contentStructure'] = structureScore;
  totalScore += structureScore;

  // Technical SEO (20 points)
  let technicalScore = 0;
  if (metadata.openGraph?.type) technicalScore += 5;
  if (metadata.openGraph?.image) technicalScore += 5;
  if (metadata.twitter?.card) technicalScore += 5;
  if (metadata.twitter?.image) technicalScore += 5;
  breakdown['technicalSEO'] = technicalScore;
  totalScore += technicalScore;

  // Social Media Optimization (15 points)
  let socialScore = 0;
  if (metadata.openGraph?.title) socialScore += 5;
  if (metadata.openGraph?.description && metadata.openGraph.description.length >= 100 && metadata.openGraph.description.length <= 120) socialScore += 5;
  if (metadata.twitter?.title) socialScore += 5;
  breakdown['socialOptimization'] = socialScore;
  totalScore += socialScore;

  // User Value (15 points) - based on metadata completeness
  let userValueScore = 0;
  const allFieldsPresent = REQUIRED_FIELDS.every(f => getNestedValue(metadata, f) !== undefined);
  if (allFieldsPresent) userValueScore += 15;
  breakdown['userValue'] = userValueScore;
  totalScore += userValueScore;

  return { score: totalScore, breakdown };
}

// Generate improvement suggestions
function generateSuggestions(filePath: string): string[] {
  const suggestions: string[] = [];

  if (!existsSync(filePath)) {
    suggestions.push('File not found - create SEO metadata first');
    return suggestions;
  }

  const metadata: SEOMetadata = JSON.parse(readFileSync(filePath, 'utf-8'));
  const limitResults = checkLimits(filePath);

  // Character limit suggestions
  for (const check of limitResults) {
    if (check.status === 'too_short') {
      suggestions.push(`${check.field}: Add ${check.min - check.value} more characters (current: ${check.value}, min: ${check.min})`);
    } else if (check.status === 'too_long') {
      suggestions.push(`${check.field}: Remove ${check.value - check.max} characters (current: ${check.value}, max: ${check.max})`);
    }
  }

  // Keyword suggestions
  if (!metadata.keywords?.lsi || metadata.keywords.lsi.length === 0) {
    suggestions.push('Add LSI (Latent Semantic Indexing) keywords for better semantic relevance');
  }
  if (!metadata.keywords?.longTail || metadata.keywords.longTail.length === 0) {
    suggestions.push('Add long-tail keywords to target specific search queries');
  }

  // Image suggestions
  if (!metadata.openGraph?.image) {
    suggestions.push('Add Open Graph image for better social media previews');
  }
  if (!metadata.twitter?.image) {
    suggestions.push('Add Twitter card image for enhanced tweet previews');
  }

  // Score-based suggestions
  const { score, breakdown } = calculateScore(filePath);
  if (score < 85) {
    suggestions.push(`Current SEO score: ${score}/100 - target 85+ for optimal performance`);
    for (const [category, points] of Object.entries(breakdown)) {
      if (points < 15) {
        suggestions.push(`Improve ${category} (current: ${points} points)`);
      }
    }
  }

  return suggestions;
}

// Main CLI handler
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const filePath = args[1] ? resolve(args[1]) : '';

  switch (command) {
    case 'validate': {
      if (!filePath) {
        console.error('Usage: seo-analyze validate <file>');
        process.exit(1);
      }
      const result = validate(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.valid ? 0 : 1);
    }

    case 'score': {
      if (!filePath) {
        console.error('Usage: seo-analyze score <file>');
        process.exit(1);
      }
      const result = calculateScore(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.score >= 85 ? 0 : 1);
    }

    case 'check-limits': {
      if (!filePath) {
        console.error('Usage: seo-analyze check-limits <file>');
        process.exit(1);
      }
      const results = checkLimits(filePath);
      console.log(JSON.stringify(results, null, 2));
      const allValid = results.every(r => r.valid);
      process.exit(allValid ? 0 : 1);
    }

    case 'suggestions': {
      if (!filePath) {
        console.error('Usage: seo-analyze suggestions <file>');
        process.exit(1);
      }
      const suggestions = generateSuggestions(filePath);
      console.log(JSON.stringify(suggestions, null, 2));
      process.exit(0);
    }

    case 'help':
    default:
      console.log(`
SEO Analysis CLI - Deterministic SEO validation tool

Commands:
  validate <file>        Validate SEO metadata against schema
  score <file>           Calculate comprehensive SEO score (100-point scale)
  check-limits <file>    Check character limits compliance
  suggestions <file>     Generate improvement suggestions
  help                   Show this help message

Character Limits:
  Meta Title:        50-60 characters
  Meta Description:  150-160 characters
  OG Description:    100-120 characters
  Twitter Desc:      100-200 characters

Examples:
  bun run SeoAnalyze.ts validate ./seo-metadata.json
  bun run SeoAnalyze.ts score ./seo-metadata.json
  bun run SeoAnalyze.ts check-limits ./seo-metadata.json
`);
      process.exit(command === 'help' ? 0 : 1);
  }
}

main();
