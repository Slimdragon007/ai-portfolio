# QUICKSTART: Get This Live in 10 Minutes

You're at your Mac. Here's exactly what to do.

---

## Step 1: Open Terminal (30 seconds)

Press `Cmd + Space`, type `Terminal`, hit Enter.

---

## Step 2: Navigate to this folder (10 seconds)

If you downloaded this kit to Downloads:
```bash
cd ~/Downloads/claude-code-kit
```

Or wherever you saved it:
```bash
cd /path/to/claude-code-kit
```

---

## Step 3: Run setup (2 minutes)

```bash
chmod +x setup.sh
./setup.sh
```

This checks for Homebrew, installs Claude Code (via Homebrew cask), verifies Git, and confirms the project structure.

---

## Step 4: Authenticate Claude Code (1 minute)

```bash
claude
```

A browser tab opens. Log in with your Claude account (Pro or Max required). Follow the prompts. Done.

---

## Step 5: Add Notion MCP (30 seconds, optional but recommended)

```bash
claude mcp add notion-mcp https://mcp.notion.com/mcp
```

This connects Claude Code to your Notion workspace so the notion-sync agent can log to Build Vault.

---

## Step 6: Create GitHub repo (2 minutes)

1. Go to github.com/new
2. Repo name: `ai-portfolio`
3. Set to Public
4. Do NOT initialize with README (we have one)
5. Create repository

Then in Terminal:
```bash
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/ai-portfolio.git
git add .
git commit -m "infra: initial portfolio deployment"
git push -u origin main
```

---

## Step 7: Enable GitHub Pages (1 minute)

1. Go to your repo on GitHub
2. Settings -> Pages
3. Source: Deploy from a branch
4. Branch: main, folder: / (root)
5. Save

Your site will be live at: `YOUR_USERNAME.github.io/ai-portfolio`

---

## Step 8: Start Building (ongoing)

```bash
claude
```

Claude Code reads CLAUDE.md automatically. It knows:
- The project structure
- All four sub-agents (content-writer, frontend-dev, deployer, notion-sync)
- The design system
- The Band-Aid project ideas
- Your rules and preferences

Try these first commands:

```
"Review the current portfolio site and suggest improvements"
"Build the Receipt Snap project from the scaffold in projects/receipt-snap/"
"Add a new case study for the orchestration kit itself"
"Push the current state to GitHub"
```

---

## What's In This Kit

| File/Folder | Purpose |
|-------------|---------|
| CLAUDE.md | Orchestration brain, Claude Code reads this first |
| .claude/agents/ | 4 sub-agents for task delegation |
| index.html | GitHub Pages portfolio site (dark theme, expandable cards) |
| README.md | Repo landing page with case study table |
| case-studies/ | 6 markdown case studies |
| projects/ | 4 Band-Aid project scaffolds (ready to build) |
| setup.sh | Mac setup script |
| QUICKSTART.md | This file |

---

## Notion References (already in CLAUDE.md)

- Context Hub: https://www.notion.so/31916230665c81229894f14fc1e14d9f
- Build Vault: https://www.notion.so/afa3538c22c24a098bbf1b068a322cf6
- Portfolio Page: https://www.notion.so/31916230665c810e8f0fcc50cb032d89

---

## If Something Breaks

- Claude Code won't install? Try: `brew update && brew install --cask claude-code`
- Git push rejected? Make sure the GitHub repo exists and is empty (no initial README)
- Notion MCP won't connect? Re-run: `claude mcp add notion-mcp https://mcp.notion.com/mcp`
- Site not showing on GitHub Pages? Check Settings -> Pages, confirm branch is main and folder is /

---

This kit was built in a single Claude session using the 4D Framework.
Define -> Delegate -> Discern -> Diligence.
The kit itself is Case Study 07.
