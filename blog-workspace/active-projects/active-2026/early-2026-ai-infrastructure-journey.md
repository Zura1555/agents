---
title: "My Early 2026 AI Infrastructure Journey: From PAI Setup to Automated Blog Publishing"
slug: "early-2026-ai-infrastructure-journey"
description: "How I spent the beginning of 2026 building a personal AI infrastructure that automates my blog publishing workflow, voice notifications, and task management."
date: "2026-01-10"
tags: ["personal-ai", "claude-code", "automation", "n8n", "replicate", "sanity-cms"]
cover_image: "/blog-images/early-2026-ai-infrastructure.jpg"
author: "Admin"
---

# My Early 2026 AI Infrastructure Journey: From PAI Setup to Automated Blog Publishing

*Published: January 10, 2026*

---

## The Beginning: Diving Deep into Personal AI Infrastructure

If you've been following my journey, you know I'm obsessed with making AI work for me rather than the other way around. The beginning of 2026 was no different—I decided to dive deep into **Personal AI Infrastructure (PAI)**, a project by Daniel Miessler that completely changes how you interact with Claude Code.

PAI introduces two powerful concepts that I hadn't fully appreciated before: **hooks** and **skills**. These aren't just features—they're the foundation of a truly personal AI assistant.

One hook that particularly blew my mind is the voice notification system. Using the ElevenLabs API, PAI can actually speak to you when it finishes a task. Imagine this: you're running a complex build or deployment, and instead of staring at the terminal waiting for it to finish, you can walk away. When it's done, your AI assistant literally tells you "Task completed successfully" with a summary of what was accomplished. It's like having a personal assistant who reports back to you in real-time.

---

## The Windows Challenge: Making PAI Work Outside the Apple Ecosystem

Here's the problem: PAI is designed primarily for Mac users. Daniel Miessler's setup assumes you're on macOS with all the native integrations that come with it. As a Windows user, I was staring at what seemed like an impossible wall.

But I don't give up easily.

I spent an entire day (yes, a full Saturday) getting PAI to run from my **PowerShell Playback** environment. It wasn't straightforward—there were path issues, environment variable mismatches, and more than a few "why isn't this working" moments. But I eventually cracked it.

The satisfaction of hearing my AI assistant speak through PowerShell after all that troubleshooting? Worth every frustrating minute.

---

## The ElevenLabs Problem: When Free Credits Burn Too Fast

One thing I didn't anticipate: the ElevenLabs credit consumption. PAI offers voice notifications, and while the quality is incredible, I quickly discovered that I was burning through credits alarmingly fast. During just a 3-day holiday period, I burned through 50,000 of my 100,000 monthly credits.

That's half my allocation in three days.

I knew I needed a backup plan—or better yet, an alternative that wouldn't break the bank.

---

## Finding Hume AI: A Beautiful Alternative

That's when I discovered [Hume AI](https://www.hume.ai/), and honestly, their website alone is worth visiting. It's minimal, beautiful, and immediately communicates that they're different from the competition.

**So how does Hume AI compare to ElevenLabs?**

| Feature | ElevenLabs | Hume AI |
|---------|------------|---------|
| **Focus** | Text-to-speech, voice cloning | Empathic AI, emotional intelligence |
| **Voice Quality** | Extremely realistic, industry-leading | Expressive, emotionally-aware |
| **Primary Use Case** | Audiobooks, content creation, dubbing | Conversational AI, voice interfaces |
| **Technology** | Traditional TTS models | Voice-based LLM (Octave 2) |
| **Languages** | 100+ languages | 11+ languages with under 200ms latency |
| **Latency** | Good for pre-recorded content | Optimized for real-time conversations |

**My take:** If you're doing voice notifications like I am with PAI, Hume AI's Octave 2 is compelling because it understands context and predicts emotions, cadence, and delivery. It's not just reading text—it's speaking it with understanding.

For ElevenLabs, I may consider local voice models in the future once I have more budget. Running TTS locally would eliminate the per-credit cost entirely.

---

## Why This Matters: The Productivity Argument

You might be wondering: why spend so much time on infrastructure instead of, you know, actually working?

