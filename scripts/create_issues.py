#!/usr/bin/env python3
"""
Smiling Critters — GitHub Issues & Project Board Setup
Run this once to create all Issues and a project board.

Prerequisites:
    gh auth login          # if not already authenticated
    pip install PyGithub   # optional, we use gh CLI directly

Usage:
    python scripts/create_issues.py
"""

import subprocess
import sys
import json

REPO = "samarthya/smilingcritters"

ISSUES = [
    # ── Visual & UX ──────────────────────────────────────────────────────────
    {
        "title": "🎨 [UX] SVG critter avatars on home screen",
        "body": """## Description
Replace emoji placeholders with hand-crafted SVG critter avatars on the home screen.

## Acceptance Criteria
- [ ] All 5 critters have unique SVG illustrations
- [ ] Avatars animate (float/bounce) on the home screen  
- [ ] Avatars appear in chat header
- [ ] Responsive at all screen sizes

## Notes
SVGs defined in `theme.py` → `CRITTER_SVGS` dict.
""",
        "labels": ["enhancement", "ui/ux"],
    },
    {
        "title": "🎨 [UX] Global theme — Nunito font, bubbly buttons, gradient background",
        "body": """## Description
Apply child-friendly visual theme: Nunito font, rounded buttons, soft gradient backgrounds, card hover animations.

## Acceptance Criteria
- [ ] Nunito font loaded from Google Fonts
- [ ] All buttons rounded (24px border-radius)
- [ ] Page background is soft gradient (not white)
- [ ] Critter cards have hover lift animation
- [ ] Chat bubbles are styled per critter colour

## Files
`theme.py` → `GLOBAL_CSS` + `apply_theme()`
""",
        "labels": ["enhancement", "ui/ux"],
    },
    {
        "title": "💬 [UX] Critter sidebar quick-pick",
        "body": """## Description
Add quick-access critter buttons to the sidebar so users can jump directly to any critter without going back to the home screen.

## Acceptance Criteria
- [ ] All 5 critters visible in sidebar
- [ ] Clicking jumps to fresh chat with that critter
- [ ] Current critter is visually highlighted

## Files
`app.py` → sidebar section
""",
        "labels": ["enhancement", "ui/ux"],
    },

    # ── Features ─────────────────────────────────────────────────────────────
    {
        "title": "🌈 [Feature] Luna emotion wheel",
        "body": """## Description
Add a visual emotion picker (wheel) for Luna's chat. 
Allows the child to tap how they're feeling, which auto-injects into the chat.

## Acceptance Criteria
- [ ] 24 emotions across 4 groups (Happy / Sad / Angry / Scared)
- [ ] Each emotion has emoji, label, colour, description
- [ ] Selected emotion auto-sends to Luna as a message
- [ ] Toggle button in Luna's chat header
- [ ] Works on mobile-width screens

## Files
`pages/emotion_wheel.py` → `render_emotion_wheel()`
`pages/chat.py` → Luna-specific integration
""",
        "labels": ["enhancement", "feature"],
    },
    {
        "title": "⏱️ [Feature] Wellness reminders at 30 and 60 minutes",
        "body": """## Description
Critters deliver in-character wellness reminders when session hits 30 and 60 minute marks.

## Acceptance Criteria
- [ ] 30-min reminder: gentle, optional break suggestion
- [ ] 60-min reminder: stronger, encourages ending session
- [ ] Each critter has their own unique reminder voice
- [ ] Parent can toggle reminders on/off in dashboard
- [ ] Reminder only shown once per threshold per session

## Files
`safety/filters.py` → `wellness_reminder()`
`pages/chat.py` → `_check_wellness()`
""",
        "labels": ["enhancement", "feature", "safety"],
    },
    {
        "title": "📖 [Feature] Session journal with keepsake cards",
        "body": """## Description
After every chat, save a journal card showing: critter, date/time, message count, session duration, and a preview of the last thing said.

## Acceptance Criteria
- [ ] Journal entry auto-saved on "Bye!" button
- [ ] Journal page shows cards in reverse chronological order
- [ ] Cards styled per critter colour theme
- [ ] Empty state with friendly message

## Files
`pages/journal.py`
`pages/chat.py` → `_save_journal_entry()`
""",
        "labels": ["enhancement", "feature"],
    },
    {
        "title": "🫁 [Feature] Shelby guided breathing exercise",
        "body": """## Description
Shelby the turtle should offer an animated breathing exercise when the child seems overwhelmed or asks to calm down.

## Acceptance Criteria
- [ ] Animated breathing circle (expand/contract with CSS)
- [ ] Box breathing: 4s in, 4s hold, 4s out, 4s hold
- [ ] 5-4-3-2-1 grounding mode as alternative
- [ ] Triggered by keywords: "overwhelmed", "can't breathe", "panic"
- [ ] Can also be manually triggered by button in Shelby's chat

## Files
`pages/breathing.py` (new)
`pages/chat.py` → Shelby integration
""",
        "labels": ["enhancement", "feature"],
    },

    # ── Safety ────────────────────────────────────────────────────────────────
    {
        "title": "🛡️ [Safety] Three-layer content filter",
        "body": """## Description
Implement the full three-layer safety system:
- Layer 1: System prompts (done — in personas.py)
- Layer 2: Input filter before LLM call
- Layer 3: Output filter before display

## Acceptance Criteria
- [ ] Regex-based keyword detection (violent, adult, drug topics)
- [ ] Alert-level detection (bullying, personal info sharing)
- [ ] Crisis detection (self-harm language) with urgent parent flag
- [ ] Each level has critter-appropriate redirect message
- [ ] Output filter catches anything Layer 1 misses
- [ ] All flags logged to SQLite with timestamp

## Files
`safety/filters.py`
""",
        "labels": ["safety", "priority"],
    },
    {
        "title": "🚨 [Safety] Parent silent alerts for crisis events",
        "body": """## Description
When crisis language is detected, the parent should receive an immediate alert — without alarming the child.

## Acceptance Criteria
- [ ] Crisis events create a DB flag immediately
- [ ] Parent dashboard shows unread badge count
- [ ] Crisis flags are highlighted in red in alert centre
- [ ] Each flag shows: timestamp, message context, critter response
- [ ] Acknowledge button to mark reviewed

## Files
`db/queries.py` → `save_flag()`, `get_unacknowledged_flags()`
`pages/parent_dashboard.py` → alerts tab
""",
        "labels": ["safety", "priority"],
    },

    # ── Infrastructure ────────────────────────────────────────────────────────
    {
        "title": "🏠 [Infra] Ollama local LLM integration with auto-fallback",
        "body": """## Description
Connect to locally running Ollama as primary LLM. Auto-detect availability and fall back to Gemini Flash when offline.

## Acceptance Criteria
- [ ] Reachability check before each request (2s timeout)
- [ ] Streaming responses from Ollama
- [ ] Auto-fallback to Gemini without user action
- [ ] Status indicator in chat header (🏠 Local / ☁️ Cloud / ❌ Off)
- [ ] Debug panel in chat view with troubleshooting steps
- [ ] Configurable URL and model in parent settings

## Test Steps
```bash
ollama serve
ollama pull llama3:latest
# Open app, check "🏠 Local" indicator
ollama stop  # check fallback to ☁️ Cloud
```

## Files
`critters/router.py`
""",
        "labels": ["infrastructure", "priority"],
    },
    {
        "title": "☁️ [Infra] Gemini Flash API cloud fallback",
        "body": """## Description
Integrate Google Gemini Flash as the cloud fallback LLM when Ollama is unavailable.

## Acceptance Criteria
- [ ] Streaming via SSE endpoint
- [ ] API key loaded from .env (never hardcoded)
- [ ] PII sanitisation before sending messages
- [ ] Graceful error if API key missing/invalid
- [ ] Cost tracking note: Gemini Flash is ~$0.075/1M tokens

## Setup
```
GEMINI_API_KEY=your_key_here  # in .env file
```

## Files
`critters/router.py` → `_call_gemini()`
""",
        "labels": ["infrastructure"],
    },
    {
        "title": "🗄️ [Infra] SQLite persistence — sessions, messages, flags, settings",
        "body": """## Description
All chat history, safety flags, and settings stored locally in SQLite. No external database needed.

## Acceptance Criteria
- [ ] Sessions table: critter, start/end time, duration, message count
- [ ] Messages table: role, content, critter, timestamp, flag level
- [ ] Safety flags table with acknowledgement tracking
- [ ] Settings key/value store with defaults
- [ ] DB auto-created on first run in ./data/ directory
- [ ] ./data/ in .gitignore (never commit chat logs)

## Files
`db/queries.py` → `init_db()` and all CRUD functions
""",
        "labels": ["infrastructure"],
    },

    # ── Parent Dashboard ──────────────────────────────────────────────────────
    {
        "title": "👨‍👧 [Dashboard] Full parent visibility panel",
        "body": """## Description
PIN-gated parent dashboard with full chat logs, safety alerts, usage stats, and all configuration.

## Acceptance Criteria
- [ ] PIN gate (default: 1234, changeable in settings)
- [ ] Overview tab: sessions, messages, avg duration, critter usage chart
- [ ] Chat logs tab: session picker, full message history
- [ ] Safety alerts tab: all flags, severity, acknowledgement
- [ ] Settings tab: child name, time limits, AI config, PIN change

## Files
`pages/parent_dashboard.py`
""",
        "labels": ["feature", "parent"],
    },

    # ── Phase 2 — iOS App ─────────────────────────────────────────────────────
    {
        "title": "📱 [iOS] SwiftUI project scaffold",
        "body": """## Description
Once the Python prototype is validated, begin the native iOS app in SwiftUI.

## Acceptance Criteria
- [ ] Xcode project created (iOS 17+, SwiftUI, SwiftData)
- [ ] Same Ollama/Gemini backend architecture
- [ ] Same 5 critter personas (system prompts ported)
- [ ] Navigation mirrors web prototype screens

## Prerequisite
Python prototype validated with child user testing ✅

## Notes
Target: TestFlight family beta within 12 weeks of iOS development start.
""",
        "labels": ["ios", "phase-2"],
    },
]

