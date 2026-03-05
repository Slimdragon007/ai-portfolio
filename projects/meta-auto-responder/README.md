# Meta Auto-Responder
## AI-drafted replies for Facebook and Instagram business DMs

### Priority: #1
### Status: Scaffolded, ready to build

---

### The Band-Aid Problem
Small business owners get DMs on Facebook and Instagram all day. "What are your hours?" "Do you do custom orders?" "How much for [service]?" They either respond 4 hours late (losing the lead), copy-paste a generic reply (feels robotic), or hire someone to monitor DMs full-time (expensive).

There's no middle ground between "ignore it" and "hire a person."

### The Fix
Connect to business's FAQ/service info -> AI monitors incoming DMs -> drafts contextual, on-brand replies -> owner reviews and sends with one tap (human-in-the-loop, not full automation)

### Architecture
```
Business context input (services, pricing, hours, tone, FAQs)
    -> incoming DM (text input for MVP, Meta API for production)
    -> Claude API classifies intent:
        - Pricing inquiry
        - Availability/scheduling
        - Service question
        - Complaint/concern
        - General inquiry
    -> draft response matched to:
        - intent category
        - business context
        - brand tone (friendly, professional, casual)
    -> owner preview + edit
    -> send (copy-to-clipboard for MVP, API integration for production)
```

### Technical Approach

**MVP (portfolio demo, no Meta API needed):**
- HTML/CSS/JS single page
- Left panel: "incoming DM" text input (simulates receiving a message)
- Right panel: AI-drafted response with intent tag
- Top: business context setup (paste your services, hours, tone preference)
- Claude API for response generation
- Copy-to-clipboard for the reply

**Production version (FlowstateAI client engagement):**
- Meta Business API integration (Messenger + Instagram DM)
- Webhook listener for incoming messages
- Queue system: AI drafts pile up for owner review
- Dashboard: inbox view with draft responses, one-click approve/edit/send
- Analytics: response time improvement, lead conversion tracking

### MVP Scope
- [ ] Business context setup form (services, hours, pricing, tone)
- [ ] "Incoming DM" simulator (text input)
- [ ] Intent classification display (what type of message is this?)
- [ ] AI-drafted response with brand tone matching
- [ ] Edit field (owner tweaks before sending)
- [ ] Copy-to-clipboard
- [ ] Response history log
- [ ] 3 preset business types to demo: restaurant, salon, home services

### Prompt Engineering
```
You are a customer service assistant for a small business.

Business context:
{business_name}
{services}
{hours}
{pricing}
{tone: friendly | professional | casual}

A customer sent this DM:
"{incoming_message}"

1. Classify the intent: pricing | availability | service_question | complaint | general
2. Draft a response that:
   - Answers their specific question using the business context
   - Matches the brand tone
   - Is concise (under 3 sentences for simple questions)
   - Includes a call-to-action when appropriate (book now, call us, visit website)
   - Feels human, not like a chatbot

Return JSON:
{
  "intent": "...",
  "confidence": 0.0-1.0,
  "draft_response": "...",
  "suggested_cta": "..."
}
```

### Why This Is a Portfolio Piece
- Solves a real, daily problem for every small business on Meta
- Shows the "augment, don't replace" philosophy (owner reviews before sending)
- MVP is a demo anyone can try without API setup
- Production path shows FlowstateAI can take this from prototype to deployed product
- Focused on Meta platforms (Facebook and Instagram DMs)

### FlowstateAI Client Pitch
"Your team spends 2 hours a day answering the same 10 DM questions. We build an AI layer that drafts responses in your brand voice, you approve with one click. Response time drops from 4 hours to 10 minutes. No bots, no generic replies, just faster humans."

---

### Build Sequence (Claude Code)
1. Build the business context setup UI
2. Add DM input simulator
3. Wire Claude API for intent classification + response drafting
4. Add response preview/edit/copy flow
5. Add preset demo businesses
6. Polish UI to match portfolio design system
7. Deploy as standalone GitHub Pages project
8. Add as Case Study 07 in portfolio
