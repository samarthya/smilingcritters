"""
Smiling Critters — Chat Interface
The heart of the app. Streams responses, enforces safety, tracks wellness.
"""

import streamlit as st
import time
from datetime import datetime

from critters.personas import get_critter
from critters.router import get_llm_response, check_llm_status
from safety.filters import check_input, check_output, FlagLevel, wellness_reminder
from db.queries import (
    start_session, end_session, save_message, save_flag,
    get_setting, get_session_messages
)


def _init_session(critter_id: str):
    """Initialise a new chat session in state and DB."""
    if not st.session_state.get("session_id"):
        st.session_state.session_id    = start_session(critter_id)
        st.session_state.session_start = time.time()
        st.session_state.chat_messages = []
        st.session_state.wellness_shown = set()


def _elapsed_minutes() -> float:
    start = st.session_state.get("session_start")
    if not start:
        return 0
    return (time.time() - start) / 60


def _check_wellness(critter_id: str):
    """Show a wellness reminder card if threshold reached."""
    elapsed = _elapsed_minutes()
    already_shown = st.session_state.get("wellness_shown", set())

    for threshold in [30, 60]:
        if elapsed >= threshold and threshold not in already_shown:
            msg = wellness_reminder(elapsed, critter_id)
            if msg:
                already_shown.add(threshold)
                st.session_state.wellness_shown = already_shown
                return msg
    return None


