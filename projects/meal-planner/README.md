# Meal Planner
## What's in your fridge -> what's for dinner (with Big Green Egg mode)

### Priority: #6
### Status: Scaffolded, ready to build

---

### The Band-Aid Problem
It's 5:30pm. You open the fridge. You see chicken thighs, bell peppers, and half an onion. You Google "chicken thigh recipes" and get 40 results that require 12 ingredients you don't have. You order DoorDash. Again.

### The Fix
Type what's in your fridge -> AI generates 3 meal options using only what you have -> each with a recipe, cook time, and difficulty rating -> Big Green Egg mode suggests smoke/grill temp, wood type, and cook method

### Architecture
```
Ingredient input (free text: "chicken thighs, bell peppers, onion, rice, soy sauce")
    -> Claude API generates 3 meal options:
        - Meal name
        - Ingredients used (from your list)
        - Optional add (1-2 items that would elevate it)
        - Recipe steps
        - Cook time + difficulty
        - Dietary tags (if applicable)
    -> BGE Mode toggle:
        - Suggested grill/smoke temp
        - Wood pairing (hickory, cherry, mesquite, etc.)
        - Direct vs. indirect heat
        - Cook method notes

    -> rendered as meal cards
    -> click to expand full recipe
    -> optional: save favorites
```

### Stack
- HTML/CSS/JS (single file)
- Claude API for meal generation
- Toggle for Big Green Egg mode
- Clean card-based recipe display

### MVP Scope
- [ ] Ingredient text input (comma-separated or free text)
- [ ] Dietary preference selector (none, keto, vegetarian, dairy-free)
- [ ] "What Can I Make?" button
- [ ] 3 meal cards with name, cook time, difficulty
- [ ] Expand card for full recipe
- [ ] Big Green Egg toggle: adds grill temp, wood, cook method to each recipe
- [ ] "Try Again" button for different suggestions

### Why This Is a Portfolio Piece
- Universally relatable problem (everyone eats)
- Quick demo: type 5 ingredients, get dinner ideas in 3 seconds
- BGE mode is a personality touch that makes it memorable
- Shows AI generating structured, actionable content from minimal input
- Low barrier to try (no setup, no account, just type and go)

---

### Build Sequence (Claude Code)
1. Build ingredient input + dietary selector UI
2. Wire Claude API for meal generation
3. Render meal cards with expand/collapse
4. Add Big Green Egg mode toggle
5. Polish card design
6. Deploy as standalone project
7. Add as Case Study 12 in portfolio
