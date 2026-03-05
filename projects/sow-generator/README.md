# SOW Generator
## Describe the project, get a formatted Statement of Work

### Priority: #2
### Status: Scaffolded, ready to build

---

### The Band-Aid Problem
Writing a Statement of Work takes 1-3 hours. You know what you're going to build, but formatting it into a professional document with deliverables, timelines, payment milestones, and assumptions is tedious. Most freelancers and small agencies either skip the SOW (risky) or reuse a stale template that doesn't fit the project (also risky).

FlowstateAI needs this tool internally AND it's a demo-able product for clients.

### The Fix
Describe the project in plain English -> AI generates a structured SOW with all standard sections -> edit inline -> export as PDF or copy as markdown

### Architecture
```
Project description (conversational input)
    -> Claude API structures into SOW sections:
        - Project overview
        - Scope of work (deliverables list)
        - Timeline with milestones
        - Payment terms
        - Assumptions and exclusions
        - Acceptance criteria
        - Change order process
    -> rendered preview (professional formatting)
    -> inline editing (every section editable)
    -> export: PDF download or markdown copy
```

### Stack
- HTML/CSS/JS (single file for MVP)
- Claude API for SOW generation
- Client-side PDF generation (html2pdf.js or jsPDF)
- Markdown export option

### MVP Scope
- [ ] Text input: "Describe your project in a few sentences"
- [ ] Optional fields: client name, budget range, timeline preference
- [ ] "Generate SOW" button
- [ ] Rendered SOW with all standard sections
- [ ] Each section editable inline
- [ ] PDF export (professional formatting)
- [ ] Markdown copy-to-clipboard
- [ ] 3 example projects to demo: website redesign, AI automation, photography package

### Why This Is a Portfolio Piece
- FlowstateAI uses this internally (it's not hypothetical)
- Shows AI transforming unstructured input into professional business documents
- Directly demonstrates value for agencies, freelancers, consultancies
- PDF export proves production-grade output

---

### Build Sequence (Claude Code)
1. Build project description input UI
2. Wire Claude API for SOW generation
3. Render SOW sections with editable fields
4. Add PDF export
5. Add example project presets
6. Polish formatting to look like a real SOW
7. Deploy as standalone project
8. Add as Case Study 08 in portfolio
