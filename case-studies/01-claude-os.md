# Case Study 01: Claude OS
## A Personal AI Operating System with Context Routing

---

## Problem

AI assistants lose context between sessions. Every new conversation starts from zero. For someone operating across three distinct professional modes (enterprise sales, AI consultancy, personal life), this means constant re-explaining, inconsistent outputs, and wasted cycles.

The core question: how do you make AI remember who you are, how you work, and what you're building, across every session, without manual copy-pasting?

---

## Architecture

```
CLAUDE.md master context file
    -> Mode-specific prompts (FlowstateAI, Business, Personal)
    -> Trigger phrase routing ("FlowstateAI mode", "Business mode", "Personal mode")
    -> Notion-hosted prompt database (Claude Prompt OS)
    -> Session startup checklist (5-step verification)
```

### Key Components

1. **CLAUDE.md Library**: a persistent context file containing identity, rules, routing logic, technical preferences, communication style (ENFP-calibrated), and a living mistakes log that evolves with every correction

2. **Claude Prompt OS**: a Notion database housing mode-specific prompts with trigger phrases, version tracking, and status management

3. **Context Hub**: a central Notion page that routes to the correct prompt based on the session's domain

4. **Error Correction Protocol**: a "Mistakes" section modeled on Boris Cherny's methodology. Every correction gets logged permanently. The system learns from its failures.

---

## Build Details

**Stack**: Claude (Anthropic), Notion (MCP integration), structured markdown

### What Makes It Different

- **Three-mode architecture**: FlowstateAI (AI consulting), Business (sales/agency), Personal (life management). Each mode loads different context, rules, and behavior patterns.
- **Personality-calibrated responses**: ENFP profile mapped to communication preferences. Vision first, then concrete actions. Peer tone, not assistant tone.
- **Self-healing context**: the mistakes log means the system gets more accurate over time without manual prompt rewrites.
- **Session resumability**: every build gets a Resume Card with exact state, so any future session can pick up where the last one left off.

---

## Result

- Zero cold-start sessions across 3 professional domains
- Consistent output quality regardless of which device or conversation is used
- Living system that improves with use (mistakes log has captured 6+ recurring corrections)
- Foundation layer that every other build in this portfolio depends on

---

## Proof

The CLAUDE.md Library, Claude Prompt OS database, and Context Hub are all live and in daily use. This portfolio itself was built using the system it describes.

---

[Back to Portfolio](../README.md)
