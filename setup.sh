#!/bin/bash
# ============================================
# AI Portfolio Setup Script for Mac
# Owner: Michael Haslim (Slim)
# Run this once to set up Claude Code and
# initialize the portfolio project.
# ============================================

set -e

echo ""
echo "=========================================="
echo " AI Portfolio Setup"
echo " Michael Haslim | FlowstateAI"
echo "=========================================="
echo ""

# ── Step 1: Check for Homebrew ──
echo "[1/6] Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "  Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "  Homebrew installed."
else
    echo "  Homebrew found."
fi

# ── Step 2: Install Claude Code ──
echo ""
echo "[2/6] Installing Claude Code..."
if command -v claude &> /dev/null; then
    echo "  Claude Code already installed: $(claude --version 2>/dev/null || echo 'version check skipped')"
else
    echo "  Installing via Homebrew..."
    brew install --cask claude-code
    echo "  Claude Code installed."
fi

# ── Step 3: Install Git (if needed) ──
echo ""
echo "[3/6] Checking Git..."
if ! command -v git &> /dev/null; then
    echo "  Git not found. Installing..."
    brew install git
    echo "  Git installed."
else
    echo "  Git found: $(git --version)"
fi

# ── Step 4: Initialize Git repo ──
echo ""
echo "[4/6] Initializing Git repository..."
if [ -d ".git" ]; then
    echo "  Git repo already initialized."
else
    git init
    echo "  Git repo initialized."
fi

# ── Step 5: Configure git (if not set) ──
echo ""
echo "[5/6] Checking Git config..."
GIT_NAME=$(git config --global user.name 2>/dev/null || echo "")
GIT_EMAIL=$(git config --global user.email 2>/dev/null || echo "")

if [ -z "$GIT_NAME" ]; then
    echo "  Setting Git name..."
    git config --global user.name "Michael Haslim"
fi

if [ -z "$GIT_EMAIL" ]; then
    echo "  Setting Git email..."
    git config --global user.email "michael@flowstateai.com"
fi

echo "  Git configured as: $(git config --global user.name) <$(git config --global user.email)>"

# ── Step 6: Verify structure ──
echo ""
echo "[6/6] Verifying project structure..."

REQUIRED_FILES=(
    "CLAUDE.md"
    "index.html"
    "README.md"
    ".nojekyll"
    ".claude/agents/content-writer.md"
    ".claude/agents/frontend-dev.md"
    ".claude/agents/deployer.md"
    ".claude/agents/notion-sync.md"
)

ALL_GOOD=true
for f in "${REQUIRED_FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "  [ok] $f"
    else
        echo "  [MISSING] $f"
        ALL_GOOD=false
    fi
done

if [ "$ALL_GOOD" = true ]; then
    echo ""
    echo "=========================================="
    echo " Setup complete."
    echo "=========================================="
    echo ""
    echo " Next steps:"
    echo ""
    echo " 1. Authenticate Claude Code:"
    echo "    $ claude"
    echo "    (follow browser prompts to log in)"
    echo ""
    echo " 2. Add Notion MCP (optional but recommended):"
    echo "    $ claude mcp add notion-mcp https://mcp.notion.com/mcp"
    echo ""
    echo " 3. Create GitHub repo:"
    echo "    Go to github.com/new"
    echo "    Repo name: ai-portfolio"
    echo "    Public repo"
    echo "    Do NOT add README (we have one)"
    echo ""
    echo " 4. Connect remote and push:"
    echo "    $ git remote add origin git@github.com:YOUR_USERNAME/ai-portfolio.git"
    echo "    $ git add ."
    echo "    $ git commit -m 'infra: initial portfolio deployment'"
    echo "    $ git push -u origin main"
    echo ""
    echo " 5. Enable GitHub Pages:"
    echo "    Settings -> Pages -> Source: main branch, root (/)"
    echo ""
    echo " 6. Start building with Claude Code:"
    echo "    $ claude"
    echo "    Claude will read CLAUDE.md automatically."
    echo ""
else
    echo ""
    echo "  Some files are missing. Check the project structure."
    echo "  CLAUDE.md should be in the project root."
fi