I had the same question until I watched [this video from Daniel Miessler](https://www.youtube.com/watch?v=Le0DLrn7ta0). His argument changed my perspective entirely: **AI can automate tasks that compound over time, upgrading your capabilities in ways that multiply your output.**

Let me give you a concrete example from my own setup.

---

## My Obsidian Vault Agent: From Messy Ideas to Organized Actions

I set up a specialized agent that manages my Obsidian vault. Here's how it works:

1. **I'm in a meeting** and taking notes messily—ideas, next actions, random thoughts all jumbled together in my inbox
2. **I type it all into the chat**—no formatting, no organization, just raw input
3. **The agent takes over**: It reads my chaotic notes, understands the intent, and reorganizes everything into the appropriate folders—Project Notes, Next Actions, Reference Material, or Someday/Maybe

The best part? I'm not using Claude Opus 4.5 for this. As Daniel wisely says in his content, "don't use Opus 4.5 for this, your cost will exceed your productivity."

Instead, I'm using **MiniMax M2.1**, a Chinese LLM that's incredibly efficient and low-cost. It's perfect for orchestration tasks like this—organizing notes, routing tasks, and managing workflows. For high-level creative work and complex reasoning, I still use Claude. But for the mundane automation? MiniMax M2.1 is my go-to.

This setup has transformed how I capture ideas. No more "I'll organize that later" that never comes. It's organized automatically, and I can focus on the meeting itself.

---

## Automated Blog Images: From Text to Featured Image in Minutes

The most impressive automation I've built is for blog post images.

Remember the [Docker MCP blog post](/blog/docker-mcp-server)? Take a look at the featured image. Does it look like a generic canvas image from OpenAI DALL-E? No. It looks like an Excalidraw diagram, hand-drawn and specific to the blog content.

Here's how it works:

1. **I write the blog post** in Markdown
2. **My PAI agent extracts key concepts** from each section
3. **It sends those concepts to Replicate API** using the Excalidraw x Tron model
4. **The AI generates unique images** that visually represent each section
5. **The agent downloads the images**, maps them to the blog post, and prepares everything for Sanity CMS
6. **I review for 10 minutes**, make any tweaks, and hit publish

I call this technology **Nano Banana**—because it takes something complex (generating contextual images for blog posts) and makes it as simple as eating a banana.

---

## The Weekly Blog Commitment (And Why I Missed Last Week)

I've committed to posting one blog post per week. Last week? I missed it.

Why? Because I was busy setting up PAI version 2.

I'm not a very technical person, so I hired **Antigravity** to handle the setup and testing. I was essentially the "babysitter"—overseeing the process, checking results, and making sure everything worked as expected.

It was time well spent. The new PAI v2 infrastructure means:
- Faster voice notifications
- More reliable skill execution
- Better integration with my existing tools
- A foundation for future automation

Missing one blog post to build infrastructure that will save hours every week? That's a trade I'll make every time.

---

## The Workflow That Changed Everything

Here's my current automated workflow:

```
[Meeting Notes] → [MiniMax M2.1 Agent] → [Obsidian Vault Organization]
                                                     ↓
[Blog Draft] → [Replicate API + Excalidraw] → [AI-Generated Images]
                                                     ↓
[Sanity CMS] ← [Automated Mapping] ← [Nano Banana Pipeline]
                                                     ↓
                                    [10-Min Review] → [Published Post]
```

Every arrow represents something I used to do manually. Now? The AI handles it.

---

## What's Next?

My goals for the rest of 2026:

1. **Local voice model**: Once budget allows, set up a local TTS solution to eliminate API costs entirely
2. **More specialized agents**: Extend the Obsidian agent pattern to other workflows
3. **Expand Nano Banana**: Apply the automated image generation to other content types
4. **Better voice integration**: Fully integrate Hume AI as a fallback/alternative to ElevenLabs

---

## Final Thoughts

The beginning of 2026 taught me something important: **the best investment you can make is in infrastructure that compounds.**

Yes, setting up PAI on Windows took a whole day.
Yes, building the automated blog pipeline required research and experimentation.
Yes, finding alternatives to ElevenLabs meant more investigation.

But now I have systems that work for me 24/7, that improve every time I use them, and that free up my mental energy for creative work rather than repetitive tasks.

If you're on the fence about investing time in your AI infrastructure, my advice is simple: start with one automation, make it work, then build from there. You don't need to build everything at once. But you need to start.

The AI revolution isn't coming—it's here. The question is: are you using it to build your infrastructure, or are you still doing everything manually?

---

*Have questions about setting up PAI on Windows, voice notifications, or the Nano Banana pipeline? Drop a comment below or reach out to me directly.*

---

**Sources:**
- [Hume AI](https://www.hume.ai/)
- [Daniel Miessler - Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [Daniel Miessler - AI Can Automate Your Tasks](https://www.youtube.com/watch?v=Le0DLrn7ta0)
