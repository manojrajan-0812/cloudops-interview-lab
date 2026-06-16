# Troubleshooting Guide

Common problems and fixes for the CloudOps Interview Lab.

---

## Setup Issues

### `./interview` — Permission denied

```
bash: ./interview: Permission denied
```

**Fix:**
```bash
chmod +x interview
```

---

### `ModuleNotFoundError: No module named 'yaml'` or similar

```
ModuleNotFoundError: No module named 'yaml'
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'structlog'
```

**Fix:**
```bash
pip3 install pyyaml flask structlog prometheus-client
```

---

### Python version too old

```
SyntaxError: f-string expression part cannot include a backslash
```

The runner requires Python 3.9+. Check your version:
```bash
python3 --version
```

**Fix:**
```bash
brew install python@3.11
```

Then verify `python3` points to 3.11:
```bash
python3 --version   # should show 3.11.x
```

---

### `brew: command not found`

Homebrew is not installed.

**Fix:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### `claude: command not found`

Claude Code is not installed.

**Fix:**
```bash
brew install claude
```

Then sign in:
```bash
claude
```

---

## Session Issues

### `./interview start` — Working tree is not clean

```
❌ Working tree is not clean. Run './interview reset' first.
```

A previous session left modified files in the working tree. This happens when a session ends without resetting, or when someone ran `git restore` during a session.

**Fix:**
```bash
./interview reset
```

---

### `./interview start` — No name prompt appears, session starts with "Candidate"

The name prompt was bypassed (e.g. the name was piped in via `echo "name" | ./interview start`). This is expected behaviour when automating. In a live interview, run:
```bash
./interview start --level mid
```
and type the candidate name when prompted.

---

### `./interview validate` — No active interview session

```
❌ No active interview session. Run './interview start' first.
```

The `.interview-state` file is missing — either reset was run, or the session file was deleted.

**Fix:** Start a new session:
```bash
./interview start --level mid
```

---

### `./interview validate` — Validator error / module not found

```
❌ Validator error: No module named 'tools.validators.k_001'
```

The runner is being invoked from the wrong directory.

**Fix:** Always run from the repo root:
```bash
cd /path/to/cloudops-interview-lab
./interview validate
```

---

### `./interview validate` — K-005 health check fails with prometheus error

```
ValueError: Duplicated timeseries in CollectorRegistry
```

This was a known bug (now fixed) caused by `importlib.reload` re-registering Prometheus metrics. Make sure you have the latest version:

```bash
git pull origin main
```

---

### `git restore .` passes validation (jailbreak)

A candidate ran `git restore .` and the validator passed without them fixing anything. This was a known design flaw where `git restore .` restored the correct baseline from HEAD, bypassing the need to fix anything.

This is fixed in the current version: `./interview start` now commits the broken state to HEAD, so `git restore .` restores the broken files instead.

Make sure you have the latest version:
```bash
git pull origin main
./interview reset
```

---

### `./interview reset` — does not return to clean baseline

If reset leaves unexpected files or a dirty working tree:

```bash
git log --oneline | head -5
```

Look for commits named `_broken_state_*` — these are temporary commits added during a session. Reset should remove them automatically. If they remain:

```bash
# Find the last real commit (before any _broken_state_ commits)
git log --oneline | grep -v "_broken_state_"
# Reset to it manually
git reset --hard <SHA>
git clean -fdx
```

---

## Interview Flow Issues

### Candidate finishes in under 2 minutes — suspiciously fast

Check if the candidate:
1. Ran `git restore .` to get answers from the git baseline — upgrade to the latest version which closes this
2. Opened `interviewer/solutions/` — the honour system applies; probe the follow-up questions harder
3. Genuinely solved it — ask them to explain the root cause live

---

### Validator passes but candidate's fix looks wrong

Validators check for the correct end state, not how the candidate got there. If the validator passes:
- The fix is functionally correct (the validator is correct)
- The candidate may have used a different but valid approach — refer to `interviewer/solutions/{ID}.md` for "alternative acceptable fixes"

---

### `./interview next` — refuses to advance

```
❌ {ID} has not been validated yet.
```

The current problem must pass validation before advancing. If you need to skip for operational reasons (interviewer override):

```bash
./interview next --force
```

---

### All 5 problems show the same file to fix

This can happen if multiple problems in the assigned queue affect the same file. Each problem's fixture overwrites the previous one as you advance. This is expected — focus on the specific symptom described in the current problem statement, not all visible issues in the file.

---

## Common Mistakes by Candidates

These are not bugs — document them here so interviewers know what to watch for.

| Behaviour | What it means |
|---|---|
| Runs `./interview validate` without changing any file | Did not read the problem statement carefully |
| Fixes a different file than the one with the bug | Misdiagnosed the root cause |
| Passes validation but can't explain the fix | May have copied from `interviewer/solutions/` |
| Asks Claude "fix this" with no context | Poor AI usage — flag in scoring |
| Removes a probe or resource entirely to "fix" it | Wrong fix — some validators explicitly reject this |

---

## Getting Help

If you encounter an issue not covered here:

1. Check the [README](../README.md) for setup and usage reference
2. Check the [Interviewer Guide](../interviewer/interviewer-guide.md) for session-specific questions
3. Open an issue or PR at [github.com/manojrajan-0812/cloudops-interview-lab](https://github.com/manojrajan-0812/cloudops-interview-lab)
