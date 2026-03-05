# Photo Workflow OS
## End-to-end photography business operating system

### Priority: #4
### Status: Scaffolded, ready to build (flagship project)

---

### The Band-Aid Problem
Photography business operations are scattered across 5-10 tools: inquiries come through email and Instagram DMs, quotes live in Google Docs, contracts are PDFs emailed back and forth, shot lists are in Notes app, delivery is via gallery links with no follow-up system. Every photographer reinvents this wheel. Most drop balls between steps.

### The Fix
A single-page app that walks a photographer through the entire client lifecycle: inquiry -> quote -> contract -> shoot prep -> delivery -> follow-up. AI assists at every step.

### Architecture
```
Pipeline view (kanban-style stages)
    -> Inquiry: log client name, event type, date, source
    -> Quote: AI generates pricing based on event type + hours + add-ons
    -> Contract: AI drafts terms from quote details
    -> Shoot Prep: AI generates shot list from event type + venue + client preferences
    -> Delivery: AI drafts gallery delivery email with review request
    -> Follow-up: automated thank-you + review request + referral ask timing

Each stage:
    -> AI-assisted content generation
    -> editable output
    -> status tracking per client
    -> move to next stage with one click
```

### Stack
- React (single page app) or HTML/CSS/JS
- Claude API for content generation at each stage
- In-memory client storage for MVP (no backend)
- Optional: localStorage for session persistence
- PDF export for quotes and contracts

### MVP Scope

**Pipeline View:**
- [ ] Kanban board with 6 columns (Inquiry -> Quote -> Contract -> Prep -> Deliver -> Complete)
- [ ] Add new client card
- [ ] Drag cards between stages

**Inquiry Stage:**
- [ ] Client info form: name, email, event type, date, venue, how they found you
- [ ] Auto-categorize: wedding, portrait, corporate, event

**Quote Stage:**
- [ ] Input: hours, travel, editing scope, add-ons
- [ ] AI generates line-item quote with professional formatting
- [ ] Edit line items
- [ ] PDF export

**Contract Stage:**
- [ ] AI drafts contract terms from quote (cancellation, delivery timeline, usage rights)
- [ ] Editable template
- [ ] PDF export

**Shoot Prep Stage:**
- [ ] Input: event type, venue, time of day, client preferences
- [ ] AI generates detailed shot list with timing
- [ ] Editable checklist format

**Delivery Stage:**
- [ ] Input: client name, event, gallery link
- [ ] AI drafts delivery email (warm, sets expectations, includes review request)
- [ ] Copy-to-clipboard

**Follow-up Stage:**
- [ ] AI suggests follow-up timing (thank you at 1 week, review request at 2 weeks, referral ask at 1 month)
- [ ] Draft messages for each touchpoint

### Why This Is a Portfolio Piece
- This is the biggest build in the portfolio. Shows end-to-end product thinking.
- AI isn't the product, it's the engine inside a real workflow tool.
- Proves FlowstateAI can take a client from "I have a messy process" to "I have an operating system."
- Slim uses this himself for Michael Haslim Photo (dogfooding)
- Potential standalone SaaS product if demand validates

### FlowstateAI Client Pitch
"We don't just build you a chatbot. We map your entire client lifecycle, identify where AI accelerates each step, and deliver an operating system that runs your business the way you'd run it if you had 3 extra hours a day."

---

### Build Sequence (Claude Code)
1. Build pipeline/kanban UI shell
2. Add client card creation and stage movement
3. Wire Quote stage (AI pricing generation)
4. Wire Prep stage (AI shot list generation)
5. Wire Delivery stage (AI email drafting)
6. Add PDF export for quotes and contracts
7. Polish responsive design
8. Deploy as standalone project
9. Add as Case Study 10 in portfolio
