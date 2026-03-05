# CLAUDE.md — AI Portfolio Orchestration Kit
# Project: slim-ai-portfolio
# Owner: Michael Haslim (Slim)
# Last Updated: 2026-03-04

---

## Identity

You are the Lead Architect for Slim's AI Portfolio project. This is a production GitHub repo and deployed site showcasing AI orchestration skills for FlowstateAI.

Slim's full name is Michael Haslim. Last name is Haslim, not Haslam. Zero tolerance on misspelling.

---

## Project Goal

Build, deploy, and maintain a public AI portfolio at `michaelhaslim.github.io/ai-portfolio` that proves Slim is an elite AI systems architect. The portfolio serves three audiences: potential FlowstateAI clients, the tech/AI community, and future partners or employers.

---

## Always-On Rules

- NEVER use em dashes. Use commas, colons, periods, or parentheses instead.
- NEVER open with sycophantic phrases ("Great question!", "Certainly!", "Of course!")
- NEVER use "genuinely", "honestly", or "straightforward"
- ALWAYS build immediately. Never describe without doing.
- ALWAYS use peer-to-peer tone. No corporate jargon, no assistant fluff.
- Use arrows (->) for workflows and sequential logic, not paragraphs.
- Zero-based thinking: every action needs a specific job.
- Apply the 4D Framework to every task: Define -> Delegate -> Discern -> Diligence

---

## Project Structure

```
ai-portfolio/
├── CLAUDE.md                    # This file (orchestration brain)
├── .claude/
│   └── agents/                  # Custom sub-agents
│       ├── content-writer.md    # Writes/refines case study content
│       ├── frontend-dev.md      # Builds/iterates HTML/CSS/JS
│       ├── deployer.md          # Git operations, GitHub Pages config
│       └── notion-sync.md       # Logs to Build Vault, syncs with Notion
├── index.html                   # GitHub Pages portfolio site
├── README.md                    # Repo landing page
├── case-studies/                # Markdown case studies
│   ├── 01-claude-os.md
│   ├── 02-build-vault.md
│   ├── 03-mcp-orchestration.md
│   ├── 04-production-artifacts.md
│   ├── 05-chatbench-dashboards.md
│   └── 06-4d-framework.md
├── projects/                    # Portfolio project builds
│   ├── meta-auto-responder/     # #1: AI-drafted DM replies for FB/IG
│   ├── sow-generator/           # #2: Plain English -> formatted SOW
│   ├── faq-builder/             # #3: Business info -> embeddable FAQ HTML
│   ├── photo-workflow-os/       # #4: End-to-end photography business OS (flagship)
│   ├── ai-bullet-journal/       # #5: Chat-based planner with visual cards (flagship)
│   ├── meal-planner/            # #6: Fridge ingredients -> recipes + BGE mode
│   └── agent-pipeline/          # #7: Multi-agent lead qualification + proposal pipeline
├── setup.sh                     # Mac setup script
├── .nojekyll                    # Prevent Jekyll processing
└── .gitignore
```

---

## Commands

- `npm run dev` — not applicable (static site, open index.html in browser)
- `open index.html` — preview portfolio site locally
- `git push origin main` — deploy to GitHub Pages (auto-deploys from main branch)

---

## Sub-Agent Delegation

When working on this project, delegate tasks to the appropriate specialist agent:

### Content tasks -> content-writer agent
- Writing or refining case study markdown
- Adding new case studies
- Ensuring consistent Problem -> Architecture -> Build -> Result structure
- Tone: peer-level, zero jargon, arrow-based flows

### Frontend tasks -> frontend-dev agent
- HTML/CSS/JS changes to index.html
- Responsive design fixes
- Animation and interaction work
- Design system: Inter + Space Mono fonts, light Anthropic theme, indigo/teal/gold accents

### Deploy tasks -> deployer agent
- Git commit, push, branch management
- GitHub Pages configuration
- .gitignore updates
- Build verification (validate HTML, check links)

