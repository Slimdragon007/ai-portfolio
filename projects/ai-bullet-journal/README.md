# AI Bullet Journal
## Chat-based planner with visual card rendering

### Priority: #5
### Status: Scaffolded, ready to build (flagship product)

---

### The Band-Aid Problem
Traditional planners are static. Digital planners (Notion, Todoist) require manual entry and organization. Bullet journals are beautiful but time-consuming to maintain. Nobody has combined the conversational ease of talking to AI with the visual satisfaction of a well-organized journal.

The gap: there's no planner where you can say "I need to meal prep Sunday, Ellie has soccer at 3, and I have a pitch Monday" and get back a rendered visual layout, not a text list.

### The Fix
Chat interface where you talk naturally about your day/week -> AI renders structured visual entries (cards, blocks, timelines) -> persistent journal view that builds over time -> daily and weekly visual layouts

### Architecture
```
Chat input (natural language)
    -> Claude API parses intent:
        - Task (actionable, has a deadline or context)
        - Event (time-bound, goes on calendar view)
        - Note (capture for later, no action needed)
        - Reflection (journal entry, personal)
        - Goal (longer-term, connects to weekly/monthly view)
    -> renders as visual card in journal view:
        - Tasks: checkbox card with priority dot
        - Events: timeline block with time
        - Notes: sticky-note style card
        - Reflections: journal entry with date stamp
        - Goals: progress tracker card
    -> journal view: daily spread, weekly spread, monthly overview
    -> chat history stays in left panel, journal builds in right panel
```

### Stack
- React (component-based rendering for card types)
- Claude API for natural language parsing and card generation
- In-memory state for MVP
- CSS Grid/Flexbox for journal layout
- Possible: drag-to-reorder cards within a day

### MVP Scope

**Chat Panel (left side):**
- [ ] Chat input with send button
- [ ] Message history (user messages + AI confirmations)
- [ ] AI confirms what it parsed: "Added: Soccer at 3pm, tagged as Event"
- [ ] Quick commands: "/today", "/week", "/goals"

**Journal Panel (right side):**
- [ ] Daily view: today's cards rendered in a visual spread
- [ ] Card types with distinct visual styles:
  - Task cards (checkbox, priority color, context tag)
  - Event cards (time block, duration, location)
  - Note cards (yellow sticky-note style)
  - Reflection cards (journal-style, italic text)
  - Goal cards (progress bar, target date)
- [ ] Click card to edit
- [ ] Check off tasks

**Navigation:**
- [ ] Day picker (previous/next day)
- [ ] Week view (7-day grid with cards)
- [ ] Toggle between chat-focused and journal-focused layout

### Design Direction
- BuJo-inspired aesthetic: clean, slightly analog feel
- Card-based layout (not a list)
- Muted color palette with color-coded card types
- Handwriting-style font option for reflections
- Satisfying micro-animations on card creation

### Why This Is a Portfolio Piece
- This is a product, not a utility. Shows product thinking, not just technical skill.
- The chat -> visual rendering pattern is the core of human-AI collaboration
- Combines conversational AI with real UI/UX design
- Personal tool Slim actually uses (dogfooding)
- Potential standalone product

---

### Build Sequence (Claude Code)
1. Build split-panel layout (chat left, journal right)
2. Wire chat input to Claude API
3. Build card type components (task, event, note, reflection, goal)
4. Render parsed entries as cards in journal view
5. Add day navigation and week view
6. Add card editing and task completion
7. Polish BuJo aesthetic
8. Deploy as standalone project
9. Add as Case Study 11 in portfolio
