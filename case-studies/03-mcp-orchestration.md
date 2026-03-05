# Case Study 03: MCP Multi-Tool Orchestration
## Production Integration Across 5+ Services

---

## Problem

Modern knowledge work happens across dozens of tools. Calendar events, email drafts, CRM entries, document creation, and task logging all live in different systems. Switching between them creates friction, context loss, and execution gaps.

The question: can a single AI layer sit on top of all of them and orchestrate actions across tools in one conversational flow?

---

## Architecture

```
Claude (orchestration layer)
    -> MCP connections
        -> Notion (knowledge base + logging)
        -> Google Calendar (scheduling)
        -> Gmail (communications)
        -> Google Drive (file storage)
        -> Apollo.io (CRM / prospecting)
```

### Routing Logic

```
Recipes, golf, music          -> log to Notion
Reminders                     -> Apple Reminders via MCP
Meetings, scheduling          -> Google Calendar MCP
Sheet music, manuals          -> Google Drive
Client comms                  -> Gmail (draft, confirm, then send)
FlowstateAI prospects         -> FlowstateAI Pipeline in Notion
```

---

## Build Details

**Stack**: Claude (Anthropic), Notion MCP, Google Calendar MCP, Gmail MCP, Google Drive, Apollo.io Pro

### What Makes It Different

- **Intent-based routing**: Claude determines which tool to use based on the content of the request, not explicit commands. Say "schedule a follow-up with the prospect" and it routes to Calendar. Say "log this to the pipeline" and it routes to Notion.
- **Confirmation gates**: nothing gets sent or logged without explicit approval. This prevents AI overreach while maintaining speed.
- **Cross-tool workflows**: a single conversation can search Apollo for prospects, draft a Gmail outreach, schedule a Calendar follow-up, and log the activity to Notion's pipeline. One flow, five tools.
- **Slash command layer**: custom commands (/log-golf, /log-cook, /log-photo, /log-flowstate) for rapid structured logging into domain-specific Notion databases.

---

## Result

- Single conversational interface for 5+ production tools
- Eliminated tab-switching for routine workflows
- Structured logging with prompted field completion (no missing data)
- Confirmation-gated actions that prevent AI errors in production

---

## Proof

The routing logic is documented in the CLAUDE.md Library. The slash commands, confirmation gates, and tool connections are all live and used daily for Yelp prospecting, FlowstateAI pipeline management, and personal life logging.

---

[Back to Portfolio](../README.md)
