# FAQ Builder
## Paste your business info, get a ready-to-deploy FAQ section

### Priority: #3
### Status: Scaffolded, ready to build

---

### The Band-Aid Problem
Every business website needs an FAQ section. Nobody writes one because it requires anticipating questions you've already answered 500 times verbally but never documented. When someone finally writes FAQs, they miss obvious questions and the answers sound stiff.

### The Fix
Paste your website copy, service descriptions, or just ramble about what you do -> AI generates 10-15 FAQs in your brand voice -> edit, reorder, export as HTML ready to drop on your site

### Architecture
```
Business info input (paste text, URL, or free-form description)
    -> Claude API analyzes for:
        - Common customer questions (inferred from services)
        - Pricing/availability questions
        - Process/logistics questions
        - Trust/credibility questions
    -> generates Q&A pairs in brand voice
    -> rendered as accordion-style FAQ preview
    -> drag-to-reorder
    -> export: embeddable HTML snippet or markdown
```

### Stack
- HTML/CSS/JS (single file)
- Claude API for FAQ generation
- Drag-and-drop reordering (native HTML5 drag API)
- Code snippet export (copy embeddable HTML)

### MVP Scope
- [ ] Text input: paste business description or service info
- [ ] Optional: brand tone selector (friendly, professional, casual)
- [ ] "Generate FAQs" button
- [ ] Rendered accordion-style FAQ preview
- [ ] Edit any Q or A inline
- [ ] Delete or reorder entries
- [ ] Export: copy as embeddable HTML with accordion CSS included
- [ ] Export: copy as markdown
- [ ] Regenerate individual Q&As

### Why This Is a Portfolio Piece
- Fastest time-to-value of any project in the portfolio (paste -> done in 30 seconds)
- The export IS the product (embeddable HTML, not just text)
- Shows AI generating production-ready web content, not just drafts
- Every small business client can immediately use this

---

### Build Sequence (Claude Code)
1. Build text input + tone selector UI
2. Wire Claude API for FAQ generation
3. Render accordion preview
4. Add inline editing and reorder
5. Build HTML snippet export (includes CSS)
6. Add markdown export
7. Deploy as standalone project
8. Add as Case Study 09 in portfolio
