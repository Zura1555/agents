#!/usr/bin/env bun
/**
 * Content Validation CLI
 *
 * Deterministic content validation tool for blog posts.
 * Part of the enhanced blog writing system.
 *
 * Usage:
 *   validate-content check <file>         Full validation check
 *   validate-content word-count <file>    Word count analysis
 *   validate-content structure <file>     Structure validation
 *   validate-content brand-voice <file>   Brand voice compliance
 *   validate-content readability <file>   Readability analysis
 *   validate-content help                 Show this help message
 *
 * Examples:
 *   bun run ValidateContent.ts check ./draft.md
 *   bun run ValidateContent.ts word-count ./draft.md
 */

import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

// Content requirements
const WORD_COUNT_TARGETS = {
  tech: { min: 1000, max: 1200, target: 1100 },
  'personal-dev': { min: 1200, max: 1500, target: 1350 },
  default: { min: 800, max: 1500, target: 1100 },
};

// Brand voice keywords (Professional, Friendly, Authentic)
const BRAND_VOICE_INDICATORS = {
  professional: [
    'implement', 'solution', 'approach', 'strategy', 'optimize', 'efficient',
    'framework', 'methodology', 'best practice', 'recommend', 'analysis',
  ],
  friendly: [
    "let's", "you'll", "we", "together", 'enjoy', 'love', 'excited',
    'awesome', 'great', 'amazing', "isn't it", 'right?', 'imagine',
  ],
  authentic: [
    'honestly', 'personally', 'in my experience', 'I learned', 'I found',
    'real', 'genuine', 'truth', 'admit', 'struggle', 'challenge',
  ],
};

// Required structure elements
const STRUCTURE_REQUIREMENTS = {
  hasTitle: true,
  hasIntroduction: true,
  hasConclusion: true,
  minSections: 5,
  maxSections: 9,
  maxConclusionParagraphs: 3,
};

interface ValidationResult {
  valid: boolean;
  score: number;
  issues: string[];
  suggestions: string[];
}

interface WordCountResult {
  total: number;
  perSection: Record<string, number>;
  readingTime: number;
  target: { min: number; max: number; target: number };
  withinRange: boolean;
}

interface StructureResult {
  valid: boolean;
  sections: string[];
  sectionCount: number;
  hasTitle: boolean;
  hasIntroduction: boolean;
  hasConclusion: boolean;
  conclusionParagraphs: number;
  issues: string[];
}

interface BrandVoiceResult {
  score: number;
  breakdown: {
    professional: { score: number; indicators: string[] };
    friendly: { score: number; indicators: string[] };
    authentic: { score: number; indicators: string[] };
  };
  balance: 'good' | 'needs_adjustment';
  suggestions: string[];
}

interface ReadabilityResult {
  sentenceCount: number;
  avgWordsPerSentence: number;
  avgSyllablesPerWord: number;
  fleschReadingEase: number;
  gradeLevel: string;
  issues: string[];
}

// Parse markdown to extract sections
function parseMarkdown(content: string): { title: string; sections: Array<{ heading: string; content: string }> } {
  const lines = content.split('\n');
  let title = '';
  const sections: Array<{ heading: string; content: string }> = [];
  let currentSection: { heading: string; content: string } | null = null;

  for (const line of lines) {
    // Check for title (H1)
    if (line.startsWith('# ') && !title) {
      title = line.slice(2).trim();
      continue;
    }

    // Check for section heading (H2)
    if (line.startsWith('## ')) {
      if (currentSection) {
        sections.push(currentSection);
      }
      currentSection = { heading: line.slice(3).trim(), content: '' };
      continue;
    }

    // Add content to current section
    if (currentSection) {
      currentSection.content += line + '\n';
    }
  }

  // Don't forget the last section
  if (currentSection) {
    sections.push(currentSection);
  }

  return { title, sections };
}

