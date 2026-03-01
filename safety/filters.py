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
    "bubba":  "Ooh, that's a bit outside what I can chat about! Let's keep things cosy ✨ Tell me — is there something fun you're learning about? 🐘",
    "bobby":  "Hmm, that's not something I can talk about ❤️ But I'm all ears for how you're *feeling* today. What's going on in your heart? 🐻",
    "dogday": "Ooh, let's steer our adventure somewhere more magical! 🗺️ What if a friendly dragon showed up right now? 🐕",
    "catnap": "Let's keep our space calm and soft 🐱 Can we take a slow breath together and talk about something peaceful? 💜",
    "kickin": "Hmm, let's find something even more amazing to wonder about! 🐔 Did you know there are more stars in space than grains of sand on Earth? ✨",
    "hoppy":  "Ooh, let's hop over to something way more fun! 🐇 What's your favourite game we could play right now? ⚡",
    "piggy":  "Hmm, let's chat about something more fun! 🐷 Did you eat something yummy today? Tell me! 🍎",
    "crafty": "Let's sparkle somewhere more magical! 🦄 What if we made up a rainbow creature together instead? 🌈",
}

_CRISIS_RESPONSE = """I hear you, and I care about you so much 💜

What you're feeling sounds really, really hard. You don't have to feel this way alone.

**Please tell a grown-up you trust right now** — a parent, teacher, or someone at home. They love you and they want to help.

If you need to talk to someone right now, you can also text or call a helpline for kids — ask a grown-up to help you find one.

You are loved. You matter. 💜🦋"""


# ─── Public API ──────────────────────────────────────────────────────────────

def check_input(text: str, critter_id: str = "bubba") -> SafetyResult:
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
            redirect_message=_REDIRECT_MESSAGES.get(critter_id, _REDIRECT_MESSAGES["bubba"])
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


def wellness_reminder(minutes_elapsed: float, critter_id: str = "bubba") -> str | None:
    """
    Returns a wellness reminder message if appropriate, else None.
    Thresholds: 30 min gentle, 60 min strong.
    """
    reminders_30 = {
        "bubba":  "Psst! We've been chatting for 30 minutes! A little break will help your brain remember everything! Want to rest and come back? 🐘✨",
        "bobby":  "Hey friend 🐻❤️ We've been talking for a while. It's okay to take a little break — your eyes and body deserve a rest too! I'll be right here!",
        "dogday": "Whoa, we've had SO many adventures in the last 30 minutes! 🐕 Even great explorers need a rest! Quick break before the next quest? 🗺️",
        "catnap": "We've been here for 30 minutes 🐱 Time for a little catnap break! Your body will feel even calmer after... 💜",
        "kickin": "Fun fact: resting helps your brain remember all the amazing things we talked about! 🐔 Want a 5-minute break? Science says it helps! ✨",
        "hoppy":  "Wow 30 minutes of fun! 🐇 Even Hoppy needs to stop and wiggle around! Take a 5-minute movement break? ⚡",
        "piggy":  "30 minutes! Maybe time for a little snack AND a break? 🐷 Come back when you're refreshed! 🍎",
        "crafty": "30 magical minutes! 🦄 Step away, rest your eyes, and come back with even MORE sparkly ideas! 🌈",
    }
    reminders_60 = {
        "bubba":  "Wow, a whole hour of learning! 🐘📚 That's amazing — but even the best learners need a proper rest now. I'll be right here when you come back! ⭐",
        "bobby":  "An hour together 🐻❤️ I love our chats SO much. But it's really time for a proper break — your body and mind need it. See you soon!",
        "dogday": "An HOUR of adventures! 🐕 That's a legendary quest! Even the bravest explorers sleep. Time for a real break — your story will be here! 🗺️",
        "catnap": "One hour 🐱 That's a long time even for CatNap! Time for a proper rest now. I'll be here, calm and cosy, when you return 💜",
        "kickin": "One whole hour — your brain has taken in SO many amazing things! 🐔 Now it needs rest to sort it all out. Time for a real break! ✨",
        "hoppy":  "AN HOUR! 🐇 That's incredible! Even Hoppy needs a real rest after that much fun. Go play outside and come back! ⚡",
        "piggy":  "A whole hour! 🐷 Time for a proper rest AND a healthy snack. Your body will thank you! Come back soon! 🍎",
        "crafty": "One whole magical hour! 🦄 Your brain is FULL of wonderful ideas now — let it rest and dream. More creating tomorrow! 🌈",
    }

    if minutes_elapsed >= 60:
        return reminders_60.get(critter_id, reminders_60["bubba"])
    elif minutes_elapsed >= 30:
        return reminders_30.get(critter_id, reminders_30["bubba"])
    return None
