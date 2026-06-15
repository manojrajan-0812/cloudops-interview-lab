#!/usr/bin/env bash
# CloudOps Interview Lab — one-shot setup script
# Works on macOS. Safe to re-run: skips anything already installed.
#
# Usage (from inside the cloned repo):
#   ./setup.sh
#
# Usage (fresh machine, repo not yet cloned):
#   curl -fsSL https://raw.githubusercontent.com/manojrajan-0812/cloudops-interview-lab/main/setup.sh -o setup.sh
#   chmod +x setup.sh && ./setup.sh

set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

ok()      { echo -e "${GREEN}  ✅ $*${NC}"; }
skip()    { echo -e "${GREEN}  ✔  $*${NC}"; }
install() { echo -e "${YELLOW}  ➜  $*${NC}"; }
header()  { echo -e "\n${BLUE}── $* ─────────────────────────────────────────${NC}"; }
fail()    { echo -e "${RED}  ❌ $*${NC}"; exit 1; }

REPO_URL="https://github.com/manojrajan-0812/cloudops-interview-lab.git"
REPO_DIR="cloudops-interview-lab"

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║      CloudOps Interview Lab — Setup Script            ║"
echo "║      github.com/manojrajan-0812/cloudops-interview-lab║"
echo "╚═══════════════════════════════════════════════════════╝"

# ── Step 1: Homebrew ─────────────────────────────────────────────────────
header "Step 1 — Homebrew"
if command -v brew &>/dev/null; then
    skip "Homebrew already installed ($(brew --version | head -1))"
else
    install "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ok "Homebrew installed"
fi

# ── Step 2: Python 3.9+ ──────────────────────────────────────────────────
header "Step 2 — Python 3.9+"
if command -v python3 &>/dev/null && python3 -c "import sys; assert sys.version_info >= (3, 9)" 2>/dev/null; then
    skip "Python $(python3 --version) already installed"
else
    install "Installing Python 3.11 via Homebrew..."
    brew install python@3.11
    ok "Python 3.11 installed"
fi

# ── Step 3: Git ───────────────────────────────────────────────────────────
header "Step 3 — Git"
if command -v git &>/dev/null; then
    skip "Git already installed ($(git --version))"
else
    install "Installing git via Homebrew..."
    brew install git
    ok "Git installed"
fi

# ── Step 4: SQLite3 ───────────────────────────────────────────────────────
header "Step 4 — SQLite3"
if command -v sqlite3 &>/dev/null; then
    skip "SQLite3 already installed ($(sqlite3 --version | cut -d' ' -f1))"
else
    install "Installing sqlite3 via Homebrew..."
    brew install sqlite
    ok "SQLite3 installed"
fi

# ── Step 5: Claude Code ───────────────────────────────────────────────────
header "Step 5 — Claude Code"
if command -v claude &>/dev/null; then
    skip "Claude Code already installed"
else
    install "Installing Claude Code via Homebrew..."
    brew install claude
    ok "Claude Code installed"
fi
echo -e "  ${YELLOW}ℹ  Sign in with: claude${NC}"
echo -e "  ${YELLOW}ℹ  Requires an Anthropic account (claude.ai)${NC}"

# ── Step 6: Clone repository ──────────────────────────────────────────────
header "Step 6 — Repository"
if [[ -f "./interview" && -d "./problems" ]]; then
    skip "Already inside the cloudops-interview-lab repo"
    REPO_ROOT="$(pwd)"
elif [[ -d "./$REPO_DIR" ]]; then
    skip "Repo already cloned at ./$REPO_DIR"
    cd "$REPO_DIR"
    REPO_ROOT="$(pwd)"
else
    install "Cloning cloudops-interview-lab..."
    git clone "$REPO_URL"
    ok "Cloned to ./$REPO_DIR"
    cd "$REPO_DIR"
    REPO_ROOT="$(pwd)"
fi

# ── Step 7: Python dependencies ───────────────────────────────────────────
header "Step 7 — Python dependencies"
install "Installing pyyaml flask structlog prometheus-client..."
pip3 install pyyaml flask structlog prometheus-client --quiet
ok "Python dependencies installed"

# ── Step 8: Runner permissions ────────────────────────────────────────────
header "Step 8 — Runner permissions"
if [[ -x "./interview" ]]; then
    skip "interview runner is already executable"
else
    chmod +x interview
    ok "interview runner made executable"
fi

# ── Verification ──────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo "  Verifying setup..."
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

./interview reset
echo ""
./interview list

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Setup complete — this laptop is ready for interviews!${NC}"
echo ""
echo "  Repo location : ${REPO_ROOT}"
echo ""
echo "  To start an interview:"
echo "    cd ${REPO_ROOT}"
echo "    ./interview start --level mid"
echo "    ./interview start --level senior"
echo ""
echo "  To preview all problems:"
echo "    ./interview list"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
