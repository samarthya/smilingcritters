"""
Smiling Critters — Chat Interface (v2)
Improved visuals, emotion wheel for Luna, Ollama debug panel, better flow.
"""

import streamlit as st
import time
from datetime import datetime

from critters.personas import get_critter
from critters.router import get_llm_response, check_llm_status
from safety.filters import check_input, check_output, FlagLevel, wellness_reminder
from db.queries import (
    start_session, end_session, save_message, save_flag,
    get_setting, get_session_messages, save_journal_entry
)
from theme import get_critter_avatar, get_critter_pil_avatar, get_critter_icon_img


def _init_session(critter_id: str):
    if not st.session_state.get("session_id"):
        st.session_state.session_id     = start_session(critter_id)
        st.session_state.session_start  = time.time()
        st.session_state.chat_messages  = []
        st.session_state.wellness_shown = set()
        st.session_state.show_emotion_wheel = False
        st.session_state.selected_emotion   = None
    # Voice state — initialise if missing (survives across reruns within a session)
    if "voice_key" not in st.session_state:
        st.session_state.voice_key = 0
    if "voice_pending" not in st.session_state:
        st.session_state.voice_pending = None


def _elapsed_minutes() -> float:
    start = st.session_state.get("session_start")
    return (time.time() - start) / 60 if start else 0


def _check_wellness(critter_id: str):
    elapsed = _elapsed_minutes()
    shown   = st.session_state.get("wellness_shown", set())
    for threshold in [30, 60]:
        if elapsed >= threshold and threshold not in shown:
            msg = wellness_reminder(elapsed, critter_id)
            if msg:
                shown.add(threshold)
                st.session_state.wellness_shown = shown
                return msg
    return None


