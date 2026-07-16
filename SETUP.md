# Email Inbox Agent Setup Guide

## Overview

This agent triages your Gmail inbox using AI:
- Reads unread emails (last 12 hours by default)
- Creates **summaries** of each email
- Classifies them (IGNORE, REPLY, SUSPICIOUS, **ARCHIVE**, **MOVE_TO_FOLDER**)
- **Archives** low-priority emails (newsletters, promotions)
- **Moves** emails to proper folders to declutter inbox
- Applies topic labels (Personal, Finance, Sales, etc.)
- Creates draft replies for action-required emails
- **Never auto-sends** - creates drafts only

---

## New Features (v2.0)

### Actions
| Action | Description |
|--------|-------------|
| **IGNORE** | Leave in inbox, no action needed |
| **REPLY** | Create draft reply |
| **SUSPICIOUS** | Flag for manual review |
| **ARCHIVE** | Move out of inbox (newsletters, promotions) |
| **MOVE_TO_FOLDER** | Organize into specific folder |

### What It Does Now
1. **Summarizes** - Creates brief summary of each email
2. **Archives** - Removes low-priority emails from inbox
3. **Organizes** - Moves emails to labeled folders
4. **Labels** - Applies category labels
5. **Drafts** - Creates reply drafts when needed

---

## Requirements

1. **Ollama** running on Windows
2. **Gmail OAuth credentials** (one-time setup)
3. Conda environment

---

## Starting Ollama (Windows)

If Ollama isn't running, open PowerShell:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
Start-Process ollama
```

---

## Running the Agent

### Step 1: Activate environment

In WSL terminal:

```bash
source ~/miniconda/bin/activate email-agent
cd /mnt/c/Users/ozmnf/OMReseach/Email-Inbox-Agent---OMF
```

### Step 2: Run the agent

```bash
python -m app.main
```

### First Run (OAuth Setup)

On first run, it will:
1. Show a URL to authorize
2. Open browser (or copy URL manually)
3. Sign in with Google
4. Grant permissions
5. Token saved automatically

If browser doesn't open automatically, copy the URL from terminal and open manually in Windows browser.

---

## Configuration

Edit `.env` file to customize:

### Model Settings (using Ollama)
```env
OPENAI_API_KEY="ollama"
OPENAI_BASE_URL="http://172.22.240.1:11434/v1"
OPENAI_MODEL_TRIAGE="llama3"
OPENAI_MODEL_DRAFT="llama3"
```

### Runtime Settings
```env
MAX_EMAILS_PER_RUN="10"
MAX_EMAIL_AGE_HOURS="12"
INCLUDE_READ_INBOX_EMAILS="false"
```

### Label Names (match your Gmail labels)
```env
LABEL_PERSONAL_DIRECT="Personal & Direct"
LABEL_FINANCE="Finance"
LABEL_SALES_OUTREACH="Sales & Outreach"
LABEL_EVENTS_CALENDAR="Events & Calendar"
LABEL_NEWSLETTERS="Newsletters"
LABEL_SECURITY_ADMIN="Security & Admin"
LABEL_PROFESSIONAL_NETWORK="Professional Network"
LABEL_RECEIPTS_BILLING="Receipts & Billing"
LABEL_SAAS_TOOLS="SaaS & Tools"
LABEL_ACTION_REQUIRED="Action Required"
```

---

## Optional: Using a Different Model

You can switch to a more powerful model. In `.env`:

```env
OPENAI_MODEL_TRIAGE="deepseek-r1"
OPENAI_MODEL_DRAFT="deepseek-r1"
```

Make sure the model is downloaded in Ollama:
```bash
curl http://172.22.240.1:11434/api/tags
```

---

## Running Continuously (Schedule)

### Windows Task Scheduler

Enable (every 2 minutes):
```powershell
.\scripts\enable_scheduler_windows.ps1 -EveryMinutes 2
```

Disable:
```powershell
.\scripts\disable_scheduler_windows.ps1
```

### macOS/Linux

Enable (every 2 minutes):
```bash
bash scripts/enable_scheduler_mac.sh 2
```

Disable:
```bash
bash scripts/enable_scheduler_mac.sh disable
```

---

## Testing with Fake Emails

Generate test emails to see the agent in action:

```bash
source ~/miniconda/bin/activate email-agent
cd /mnt/c/Users/ozmnf/OMReseach/Email-Inbox-Agent---OMF
python -m scripts.send_stress_test_emails
```

This sends 15 fake emails to your inbox for the agent to classify.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `source ~/miniconda/bin/activate email-agent` | Activate environment |
| `python -m app.main` | Run the agent |
| `python -m app.cleanup_labels --dry-run` | Preview label cleanup |
| `python -m app.cleanup_labels` | Remove legacy labels |
| `python -m scripts.send_stress_test_emails` | Generate test emails |

---

## Troubleshooting

### "Request timed out" - Ollama not accessible
Restart Ollama on Windows:
```powershell
Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process
$env:OLLAMA_HOST="0.0.0.0:11434"
Start-Process ollama
```

### "Token expired" or "Invalid credentials"
Delete `token.json` and run `python -m app.main` again to re-authenticate.

### "No emails found"
Check `MAX_EMAIL_AGE_HOURS` in `.env` - set to `0` to process all emails regardless of age.