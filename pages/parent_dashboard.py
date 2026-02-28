"""
Smiling Critters — Parent Dashboard
Full visibility and control. PIN-protected.
"""

import streamlit as st
from db.queries import (
    get_all_settings, set_setting, get_setting,
    get_recent_sessions, get_session_messages,
    get_unacknowledged_flags, get_all_flags,
    acknowledge_flag, get_usage_stats
)
from critters.personas import get_critter, get_all_critters
from critters.router import check_llm_status


FLAG_COLORS = {
    "safe":     ("#4CAF50", "✅ Safe"),
    "redirect": ("#FF9800", "↩️ Redirected"),
    "alert":    ("#F44336", "⚠️ Alert"),
    "crisis":   ("#B71C1C", "🚨 CRISIS"),
}


def render_parent_dashboard():
    # ── PIN gate ──────────────────────────────────────────────────────────────
    if not st.session_state.get("parent_authenticated"):
        _render_pin_gate()
        return

    _render_dashboard()


def _render_pin_gate():
    st.markdown("""
    <div style="max-width:360px; margin:4rem auto; text-align:center;">
        <div style="font-size:3rem; margin-bottom:1rem;">👨‍👧</div>
        <h2 style="color:#6C3FC8;">Parent Dashboard</h2>
        <p style="color:#888;">Enter your PIN to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin = st.text_input("PIN", type="password", max_chars=8, label_visibility="collapsed",
                            placeholder="Enter PIN...")
        if st.button("Unlock 🔓", use_container_width=True):
            correct_pin = get_setting("parent_pin", "1234")
            if pin == correct_pin:
                st.session_state.parent_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect PIN. Please try again.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to App", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


def _render_dashboard():
    # Header
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("""
        <h2 style="color:#6C3FC8; margin:0;">👨‍👧 Parent Dashboard</h2>
        <p style="color:#888; margin:0;">Full visibility & control</p>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🔒 Lock"):
            st.session_state.parent_authenticated = False
            st.rerun()
        if st.button("← App"):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    # Unread alerts banner
    unread = get_unacknowledged_flags()
    if unread:
        urgent = [f for f in unread if f.get("flag_level") == "crisis"]
        if urgent:
            st.error(f"🚨 **{len(urgent)} URGENT alert(s) require your attention!** See the Alerts tab below.")
        else:
            st.warning(f"⚠️ **{len(unread)} unread safety flag(s).** See the Alerts tab below.")

    # LLM status
    status = check_llm_status()
    active = status.get("active", "none")
    status_text = {
        "ollama": "🏠 Using Local AI (Ollama) — private & offline",
        "gemini": "☁️ Using Cloud AI (Gemini) — Ollama unavailable",
        "none":   "❌ No AI connected — check settings",
    }.get(active, "Unknown")
    st.info(status_text)

    # Tabs
    tab_overview, tab_logs, tab_alerts, tab_settings = st.tabs([
        "📊 Overview", "💬 Chat Logs", "🚨 Safety Alerts", "⚙️ Settings"
    ])

    # ── OVERVIEW ──────────────────────────────────────────────────────────────
    with tab_overview:
        stats = get_usage_stats()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sessions", stats["total_sessions"])
        col2.metric("Messages Sent", stats["total_messages"])
        col3.metric("Avg Session", f"{stats['avg_session_min']} min")
        col4.metric("Safety Flags", stats["total_flags"],
                    delta=f"{stats['unread_flags']} unread" if stats["unread_flags"] else None,
                    delta_color="inverse" if stats["unread_flags"] else "off")

        st.markdown("**Favourite Critters**")
        critter_usage = stats.get("critter_usage", [])
        for cu in critter_usage:
            c = get_critter(cu["critter_id"])
            pct = (cu["n"] / max(stats["total_sessions"], 1)) * 100
            st.markdown(f"{c['emoji']} **{c['name']}** — {cu['n']} sessions ({pct:.0f}%)")

    # ── CHAT LOGS ─────────────────────────────────────────────────────────────
    with tab_logs:
        sessions = get_recent_sessions(20)
        if not sessions:
            st.info("No sessions yet.")
        else:
            session_options = {
                f"{s['id']} — {s['critter_id'].title()} — {s['started_at'][:16]}": s['id']
                for s in sessions
            }
            selected_label = st.selectbox("Select a session to view:", list(session_options.keys()))
            selected_id = session_options[selected_label]

            messages = get_session_messages(selected_id)
            if messages:
                for msg in messages:
                    critter_id = msg.get("critter_id", "pip")
                    c = get_critter(critter_id)
                    flag_int = msg.get("flagged", 0)
                    flag_label = ["", " ↩️", " ⚠️", " 🚨"][flag_int] if flag_int else ""

                    if msg["role"] == "user":
                        st.markdown(f"🧒 **You:** {msg['content']}{flag_label}")
                    else:
                        st.markdown(f"{c['emoji']} **{c['name']}:** {msg['content']}")
                    st.markdown(f"<span style='color:#ccc;font-size:0.75rem;'>{msg['timestamp'][:16]}</span>", unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No messages in this session.")

    # ── SAFETY ALERTS ─────────────────────────────────────────────────────────
    with tab_alerts:
        all_flags = get_all_flags(50)
        if not all_flags:
            st.success("✅ No safety flags — all clear!")
        else:
            for flag in all_flags:
                level = flag.get("flag_level", "redirect")
                color, label = FLAG_COLORS.get(level, ("#888", level))
                ack = flag.get("acknowledged", 0)

                with st.expander(
                    f"{label} — {flag['timestamp'][:16]}" + (" ✓" if ack else " 🔴 NEW"),
                    expanded=(not ack and level in ("alert", "crisis"))
                ):
                    st.markdown(f"**Level:** <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Reason:** {flag.get('reason', 'N/A')}")
                    st.markdown(f"**Note:** {flag.get('note', 'N/A')}")
                    if flag.get("message_content"):
                        st.markdown(f"**Message:** _{flag['message_content'][:200]}_")
                    if not ack:
                        if st.button("Mark as reviewed ✓", key=f"ack_{flag['id']}"):
                            acknowledge_flag(flag["id"])
                            st.rerun()

    # ── SETTINGS ──────────────────────────────────────────────────────────────
    with tab_settings:
        settings = get_all_settings()

        st.markdown("**Child Settings**")
        child_name = st.text_input("Child's name (used in greetings)", value=settings.get("child_name", "Friend"))
        if st.button("Save name"):
            set_setting("child_name", child_name)
            st.success("Saved!")

        st.divider()
        st.markdown("**Time Limits**")
        daily_limit = st.slider("Daily time limit (minutes)", 15, 120,
                                int(settings.get("daily_limit_min", 45)), step=5)
        col_r30, col_r60 = st.columns(2)
        with col_r30:
            remind_30 = st.checkbox("30-min wellness reminder", value=settings.get("reminder_30", "1") == "1")
        with col_r60:
            remind_60 = st.checkbox("60-min strong reminder", value=settings.get("reminder_60", "1") == "1")
        if st.button("Save time settings"):
            set_setting("daily_limit_min", str(daily_limit))
            set_setting("reminder_30", "1" if remind_30 else "0")
            set_setting("reminder_60", "1" if remind_60 else "0")
            st.success("Saved!")

        st.divider()
        st.markdown("**AI Settings**")
        prefer_local = st.checkbox(
            "Prefer local AI (Ollama) — most private",
            value=settings.get("llm_prefer_local", "1") == "1"
        )
        ollama_url = st.text_input("Ollama URL", value=settings.get("ollama_url", "http://localhost:11434"))
        gemini_key_set = "✅ Set" if settings.get("gemini_key_set") == "1" else "❌ Not set"
        st.markdown(f"Gemini API Key: **{gemini_key_set}** (set in .env file)")
        if st.button("Save AI settings"):
            set_setting("llm_prefer_local", "1" if prefer_local else "0")
            set_setting("ollama_url", ollama_url)
            st.success("Saved! Restart the app to apply Ollama URL changes.")

        st.divider()
        st.markdown("**Security**")
        new_pin = st.text_input("Change Parent PIN", type="password", max_chars=8, placeholder="New PIN...")
        confirm_pin = st.text_input("Confirm PIN", type="password", max_chars=8, placeholder="Confirm new PIN...")
        if st.button("Update PIN"):
            if new_pin and new_pin == confirm_pin and len(new_pin) >= 4:
                set_setting("parent_pin", new_pin)
                st.success("PIN updated!")
            else:
                st.error("PINs don't match or too short (min 4 characters).")