LABELS_TO_CREATE = [
    {"name": "ui/ux",          "color": "e879f9", "description": "Visual design and user experience"},
    {"name": "feature",        "color": "6C3FC8", "description": "New functionality"},
    {"name": "safety",         "color": "DC2626", "description": "Child safety and content filtering"},
    {"name": "infrastructure", "color": "2563EB", "description": "Backend, DB, LLM integration"},
    {"name": "parent",         "color": "059669", "description": "Parent dashboard features"},
    {"name": "ios",            "color": "D97706", "description": "Native iOS app (Phase 2)"},
    {"name": "phase-2",        "color": "78716C", "description": "Future phase work"},
    {"name": "priority",       "color": "EF4444", "description": "High priority"},
]


def run(cmd: str) -> tuple[int, str, str]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    print("🐾 Smiling Critters — GitHub Setup")
    print("=" * 50)

    # Check gh CLI
    code, out, _ = run("gh --version")
    if code != 0:
        print("❌ GitHub CLI not found. Install from: https://cli.github.com")
        print("   Then run: gh auth login")
        sys.exit(1)
    print(f"✅ gh CLI found: {out.split(chr(10))[0]}")

    # Check auth
    code, _, _ = run("gh auth status")
    if code != 0:
        print("❌ Not authenticated. Run: gh auth login")
        sys.exit(1)
    print("✅ GitHub authenticated")

    # Create labels
    print("\n📋 Creating labels...")
    for label in LABELS_TO_CREATE:
        code, _, err = run(
            f'gh label create "{label["name"]}" '
            f'--color "{label["color"]}" '
            f'--description "{label["description"]}" '
            f'--repo {REPO} --force'
        )
        icon = "✅" if code == 0 else "⚠️"
        print(f"  {icon} Label: {label['name']}")

    # Create issues
    print(f"\n🐾 Creating {len(ISSUES)} issues...")
    created_numbers = []
    for issue in ISSUES:
        labels_str = ",".join(issue.get("labels", []))
        # Write body to temp file to avoid shell escaping issues
        with open("/tmp/sc_issue_body.md", "w") as f:
            f.write(issue["body"])

        code, out, err = run(
            f'gh issue create '
            f'--title "{issue["title"]}" '
            f'--body-file /tmp/sc_issue_body.md '
            f'--label "{labels_str}" '
            f'--repo {REPO}'
        )
        if code == 0:
            # Extract issue number from URL
            number = out.strip().split("/")[-1]
            created_numbers.append(number)
            print(f"  ✅ #{number}: {issue['title'][:55]}...")
        else:
            print(f"  ❌ Failed: {issue['title'][:55]}... ({err[:60]})")

    print(f"\n✅ Done! Created {len(created_numbers)} issues.")
    print(f"\n🔗 View at: https://github.com/{REPO}/issues")
    print("\n💡 Next: Create a Project board at:")
    print(f"   https://github.com/{REPO}/projects")
    print("   Add columns: Backlog → In Progress → Review → Done")
    print("   Then drag issues into the right columns.")


if __name__ == "__main__":
    main()
