"""
Smiling Critters — Safety Filters
Layer 2 (input) and Layer 3 (output) of the three-layer safety system.
Layer 1 is the system prompt in personas.py.
"""

import re
from dataclasses import dataclass
from enum import Enum


class FlagLevel(Enum):
    SAFE      = "safe"
    REDIRECT  = "redirect"       # Critter gently redirects, no parent alert
    ALERT     = "alert"          # Silent parent notification sent
    CRISIS    = "crisis"         # Immediate supportive response + urgent parent alert


@dataclass
class SafetyResult:
    level: FlagLevel
    reason: str | None = None
    redirect_message: str | None = None
    parent_note: str | None = None


# ─── Keyword lists ───────────────────────────────────────────────────────────

_REDIRECT_PATTERNS = [
    # Violence / weapons
    r'\b(kill|murder|stab|shoot|gun|knife|weapon|bomb|explode|blood|gore|hurt\s+someone)\b',
    # Adult content
    r'\b(sex|porn|naked|adult|xxx|nsfw)\b',
    # Drugs
    r'\b(drug|weed|cocaine|alcohol|drunk|smoke|vape)\b',
    # Scary media
    r'\b(horror|scary movie|nightmare|demon|ghost attack)\b',
]

_ALERT_PATTERNS = [
    # Bullying - she is a target
    r'\b(bully|bullying|they hate me|nobody likes me|they made fun|excluded|left out|no friends)\b',
    # Personal info sharing attempt
    r'\b(my address|my school|where i live|my phone number|come find me)\b',
    # Someone hurting her
    r'\b(hitting me|hurting me|someone hit|someone touched|abuse)\b',
]

_CRISIS_PATTERNS = [
    r'\b(hurt myself|hurt my self|cut myself|kill myself|suicide|want to die|end it all|don\'t want to be here|i hate myself)\b',
    r'\b(self.?harm|no one cares|no one would miss me|everyone would be better without me)\b',
]

# Compile all patterns once
_redirect_re = re.compile("|".join(_REDIRECT_PATTERNS), re.IGNORECASE)
_alert_re    = re.compile("|".join(_ALERT_PATTERNS), re.IGNORECASE)
_crisis_re   = re.compile("|".join(_CRISIS_PATTERNS), re.IGNORECASE)


# ─── Redirect messages (critter-specific tones) ──────────────────────────────

_REDIRECT_MESSAGES = {
    "pip":   "Ooh, that's a bit outside what I can chat about! Let's keep things cosy ✨ Tell me — is there something fun you're learning about? 🦔",
    "luna":  "Hmm, that's not something I can talk about 💜 But I'm all ears for how you're *feeling* today. What's going on in your heart? 🦋",
    "finn":  "Ooh, let's steer our adventure somewhere more magical! 🗺️ What if a friendly dragon showed up right now — what would happen? 🦊",
    "shelby":"Let's keep our space calm and safe 🐢 Can we take a slow breath together and talk about something peaceful? 💙",
    "stella":"Hmm, let's find something even more amazing to wonder about! 🌟 Did you know there are more stars in space than grains of sand on Earth? ✨",
}

_CRISIS_RESPONSE = """I hear you, and I care about you so much 💜

What you're feeling sounds really, really hard. You don't have to feel this way alone.

**Please tell a grown-up you trust right now** — a parent, teacher, or someone at home. They love you and they want to help.

If you need to talk to someone right now, you can also text or call a helpline for kids — ask a grown-up to help you find one.

You are loved. You matter. 💜🦋"""


# ─── Public API ──────────────────────────────────────────────────────────────

def check_input(text: str, critter_id: str = "pip") -> SafetyResult:
    """Screen a child's message before sending to the LLM."""
    t = text.strip()

    if _crisis_re.search(t):
        return SafetyResult(
            level=FlagLevel.CRISIS,
            reason="Crisis language detected in child's message",
            redirect_message=_CRISIS_RESPONSE,
            parent_note=f"⚠️ URGENT: Crisis language detected — '{t[:80]}...'"
        )

    if _alert_re.search(t):
        return SafetyResult(
            level=FlagLevel.ALERT,
            reason="Distress/safety topic in child's message",
            parent_note=f"Flagged message: '{t[:120]}'"
        )

    if _redirect_re.search(t):
        return SafetyResult(
            level=FlagLevel.REDIRECT,
            reason="Off-limits topic",
            redirect_message=_REDIRECT_MESSAGES.get(critter_id, _REDIRECT_MESSAGES["pip"])
        )

    return SafetyResult(level=FlagLevel.SAFE)


def check_output(text: str) -> SafetyResult:
    """Screen LLM output before showing to the child."""
    # Run same filters on output — belt and suspenders
    if _crisis_re.search(text):
        return SafetyResult(
            level=FlagLevel.CRISIS,
            reason="Crisis content in LLM output — replaced",
            redirect_message="I'm here with you 💜 Can you find a grown-up you trust to talk to right now?",
            parent_note="LLM output contained crisis-level content and was blocked."
        )

    if _redirect_re.search(text):
        return SafetyResult(
            level=FlagLevel.REDIRECT,
            reason="Off-limits content in LLM output — replaced",
            redirect_message="Oops, my brain went a bit fuzzy! Let's talk about something fun instead ✨"
        )

    return SafetyResult(level=FlagLevel.SAFE)


def wellness_reminder(minutes_elapsed: float, critter_id: str = "pip") -> str | None:
    """
    Returns a wellness reminder message if appropriate, else None.
    Thresholds: 30 min gentle, 60 min strong.
    """
    reminders_30 = {
        "pip":   "Psst! We've been chatting for 30 minutes! My little hedgehog eyes are getting a tiny bit tired 😴 Want to take a 5-minute break and come back? I'll save our spot! 🦔",
        "luna":  "Hey friend 💜 We've been talking for a while. It's okay to take a little break — your eyes and body deserve a rest too! I'll be right here 🦋",
        "finn":  "Whoa, we've had SO many adventures in the last 30 minutes! 🦊 Even great explorers need a rest! Want to take a quick break before our next quest? 🗺️",
        "shelby":"We've been here for 30 minutes 🐢 Slow and steady — that includes resting! A little break will help us feel even better 💙",
        "stella":"Fun fact: resting actually helps your brain remember all the amazing things we talked about! 🌟 Want to take a 5-minute break? Science says it helps! ✨",
    }
    reminders_60 = {
        "pip":   "Wow, we've been learning together for a whole hour! 📚 That's amazing — but even the best students need a proper rest now. I'll be right here when you come back! 🦔⭐",
        "luna":  "An hour together 💜 I love our chats SO much. But it's really time for a proper break now — your body and mind need it. See you soon! 🦋",
        "finn":  "An HOUR of adventures! 🦊 That's a legendary quest! Even the bravest heroes sleep. Time for a real break — your story will be here waiting! ✨",
        "shelby":"One hour 🐢 That's a long time. Time for a proper rest now. I'll be here, slow and steady, when you return 💙",
        "stella":"One whole hour — your brain has taken in SO many amazing things! 🌟 Now it needs rest to process it all. Time for a real break! ✨",
    }

    if minutes_elapsed >= 60:
        return reminders_60.get(critter_id, reminders_60["pip"])
    elif minutes_elapsed >= 30:
        return reminders_30.get(critter_id, reminders_30["pip"])
    return None