// Count words in text
function countWords(text: string): number {
  return text
    .replace(/[#*`_\[\]()]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 0).length;
}

// Count syllables in a word (simplified)
function countSyllables(word: string): number {
  word = word.toLowerCase().replace(/[^a-z]/g, '');
  if (word.length <= 3) return 1;

  word = word.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '');
  word = word.replace(/^y/, '');
  const matches = word.match(/[aeiouy]{1,2}/g);
  return matches ? matches.length : 1;
}

// Detect content type from filename or content
function detectContentType(filePath: string, content: string): 'tech' | 'personal-dev' | 'default' {
  const fileName = filePath.toLowerCase();
  if (fileName.includes('tech') || fileName.includes('technical')) return 'tech';
  if (fileName.includes('personal') || fileName.includes('dev')) return 'personal-dev';

  // Check content for indicators
  const techIndicators = ['code', 'implementation', 'api', 'function', 'class', 'programming'];
  const personalIndicators = ['journey', 'learned', 'experience', 'growth', 'reflection'];

  const lowerContent = content.toLowerCase();
  let techScore = 0;
  let personalScore = 0;

  for (const indicator of techIndicators) {
    if (lowerContent.includes(indicator)) techScore++;
  }
  for (const indicator of personalIndicators) {
    if (lowerContent.includes(indicator)) personalScore++;
  }

  if (techScore > personalScore) return 'tech';
  if (personalScore > techScore) return 'personal-dev';
  return 'default';
}

// Word count analysis
function analyzeWordCount(filePath: string): WordCountResult {
  const content = readFileSync(filePath, 'utf-8');
  const { title, sections } = parseMarkdown(content);
  const contentType = detectContentType(filePath, content);
  const target = WORD_COUNT_TARGETS[contentType];

  const perSection: Record<string, number> = {};
  let total = countWords(title);

  for (const section of sections) {
    const sectionWords = countWords(section.content);
    perSection[section.heading] = sectionWords;
    total += sectionWords;
  }

  return {
    total,
    perSection,
    readingTime: Math.ceil(total / 200),
    target,
    withinRange: total >= target.min && total <= target.max,
  };
}

// Structure validation
function analyzeStructure(filePath: string): StructureResult {
  const content = readFileSync(filePath, 'utf-8');
  const { title, sections } = parseMarkdown(content);
  const issues: string[] = [];

  const hasTitle = !!title;
  const hasIntroduction = sections.some(s =>
    s.heading.toLowerCase().includes('intro') ||
    s.heading.toLowerCase().includes('overview') ||
    sections.indexOf(s) === 0
  );

  const conclusionSection = sections.find(s =>
    s.heading.toLowerCase().includes('conclusion') ||
    s.heading.toLowerCase().includes('summary') ||
    s.heading.toLowerCase().includes('wrap')
  );
  const hasConclusion = !!conclusionSection;
  const conclusionParagraphs = conclusionSection
    ? conclusionSection.content.split(/\n\n+/).filter(p => p.trim().length > 0).length
    : 0;

  // Validate requirements
  if (!hasTitle) issues.push('Missing title (H1)');
  if (!hasIntroduction) issues.push('Missing introduction section');
  if (!hasConclusion) issues.push('Missing conclusion section');

  if (sections.length < STRUCTURE_REQUIREMENTS.minSections) {
    issues.push(`Too few sections: ${sections.length} (min: ${STRUCTURE_REQUIREMENTS.minSections})`);
  }
  if (sections.length > STRUCTURE_REQUIREMENTS.maxSections) {
    issues.push(`Too many sections: ${sections.length} (max: ${STRUCTURE_REQUIREMENTS.maxSections})`);
  }

  if (conclusionParagraphs > STRUCTURE_REQUIREMENTS.maxConclusionParagraphs) {
    issues.push(`Conclusion too long: ${conclusionParagraphs} paragraphs (max: ${STRUCTURE_REQUIREMENTS.maxConclusionParagraphs})`);
  }

  return {
    valid: issues.length === 0,
    sections: sections.map(s => s.heading),
    sectionCount: sections.length,
    hasTitle,
    hasIntroduction,
    hasConclusion,
    conclusionParagraphs,
    issues,
  };
}

// Brand voice analysis
function analyzeBrandVoice(filePath: string): BrandVoiceResult {
  const content = readFileSync(filePath, 'utf-8').toLowerCase();
  const breakdown: BrandVoiceResult['breakdown'] = {
    professional: { score: 0, indicators: [] },
    friendly: { score: 0, indicators: [] },
    authentic: { score: 0, indicators: [] },
  };

  // Check each brand voice category
  for (const [category, indicators] of Object.entries(BRAND_VOICE_INDICATORS)) {
    for (const indicator of indicators) {
      if (content.includes(indicator.toLowerCase())) {
        breakdown[category as keyof typeof breakdown].score += 1;
        breakdown[category as keyof typeof breakdown].indicators.push(indicator);
      }
    }
  }

  // Normalize scores
  const maxPossible = Math.max(
    BRAND_VOICE_INDICATORS.professional.length,
    BRAND_VOICE_INDICATORS.friendly.length,
    BRAND_VOICE_INDICATORS.authentic.length
  );

  const professionalScore = Math.min(25, (breakdown.professional.score / maxPossible) * 100);
  const friendlyScore = Math.min(25, (breakdown.friendly.score / maxPossible) * 100);
  const authenticScore = Math.min(25, (breakdown.authentic.score / maxPossible) * 100);

  const totalScore = Math.round(professionalScore + friendlyScore + authenticScore);
  const suggestions: string[] = [];

  // Check balance
  const scores = [professionalScore, friendlyScore, authenticScore];
  const minScore = Math.min(...scores);
  const maxScore = Math.max(...scores);
  const balance = maxScore - minScore < 15 ? 'good' : 'needs_adjustment';

  if (professionalScore < 10) suggestions.push('Add more professional terminology and structured language');
  if (friendlyScore < 10) suggestions.push('Use more conversational phrases and second-person ("you")');
  if (authenticScore < 10) suggestions.push('Include personal experiences and honest reflections');

  return {
    score: totalScore,
    breakdown,
    balance,
    suggestions,
  };
}

// Readability analysis
function analyzeReadability(filePath: string): ReadabilityResult {
  const content = readFileSync(filePath, 'utf-8')
    .replace(/[#*`_\[\]()]/g, ' ')
    .replace(/\n+/g, ' ');

  const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const words = content.split(/\s+/).filter(w => w.length > 0);

  const sentenceCount = sentences.length;
  const wordCount = words.length;
  const avgWordsPerSentence = wordCount / sentenceCount;

  let totalSyllables = 0;
  for (const word of words) {
    totalSyllables += countSyllables(word);
  }
  const avgSyllablesPerWord = totalSyllables / wordCount;

  // Flesch Reading Ease formula
  const fleschReadingEase = 206.835 - 1.015 * avgWordsPerSentence - 84.6 * avgSyllablesPerWord;

  // Determine grade level
  let gradeLevel: string;
  if (fleschReadingEase >= 90) gradeLevel = '5th grade';
  else if (fleschReadingEase >= 80) gradeLevel = '6th grade';
  else if (fleschReadingEase >= 70) gradeLevel = '7th grade';
  else if (fleschReadingEase >= 60) gradeLevel = '8th-9th grade';
  else if (fleschReadingEase >= 50) gradeLevel = '10th-12th grade';
  else if (fleschReadingEase >= 30) gradeLevel = 'College';
  else gradeLevel = 'College graduate';

  const issues: string[] = [];
  if (avgWordsPerSentence > 25) issues.push('Sentences too long (avg > 25 words)');
  if (fleschReadingEase < 50) issues.push('Content may be too complex for general audience');
  if (fleschReadingEase > 80) issues.push('Content may be too simple for technical audience');

  return {
    sentenceCount,
    avgWordsPerSentence: Math.round(avgWordsPerSentence * 10) / 10,
    avgSyllablesPerWord: Math.round(avgSyllablesPerWord * 100) / 100,
    fleschReadingEase: Math.round(fleschReadingEase),
    gradeLevel,
    issues,
  };
}

// Full validation check
function fullCheck(filePath: string): ValidationResult {
  const issues: string[] = [];
  const suggestions: string[] = [];
  let score = 100;

  // Word count (25 points)
  const wordCount = analyzeWordCount(filePath);
  if (!wordCount.withinRange) {
    score -= 15;
    if (wordCount.total < wordCount.target.min) {
      issues.push(`Word count too low: ${wordCount.total} (min: ${wordCount.target.min})`);
    } else {
      issues.push(`Word count too high: ${wordCount.total} (max: ${wordCount.target.max})`);
    }
  }

  // Structure (25 points)
  const structure = analyzeStructure(filePath);
  if (!structure.valid) {
    score -= structure.issues.length * 5;
    issues.push(...structure.issues);
  }

  // Brand voice (25 points)
  const brandVoice = analyzeBrandVoice(filePath);
  if (brandVoice.score < 50) {
    score -= 15;
    issues.push(`Brand voice score low: ${brandVoice.score}%`);
  }
  suggestions.push(...brandVoice.suggestions);

  // Readability (25 points)
  const readability = analyzeReadability(filePath);
  if (readability.issues.length > 0) {
    score -= readability.issues.length * 5;
    issues.push(...readability.issues);
  }

  return {
    valid: score >= 70,
    score: Math.max(0, score),
    issues,
    suggestions,
  };
}

// Main CLI handler
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const filePath = args[1] ? resolve(args[1]) : '';

  if (filePath && !existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }

  switch (command) {
    case 'check': {
      if (!filePath) {
        console.error('Usage: validate-content check <file>');
        process.exit(1);
      }
      const result = fullCheck(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.valid ? 0 : 1);
    }

    case 'word-count': {
      if (!filePath) {
        console.error('Usage: validate-content word-count <file>');
        process.exit(1);
      }
      const result = analyzeWordCount(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.withinRange ? 0 : 1);
    }

    case 'structure': {
      if (!filePath) {
        console.error('Usage: validate-content structure <file>');
        process.exit(1);
      }
      const result = analyzeStructure(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.valid ? 0 : 1);
    }

    case 'brand-voice': {
      if (!filePath) {
        console.error('Usage: validate-content brand-voice <file>');
        process.exit(1);
      }
      const result = analyzeBrandVoice(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.score >= 50 ? 0 : 1);
    }

    case 'readability': {
      if (!filePath) {
        console.error('Usage: validate-content readability <file>');
        process.exit(1);
      }
      const result = analyzeReadability(filePath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.issues.length === 0 ? 0 : 1);
    }

    case 'help':
    default:
      console.log(`
Content Validation CLI - Deterministic content validation tool

Commands:
  check <file>         Full validation check (score out of 100)
  word-count <file>    Word count analysis with per-section breakdown
  structure <file>     Structure validation (sections, conclusion length)
  brand-voice <file>   Brand voice compliance (Professional, Friendly, Authentic)
  readability <file>   Readability analysis (Flesch score, grade level)
  help                 Show this help message

Scoring Criteria (100 points):
  Word Count:    25 pts (within target range)
  Structure:     25 pts (proper sections, conclusion length)
  Brand Voice:   25 pts (balanced P-F-A indicators)
  Readability:   25 pts (appropriate complexity)

Word Count Targets:
  Tech:          1000-1200 words (5-6 min read)
  Personal Dev:  1200-1500 words (6-8 min read)
  Default:       800-1500 words

Examples:
  bun run ValidateContent.ts check ./draft.md
  bun run ValidateContent.ts word-count ./draft-tech.md
  bun run ValidateContent.ts brand-voice ./polished-draft.md
`);
      process.exit(command === 'help' ? 0 : 1);
  }
}

main();