def render_chat():
    critter_id = st.session_state.get("current_critter", "pip")
    critter    = get_critter(critter_id)
    _init_session(critter_id)

    prefer_local = get_setting("llm_prefer_local", "1") == "1"

    # ── Header ────────────────────────────────────────────────────────────────
    col_back, col_title, col_status = st.columns([1, 5, 1])
    with col_back:
        if st.button("← Home"):
            _do_end_session()
            st.session_state.page = "home"
            st.rerun()
    with col_title:
        st.markdown(f"""
        <div style="text-align:center;">
            <span style="font-size:2rem;">{critter['emoji']}</span>
            <span style="font-size:1.5rem; font-weight:bold; color:{critter['color']};">
                &nbsp;{critter['name']}
            </span>
            <span style="font-size:0.9rem; color:#888;">&nbsp;— {critter['specialty']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_status:
        status = check_llm_status()
        icon = "🏠" if status["active"] == "ollama" else ("☁️" if status["active"] == "gemini" else "❌")
        st.markdown(f"<div style='text-align:right; color:#aaa; font-size:0.75rem; padding-top:0.8rem;'>{icon}</div>", unsafe_allow_html=True)

    st.divider()

    # ── Session timer display ─────────────────────────────────────────────────
    elapsed = _elapsed_minutes()
    daily_limit = int(get_setting("daily_limit_min", "45"))
    progress = min(elapsed / daily_limit, 1.0)
    time_color = "#4CAF50" if progress < 0.6 else ("#FF9800" if progress < 0.9 else "#F44336")
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        <span style="font-size:0.8rem; color:#999;">⏱️ {int(elapsed)}min / {daily_limit}min</span>
        <div style="flex:1; background:#eee; border-radius:10px; height:6px;">
            <div style="width:{progress*100:.0f}%; background:{time_color}; border-radius:10px; height:6px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Wellness reminder check ───────────────────────────────────────────────
    wellness_msg = _check_wellness(critter_id)
    if wellness_msg:
        st.info(f"{critter['emoji']} {wellness_msg}")

    # ── Chat history ──────────────────────────────────────────────────────────
    chat_container = st.container(height=420)
    with chat_container:
        # Opening message if empty
        if not st.session_state.chat_messages:
            child_name = get_setting("child_name", "friend")
            opening_messages = {
                "pip":   f"Hi {child_name}! 🦔✨ I'm SO happy you're here! What shall we learn about today? Or is there some homework I can help with?",
                "luna":  f"Hello {child_name} 🦋💜 I'm really glad you came to chat. How are you feeling today? You can tell me anything.",
                "finn":  f"WOAH, {child_name} is here! 🦊🎉 I've been dreaming up the BEST adventure! Want to go on a story with me today?",
                "shelby":f"Hello {child_name} 🐢💙 Welcome. It's nice and calm here. How are you doing today?",
                "stella":f"OH WOW {child_name}! 🌟✨ I just learned the most AMAZING thing and I can't wait to tell you! But first — how are YOU doing?",
            }
            opening = opening_messages.get(critter_id, f"Hi {child_name}! How can I help today?")
            with st.chat_message("assistant", avatar=critter['emoji']):
                st.markdown(f"<span style='color:{critter['color']}'>{opening}</span>", unsafe_allow_html=True)

        # Render history
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧒"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar=critter['emoji']):
                    st.markdown(
                        f"<span style='color:{critter['color']}'>{msg['content']}</span>",
                        unsafe_allow_html=True
                    )

    # ── Input area ────────────────────────────────────────────────────────────
    col_input, col_end = st.columns([5, 1])
    with col_input:
        user_input = st.chat_input(f"Say something to {critter['name']}... 💬")
    with col_end:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👋 Bye!", help="End this chat"):
            _do_end_session()
            _save_journal_entry(critter_id)
            st.session_state.page = "home"
            st.rerun()

    # ── Handle input ──────────────────────────────────────────────────────────
    if user_input and user_input.strip():
        _handle_message(user_input.strip(), critter, prefer_local)


def _handle_message(user_text: str, critter: dict, prefer_local: bool):
    critter_id = critter["id"]

    # Layer 2: Input safety check
    safety = check_input(user_text, critter_id)
    flag_int = {"safe": 0, "redirect": 1, "alert": 2, "crisis": 3}.get(safety.level.value, 0)

    # Save user message
    session_id = st.session_state.session_id
    msg_id = save_message(session_id, "user", user_text, critter_id, flagged=flag_int)

    st.session_state.chat_messages.append({"role": "user", "content": user_text})

    # Save flag if needed
    if safety.level != FlagLevel.SAFE and safety.parent_note:
        save_flag(session_id, msg_id, safety.level.value, safety.reason or "", safety.parent_note or "")

    # If redirect/crisis — show pre-written response, don't call LLM
    if safety.redirect_message:
        response = safety.redirect_message
        save_message(session_id, "assistant", response, critter_id)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
        return

    # Layer 1+3: Call LLM and check output
    llm_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_messages
    ]

    with st.chat_message("assistant", avatar=critter['emoji']):
        placeholder = st.empty()
        full_response = ""

        token_stream = get_llm_response(
            system_prompt=critter["system_prompt"],
            messages=llm_messages,
            use_local=prefer_local,
        )

        for token in token_stream:
            full_response += token
            placeholder.markdown(
                f"<span style='color:{critter['color']}'>{full_response}▌</span>",
                unsafe_allow_html=True
            )

        # Layer 3: Output safety check
        out_safety = check_output(full_response)
        if out_safety.redirect_message:
            full_response = out_safety.redirect_message
            if out_safety.parent_note:
                save_flag(session_id, msg_id, out_safety.level.value, out_safety.reason or "", out_safety.parent_note)

        placeholder.markdown(
            f"<span style='color:{critter['color']}'>{full_response}</span>",
            unsafe_allow_html=True
        )

    save_message(session_id, "assistant", full_response, critter_id)
    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})


def _do_end_session():
    session_id = st.session_state.get("session_id")
    if session_id and st.session_state.get("session_start"):
        duration = int(time.time() - st.session_state.session_start)
        msg_count = len([m for m in st.session_state.get("chat_messages", []) if m["role"] == "user"])
        end_session(session_id, duration, msg_count)


def _save_journal_entry(critter_id: str):
    """Save a summary card to the journal (session state list)."""
    critter = get_critter(critter_id)
    msgs = st.session_state.get("chat_messages", [])
    if not msgs:
        return

    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []

    entry = {
        "critter_id": critter_id,
        "critter_name": critter["name"],
        "critter_emoji": critter["emoji"],
        "critter_color": critter["color"],
        "date": datetime.now().strftime("%A, %d %B %Y"),
        "time": datetime.now().strftime("%H:%M"),
        "message_count": len([m for m in msgs if m["role"] == "user"]),
        "preview": msgs[-2]["content"][:100] + "..." if len(msgs) >= 2 else "A lovely chat!",
        "duration_min": int(_elapsed_minutes()),
    }
    st.session_state.journal_entries.insert(0, entry)
