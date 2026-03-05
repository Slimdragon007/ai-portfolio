# Claude Code Setup Guide — Verified March 4, 2026
## Zero-Error Terminal Commands for Mac

---

## Pre-Flight Check

Before you touch the terminal, confirm these:

- [ ] You have a paid Claude plan (Pro, Max, Team, or Enterprise)
- [ ] You know your Claude login credentials
- [ ] You downloaded the `claude-code-kit` folder from this session
- [ ] You know where you saved it (e.g., ~/Downloads/claude-code-kit)

**Plan note:** Pro ($20/mo) gives you Sonnet by default. Opus requires enabling "Extra Usage" on Pro, or upgrading to Max ($100/mo). Recommendation: start with Sonnet, it handles 90% of the work. Switch to opusplan when you need deep architecture thinking.

---

## Step 1: Open Terminal

Press `Cmd + Space`, type `Terminal`, press `Enter`.

---

## Step 2: Check if Homebrew is installed

```bash
brew --version
```

**If you see a version number** (e.g., "Homebrew 4.x.x"): skip to Step 3.

**If you see "command not found"**: install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After install, Homebrew may tell you to run two commands to add it to your PATH. They will look something like:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Run both if prompted. Then verify:

```bash
brew --version
```

---

## Step 3: Install Claude Code

```bash
brew install --cask claude-code
```

Verify it installed:

```bash
claude --version
```

You should see a version number. If you see "command not found", close Terminal and reopen it, then try again.

---

## Step 4: Move the kit to a permanent location

Pick a home for the project. I recommend:

```bash
mkdir -p ~/projects
cp -r ~/Downloads/claude-code-kit ~/projects/ai-portfolio
```

(Adjust the source path if you saved it somewhere other than Downloads.)

---

## Step 5: Navigate into the project

```bash
cd ~/projects/ai-portfolio
```

Verify the files are there:

```bash
ls -la
```

You should see: CLAUDE.md, QUICKSTART.md, README.md, index.html, setup.sh, .claude/, case-studies/, projects/

---

## Step 6: Make setup script executable and run it

```bash
chmod +x setup.sh
./setup.sh
```

This verifies: Homebrew, Claude Code, Git, and the project structure. It will tell you if anything is missing.

---

## Step 7: Initialize Git

```bash
git init
git add .
git commit -m "infra: initial portfolio with orchestration kit"
```

---

## Step 8: Launch Claude Code

**Option A — Sonnet (default, works on Pro):**
```bash
claude
```

**Option B — Opus Plan Mode (recommended if on Max, or Extra Usage enabled on Pro):**
```bash
claude --model opusplan
```

Opus Plan Mode uses Opus for planning/architecture, then auto-switches to Sonnet for code execution. Best of both worlds.

A browser tab will open. Log in with your Claude account. Follow the prompts. You'll be returned to the terminal, authenticated.

---

## Step 9: Verify CLAUDE.md loaded

Once you're in Claude Code, type:

```
Confirm you've read the CLAUDE.md. List the 4 sub-agents and the 6 project build priorities.
```

Claude should respond with: content-writer, frontend-dev, deployer, notion-sync, and the project list starting with Meta Auto-Responder. If it does, the brain is loaded.

---

## Step 10: Add Notion MCP (recommended)

Inside Claude Code, run:

```
/mcp
```

This shows connected MCP servers. To add Notion:

Exit Claude Code first (type `/exit` or press Ctrl+C), then run:

```bash
claude mcp add notion -- npx -y @notionhq/notion-mcp-server
```

Re-launch Claude Code:

```bash
claude --model opusplan
```

Verify Notion is connected:

```
/mcp
```

You should see the Notion server listed.

---

## Step 11: Create GitHub repo and push

1. Go to github.com/new in your browser
2. Repo name: `ai-portfolio`
3. Set to **Public**
4. Do **NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

Back in Terminal (exit Claude Code first with `/exit`):

```bash
cd ~/projects/ai-portfolio
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/ai-portfolio.git
git branch -M main
git push -u origin main
```

**If you get a permission error on git push:** you may need to set up SSH keys. Run:

```bash
ssh-keygen -t ed25519 -C "michael@flowstateai.com"
```

Press Enter for all defaults. Then:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output. Go to GitHub -> Settings -> SSH and GPG Keys -> New SSH Key. Paste it. Then try the push again.

**Alternative (HTTPS instead of SSH):**

```bash
git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/ai-portfolio.git
git push -u origin main
```

GitHub will prompt for username and a Personal Access Token (not password). Generate one at: github.com -> Settings -> Developer Settings -> Personal Access Tokens -> Generate New Token (classic). Check "repo" scope.

---

## Step 12: Enable GitHub Pages

1. Go to your repo on GitHub
2. Settings (tab at top) -> Pages (left sidebar)
3. Source: "Deploy from a branch"
4. Branch: `main`, folder: `/ (root)`
5. Click Save

Your site will be live in ~60 seconds at:
`https://YOUR_USERNAME.github.io/ai-portfolio`

---

## Step 13: Start building

```bash
cd ~/projects/ai-portfolio
claude --model opusplan
```

First command:

```
Review the CLAUDE.md and the Meta Auto-Responder scaffold in projects/meta-auto-responder/README.md. Then start building the MVP as a single-file HTML application.
```

---

## Model Quick Reference

| Command | What it does | Best for |
|---------|-------------|----------|
| `claude` | Default model (Sonnet) | Daily work, most tasks |
| `claude --model opusplan` | Opus for planning, Sonnet for code | Architecture + building |
| `claude --model opus` | Full Opus | Complex debugging, deep analysis |
| `/model sonnet` | Switch mid-session to Sonnet | Quick tasks, code gen |
| `/model opus` | Switch mid-session to Opus | Hit a hard problem |
| `/model haiku` | Switch mid-session to Haiku | Simple file ops, formatting |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `brew: command not found` | Install Homebrew (Step 2) |
| `claude: command not found` | Close and reopen Terminal, or run `brew install --cask claude-code` |
| Claude Code won't authenticate | Make sure you're on a paid plan (Pro/Max/Team/Enterprise) |
| Opus not available | Enable Extra Usage in your Claude account settings, or use `claude --model sonnet` |
| `git push` permission denied | Set up SSH keys (Step 11) or use HTTPS |
| GitHub Pages not showing | Wait 60 seconds, then check Settings -> Pages. Confirm branch is main, folder is / |
| Notion MCP won't connect | Re-run the mcp add command, restart Claude Code |
| CLAUDE.md not loading | Make sure you `cd` into the project folder BEFORE running `claude` |

---

## Do NOT Use Cowork For This

Cowork is for non-coding knowledge work (file organization, document creation, research). You're building code, pushing to GitHub, and running terminal commands. Claude Code is the correct tool for this project. Cowork and Claude Code use the same underlying architecture, but Claude Code gives you terminal access, git integration, and file system control that Cowork doesn't.