def render_chat():
    critter_id   = st.session_state.get("current_critter", "bubba")
    critter      = get_critter(critter_id)
    prefer_local = get_setting("llm_prefer_local", "1") == "1"
    _init_session(critter_id)

    # PIL avatar — used for st.chat_message; falls back to emoji if PNGs not yet extracted
    _pil_avatar = get_critter_pil_avatar(critter_id) or critter["emoji"]

    # ── Header bar ────────────────────────────────────────────────────────────
    svg = get_critter_avatar(critter_id, size=60)
    col_back, col_avatar, col_title, col_status = st.columns([1, 1, 5, 1.5])

    with col_back:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Home", key="back_home"):
            _do_end_session()
            st.session_state.page = "home"
            st.rerun()

    with col_avatar:
        st.markdown(
            f'<div style="width:60px; margin-top:0.2rem;">{svg}</div>',
            unsafe_allow_html=True
        )

    with col_title:
        st.markdown(f"""
        <div style="padding-top:0.6rem;">
            <span style="font-family:'Nunito',sans-serif; font-size:1.5rem;
                         font-weight:900; color:{critter['color']};">
                {critter['name']}
            </span>
            <span style="font-size:0.85rem; color:#aaa; margin-left:0.5rem;">
                — {critter['specialty']}
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_status:
        status = check_llm_status()
        active = status.get("active", "none")
        backoff_secs = status.get("gemini", {}).get("backoff_secs", 0)
        status_html = {
            "ollama":       '<span style="background:#E8F5E9;color:#2E7D32;border-radius:12px;padding:0.2rem 0.6rem;font-size:0.75rem;font-weight:700;">🏠 Local</span>',
            "gemini":       '<span style="background:#E3F2FD;color:#1565C0;border-radius:12px;padding:0.2rem 0.6rem;font-size:0.75rem;font-weight:700;">☁️ Cloud</span>',
            "rate_limited": f'<span style="background:#FFF3E0;color:#E65100;border-radius:12px;padding:0.2rem 0.6rem;font-size:0.75rem;font-weight:700;" title="Gemini rate-limited, retrying in {backoff_secs}s">⏳ Cooling</span>',
            "none":         '<span style="background:#FFEBEE;color:#C62828;border-radius:12px;padding:0.2rem 0.6rem;font-size:0.75rem;font-weight:700;">❌ Off</span>',
        }.get(active, "")
        st.markdown(f'<div style="padding-top:0.8rem;text-align:right;">{status_html}</div>', unsafe_allow_html=True)

    # ── Ollama debug panel (expander, auto-open if disconnected) ──────────────
    if active == "none":
        with st.expander("⚠️ No AI connected — click to troubleshoot", expanded=True):
            _render_ollama_debug(status)
    else:
        with st.expander("🔧 AI Connection Details", expanded=False):
            _render_ollama_debug(status)

    st.markdown('<hr style="margin:0.4rem 0 0.6rem 0;">', unsafe_allow_html=True)

    # ── Session timer ─────────────────────────────────────────────────────────
    elapsed      = _elapsed_minutes()
    daily_limit  = int(get_setting("daily_limit_min") or "45")
    progress     = min(elapsed / daily_limit, 1.0)
    bar_color    = "#4CAF50" if progress < 0.6 else ("#FF9800" if progress < 0.9 else "#F44336")

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.6rem;">
        <span style="font-size:0.8rem; color:#aaa; white-space:nowrap;">
            ⏱️ {int(elapsed)}m / {daily_limit}m
        </span>
        <div style="flex:1; background:#F0EAF8; border-radius:10px; height:7px; overflow:hidden;">
            <div style="width:{progress*100:.0f}%; background:{bar_color};
                        border-radius:10px; height:7px;
                        transition: width 1s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Wellness reminder ─────────────────────────────────────────────────────
    wellness_msg = _check_wellness(critter_id)
    if wellness_msg:
        st.markdown(f"""
        <div class="fade-in" style="
            background: linear-gradient(135deg, {critter['bg_color']}, white);
            border: 2px solid {critter['color']}44;
            border-radius: 20px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.8rem;
            font-size: 0.95rem;
        ">
            {get_critter_icon_img(critter_id, size=32, style='margin-right:8px;')} {wellness_msg}
        </div>
        """, unsafe_allow_html=True)

    # ── Bobby emotion wheel toggle ─────────────────────────────────────────────
    if critter_id == "bobby":
        col_ew, _ = st.columns([2, 5])
        with col_ew:
            wheel_label = "🌈 Hide feelings wheel" if st.session_state.get("show_emotion_wheel") else "🌈 How am I feeling?"
            if st.button(wheel_label, key="emotion_wheel_toggle"):
                st.session_state.show_emotion_wheel = not st.session_state.get("show_emotion_wheel", False)
                st.session_state.selected_emotion   = None
                st.rerun()

        if st.session_state.get("show_emotion_wheel"):
            from pages.emotion_wheel import render_emotion_wheel
            chosen = render_emotion_wheel(critter_id)
            if chosen:
                # Auto-inject into chat
                feeling_msg = f"I'm feeling {chosen.lower()} right now."
                st.session_state.show_emotion_wheel = False
                st.session_state.selected_emotion   = None
                _handle_message(feeling_msg, critter, prefer_local)
                st.rerun()
            return  # Don't show chat while wheel is open

    # ── Chat history ──────────────────────────────────────────────────────────
    chat_container = st.container(height=400)
    with chat_container:
        # Opening message
        if not st.session_state.chat_messages:
            child_name = get_setting("child_name", "friend")
            openings = {
                "bubba":  f"Hi {child_name}! 🐘✨ I'm SO happy you're here! Is there homework I can help with, or something cool you want to learn about?",
                "bobby":  f"Hello {child_name} 🐻❤️ I'm really glad you came. How are you feeling today? You can tell me *anything* — I'm here to listen!",
                "dogday": f"WOAH, {child_name} is here! 🐕 I've been dreaming up the BEST adventure! Want to make up a story together? 🗺️✨",
                "catnap": f"Hello {child_name} 🐱💜 Welcome. Take a slow breath... It's nice and calm here. How are you today?",
                "kickin": f"OH WOW, {child_name}! 🐔 Did you know octopuses have THREE hearts?! Amazing right?! What amazing thing shall we wonder about today? ✨",
                "hoppy":  f"YO {child_name}! 🐇⚡ Ready to PLAY?! Let's do something super fun together! What shall we try?",
                "piggy":  f"Hiii {child_name}! 🐷🍎 Did you have something yummy today? I LOVE hearing about good food and happy healthy things!",
                "crafty": f"Ooooh {child_name}! 🦄🌈 I have SO many sparkly ideas for us today! Are you ready to make something magical?!",
            }
            opening = openings.get(critter_id, f"Hi {child_name}! How can I help?")
            with st.chat_message("assistant", avatar=_pil_avatar):
                st.markdown(
                    f'<div style="color:{critter["color"]}; font-family:Nunito Sans,sans-serif;">{opening}</div>',
                    unsafe_allow_html=True
                )

        # Render history
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧒"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar=_pil_avatar):
                    st.markdown(
                        f'<div style="color:{critter["color"]}; font-family:Nunito Sans,sans-serif;">{msg["content"]}</div>',
                        unsafe_allow_html=True
                    )

    # ── Voice input ───────────────────────────────────────────────────────────
    try:
        import speech_recognition  # noqa: F401 — voice feature available
        _voice_available = True
    except ImportError:
        _voice_available = False

    if _voice_available:
        with st.expander("🎤 Use your voice", expanded=False):
            # Key rotates after each recording so the widget resets and never
            # replays the same audio on the next rerun (prevents the loop).
            voice_audio = st.audio_input(
                "Tap 🔴 to record, tap again to stop — your words will be sent automatically!",
                key=f"voice_msg_{st.session_state.voice_key}",
            )
            if voice_audio:
                with st.spinner("Listening... 🎧"):
                    voice_text = _transcribe_audio(voice_audio)
                # Rotate key NOW so the widget is blank on the next rerun
                st.session_state.voice_key += 1
                if voice_text:
                    # Stage the text — it will be sent via the normal input handler below
                    st.session_state.voice_pending = voice_text
                else:
                    st.warning("Hmm, I couldn't quite hear that! Try again below. 😊")
                st.rerun()

    # ── Input row ─────────────────────────────────────────────────────────────
    col_inp, col_share, col_bye = st.columns([6, 1, 1])
    with col_inp:
        user_input = st.chat_input(f"Say something to {critter['name']}... 💬")
    with col_share:
        msgs = st.session_state.get("chat_messages", [])
        if msgs:
            transcript = _build_transcript(critter["name"], msgs)
            st.download_button(
                "📤",
                data=transcript,
                file_name=f"chat-with-{critter['name'].lower().replace(' ', '-')}.txt",
                mime="text/plain",
                help="Download this chat as a text file to share with a grown-up",
                key="share_chat",
            )
    with col_bye:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👋 Bye!", key="end_chat", help="End this chat"):
            _do_end_session()
            _save_journal_entry(critter_id)
            st.session_state.page = "home"
            st.rerun()

    # ── Handle input (typed or voice) ─────────────────────────────────────────
    if user_input and user_input.strip():
        _handle_message(user_input.strip(), critter, prefer_local)
    elif st.session_state.get("voice_pending"):
        voice_text = st.session_state.voice_pending
        st.session_state.voice_pending = None
        _handle_message(voice_text, critter, prefer_local)
        st.rerun()


def _render_ollama_debug(status: dict):
    """Inline Ollama troubleshooting panel."""
    ollama = status.get("ollama", {})
    gemini = status.get("gemini", {})

    col1, col2 = st.columns(2)
    with col1:
        ok = ollama.get("available", False)
        icon = "✅" if ok else "❌"
        st.markdown(f"**{icon} Ollama (Local)**")
        st.code(f"URL:   {ollama.get('url', 'http://localhost:11434')}\nModel: {ollama.get('model', 'llama3:latest')}\nStatus: {'Connected' if ok else 'Not reachable'}")
        if not ok:
            st.markdown("""
**To fix:**
```bash
# Start Ollama
ollama serve

# Pull a model if you haven't yet
ollama pull llama3:latest
```
            """)

    with col2:
        ok = gemini.get("available", False)
        icon = "✅" if ok else "⚠️"
        st.markdown(f"**{icon} Gemini (Cloud fallback)**")
        st.markdown(f"Status: {'API key set ✅' if ok else 'No API key — add GEMINI_API_KEY to .env'}")
        if not ok:
            st.markdown("""
**To fix:**
1. Get free key at [ai.google.dev](https://ai.google.dev)
2. Add to `.env`: `GEMINI_API_KEY=your_key`
3. Restart the app
            """)


def _handle_message(user_text: str, critter: dict, prefer_local: bool):
    critter_id  = critter["id"]
    _pil_avatar = get_critter_pil_avatar(critter_id) or critter["emoji"]
    safety      = check_input(user_text, critter_id)
    flag_int   = {"safe": 0, "redirect": 1, "alert": 2, "crisis": 3}.get(safety.level.value, 0)

    session_id = st.session_state.session_id
    msg_id = save_message(session_id, "user", user_text, critter_id, flagged=flag_int)
    st.session_state.chat_messages.append({"role": "user", "content": user_text})

    if safety.level != FlagLevel.SAFE and safety.parent_note:
        save_flag(session_id, msg_id, safety.level.value, safety.reason or "", safety.parent_note or "")

    # Redirect / crisis — pre-written response, don't call LLM
    if safety.redirect_message:
        response = safety.redirect_message
        save_message(session_id, "assistant", response, critter_id)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
        return

    # Call LLM with streaming
    llm_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_messages
    ]

    with st.chat_message("assistant", avatar=_pil_avatar):
        placeholder   = st.empty()
        full_response = ""

        try:
            for token in get_llm_response(
                system_prompt=critter["system_prompt"],
                messages=llm_messages,
                use_local=prefer_local,
            ):
                full_response += token
                placeholder.markdown(
                    f'<div style="color:{critter["color"]};font-family:Nunito Sans,sans-serif;">{full_response}▌</div>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            full_response = f"Oops, my brain went fuzzy for a second! 🌟 Can you try again? (Error: {str(e)[:60]})"

        # Layer 3: output safety check
        out_safety = check_output(full_response)
        if out_safety.redirect_message:
            full_response = out_safety.redirect_message
            if out_safety.parent_note:
                save_flag(session_id, msg_id, out_safety.level.value,
                          out_safety.reason or "", out_safety.parent_note)

        placeholder.markdown(
            f'<div style="color:{critter["color"]};font-family:Nunito Sans,sans-serif;">{full_response}</div>',
            unsafe_allow_html=True
        )

    save_message(session_id, "assistant", full_response, critter_id)
    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})


def _do_end_session():
    session_id = st.session_state.get("session_id")
    if session_id and st.session_state.get("session_start"):
        duration  = int(time.time() - st.session_state.session_start)
        msg_count = len([m for m in st.session_state.get("chat_messages", []) if m["role"] == "user"])
        end_session(session_id, duration, msg_count)


def _transcribe_audio(audio_value) -> str:
    """Transcribe recorded audio via Google Speech Recognition (free, online).
    Returns empty string if transcription fails or the package is not installed."""
    try:
        import speech_recognition as sr
        import io

        recognizer = sr.Recognizer()
        audio_bytes = io.BytesIO(audio_value.read())
        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception:
        return ""


def _build_transcript(critter_name: str, msgs: list) -> str:
    """Format chat messages as a plain-text transcript for export."""
    lines = [
        f"Chat with {critter_name}",
        "=" * 40,
        f"Exported: {datetime.now().strftime('%A, %d %B %Y at %H:%M')}",
        "",
    ]
    for msg in msgs:
        speaker = "You" if msg["role"] == "user" else critter_name
        lines.append(f"{speaker}: {msg['content']}")
        lines.append("")
    return "\n".join(lines)


def _save_journal_entry(critter_id: str):
    critter = get_critter(critter_id)
    msgs    = st.session_state.get("chat_messages", [])
    if not msgs:
        return

    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []

    # Find last user message for preview
    user_msgs = [m["content"] for m in msgs if m["role"] == "user"]
    preview   = user_msgs[-1][:100] + "..." if user_msgs else "A lovely quiet chat!"
    duration  = int(_elapsed_minutes())
    date_str  = datetime.now().strftime("%A, %d %B %Y")
    time_str  = datetime.now().strftime("%H:%M")

    entry = {
        "critter_id":    critter_id,
        "critter_name":  critter["name"],
        "critter_emoji": critter["emoji"],
        "critter_color": critter["color"],
        "critter_bg":    critter["bg_color"],
        "date":          date_str,
        "time":          time_str,
        "message_count": len(user_msgs),
        "preview":       preview,
        "duration_min":  duration,
    }

    # Persist to SQLite so journal survives app restarts
    session_id = st.session_state.get("session_id")
    if session_id:
        save_journal_entry(
            session_id=session_id,
            critter_id=critter_id,
            critter_name=critter["name"],
            critter_emoji=critter["emoji"],
            critter_color=critter["color"],
            critter_bg=critter["bg_color"],
            date=date_str,
            time_str=time_str,
            message_count=len(user_msgs),
            preview=preview,
            duration_min=duration,
        )

    st.session_state.journal_entries.insert(0, entry)