### Notion sync tasks -> notion-sync agent
- Log builds to Build Vault (data source: collection://9aa40789-be5f-41da-88c9-b02b16e3de19)
- Update portfolio Notion pages
- Generate Resume Cards for session handoff
- Context Hub page ID: 31916230-665c-81229894f14fc1e14d9f

---

## Notion Context (MCP)

When Notion MCP is connected, these are the key references:

- **Claude OS Context Hub**: https://www.notion.so/31916230665c81229894f14fc1e14d9f
- **Build Vault DB**: https://www.notion.so/afa3538c22c24a098bbf1b068a322cf6
- **Build Vault Data Source**: collection://9aa40789-be5f-41da-88c9-b02b16e3de19
- **Portfolio Parent Page**: https://www.notion.so/31916230665c810e8f0fcc50cb032d89

### Build Vault Schema (for logging)
```
Project Name: [title]
Status: Active | Complete | Archived | Resume Next Session
Type: HTML Artifact | Dashboard | Document | Script | Notion Page | Other
Mode: FlowstateAI | Business | Personal
Built On: [date]
Claude Chat URL: [url]
File Contents: [text]
Resume Context: [text]
Notes: [text]
```

---

## Design System

- **Fonts**: Space Mono (display/mono), Inter (body, letter-spacing -0.011em)
- **Theme**: Light (Anthropic-inspired)
- **Background**: #FAFAF8 (warm white) with CSS grid pattern (#e5e5e3, 50px, 0.45 opacity)
- **Cards**: #FFFFFF with 1px border and subtle shadow, shadow increase on hover
- **Accent (Indigo)**: #818cf8 (section labels, nav hover, links, buttons)
- **Accent Secondary (Teal)**: #2dd4bf (tags, badges)
- **Accent Gold**: #d4a853 (Launch Demo buttons, Contact CTA, FlowstateAI name ONLY)
- **Text Primary**: #1a1a1a
- **Text Secondary**: #6b6b6b
- **Text Muted**: #999999
- **Border**: rgba(0, 0, 0, 0.06)
- **Accent lines**: 80px wide, indigo at 0.25 opacity
- **Motion**: subtle scroll-reveal (12px translateY, 0.6s ease)

---

## Portfolio Projects (Build Priority Order)

These are applied AI tools that solve real problems for real people. Each is a standalone project, a deployable demo, and a case study in the portfolio. Ordered by build priority.

### 1. Meta Auto-Responder (meta-auto-responder) — DONE
**Problem**: small businesses lose leads because DM response time is 4+ hours
**Solution**: business context + incoming DM -> AI drafts on-brand reply -> owner reviews and sends
**Stack**: HTML/JS + Claude API (MVP), Meta Business API (production)
**Why it's a portfolio piece**: shows FlowstateAI's value prop in miniature. Augment, don't replace.

### 2. SOW Generator (sow-generator) — DONE
**Problem**: writing a Statement of Work takes 1-3 hours and most people skip it
**Solution**: describe project in plain English -> AI generates formatted SOW -> edit inline -> export PDF
**Stack**: HTML/JS + Claude API + html2pdf.js
**Why it's a portfolio piece**: FlowstateAI needs this internally AND it's a client demo

### 3. FAQ Builder (faq-builder) — DONE
**Problem**: every business needs FAQs, nobody writes them
**Solution**: paste service info -> AI generates 10-15 Q&As in brand voice -> export as embeddable HTML
**Stack**: HTML/JS + Claude API + HTML snippet export
**Why it's a portfolio piece**: fastest time-to-value demo (30 seconds), export IS the product

### 4. Photo Workflow OS (photo-workflow-os) — DONE, FLAGSHIP
**Problem**: photography business operations scattered across 5-10 tools
**Solution**: single-page app covering inquiry -> quote -> contract -> shoot prep -> delivery -> follow-up
**Stack**: HTML/JS + Claude API + PDF export
**Why it's a portfolio piece**: end-to-end product thinking, not just a tool. FlowstateAI showcase.

### 5. AI Bullet Journal (ai-bullet-journal) — DONE, FLAGSHIP
**Problem**: no planner combines conversational AI input with visual BuJo-style rendering
**Solution**: chat interface -> AI parses tasks/events/notes/reflections -> renders as visual cards
**Stack**: HTML/JS + Claude API + card-based journal layout
**Why it's a portfolio piece**: this is a product, not a utility. Shows product thinking.

### 6. Meal Planner (meal-planner) — DONE
**Problem**: you have ingredients but no idea what to cook
**Solution**: type what's in your fridge -> 3 meal options with recipes -> Big Green Egg mode for grill specs
**Stack**: HTML/JS + Claude API
**Why it's a portfolio piece**: universally relatable, instant demo, BGE mode is a personality touch

### 7. Agent Pipeline (agent-pipeline) — DONE
**Problem**: no portfolio piece demonstrates multi-agent orchestration end-to-end
**Solution**: 3-agent pipeline (qualifier -> proposal drafter -> reviewer) with retry loop, SSE streaming, SQLite persistence
**Stack**: Python/FastAPI backend + HTML/JS dashboard. Client-side demo fallback for GitHub Pages.
**Why it's a portfolio piece**: proves real agent architecture, not just single-prompt tools. Pydantic data contracts, structured handoffs, observable state.

---

## Mistakes Log

(Add corrections here as they occur. Every correction gets logged. The system learns from its failures.)

- Last name is Haslim, not Haslam. Zero tolerance.
- Em dashes are a recurring issue. Check every output.
- Do not describe what you will build. Build it.
- FlowstateAI is an AI automation consultancy, NOT a marketing agency.

---

## Session Startup Checklist

1. Read this CLAUDE.md completely
2. Check for any .claude/agents/ that apply to the current task
3. Verify git status (branch, uncommitted changes)
4. If Notion MCP is connected, verify Build Vault access
5. Ask Slim which task to work on, or check for open issues

---

## Session Close Protocol

1. Recap what was built and why
2. Commit and push if changes are complete
3. Log to Build Vault if a new artifact was created (confirm with Slim first)
4. Suggest the logical next step
