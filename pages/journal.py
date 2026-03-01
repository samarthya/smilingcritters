"""
Smiling Critters — My Journal
Saved chat session cards. A keepsake for the child.
"""

import streamlit as st
from critters.personas import get_critter
from db.queries import get_journal_entries, get_session_messages


def render_journal():
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem;">📖</div>
        <h2 style="color: #6C3FC8; margin: 0.2rem 0;">My Journal</h2>
        <p style="color: #888;">All our chats, saved just for you!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back Home"):
        st.session_state.page = "home"
        st.session_state.pop("journal_view_session", None)
        st.rerun()

    st.markdown("---")

    # If viewing a specific past chat, show the full transcript
    if st.session_state.get("journal_view_session"):
        _render_transcript(st.session_state.journal_view_session)
        return

    # Load from DB (survives restarts); fall back to session_state for in-memory entries
    db_entries = get_journal_entries(limit=50)
    session_entries = st.session_state.get("journal_entries", [])

    # Merge: DB entries are authoritative; session entries fill in if DB is empty
    entries = db_entries if db_entries else session_entries

    if not entries:
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color: #aaa;">
            <div style="font-size: 3rem;">🌟</div>
            <p>No chats saved yet! Go have a chat with a critter and come back.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for entry in entries:
        with st.container():
            color    = entry.get("critter_color", "#6C3FC8")
            emoji    = entry.get("critter_emoji", "🐾")
            name     = entry.get("critter_name", "Critter")
            date_str = entry.get("date", "")
            time_str = entry.get("time", "")
            preview  = entry.get("preview", "")
            count    = entry.get("message_count", 0)
            dur      = entry.get("duration_min", 0)
            session_id = entry.get("session_id") or entry.get("sid")

            col_card, col_btn = st.columns([8, 1])
            with col_card:
                st.markdown(f"""
                <div style="
                    background: {color}11;
                    border-left: 5px solid {color};
                    border-radius: 10px;
                    padding: 1rem 1.2rem;
                    margin-bottom: 0.3rem;
                ">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:1.5rem;">{emoji}</span>
                            <strong style="color:{color}; margin-left:0.5rem;">Chat with {name}</strong>
                        </div>
                        <div style="color:#aaa; font-size:0.8rem;">{date_str} at {time_str}</div>
                    </div>
                    <div style="margin-top:0.5rem; color:#555; font-size:0.9rem;">"{preview}"</div>
                    <div style="margin-top:0.5rem; color:#aaa; font-size:0.78rem;">
                        💬 {count} messages &nbsp;·&nbsp; ⏱️ {dur} minutes
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                if session_id and st.button("📖", key=f"read_{session_id}_{date_str}", help="Read this chat again"):
                    st.session_state.journal_view_session = {
                        "session_id": session_id,
                        "critter_name": name,
                        "critter_color": color,
                        "critter_emoji": emoji,
                    }
                    st.rerun()


def _render_transcript(view: dict):
    """Show the full message log for a past session."""
    session_id   = view["session_id"]
    name         = view["critter_name"]
    color        = view["critter_color"]
    emoji        = view["critter_emoji"]

    if st.button("← Back to journal"):
        st.session_state.pop("journal_view_session", None)
        st.rerun()

    st.markdown(f"""
    <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
        <span style="font-size:2rem;">{emoji}</span>
        <h3 style="color:{color}; margin:0.2rem 0;">Chat with {name}</h3>
    </div>
    """, unsafe_allow_html=True)

    messages = get_session_messages(session_id)
    if not messages:
        st.info("No messages found for this chat.")
        return

    for msg in messages:
        role    = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            with st.chat_message("user", avatar="🧒"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar=emoji):
                st.markdown(
                    f'<div style="color:{color}; font-family:Nunito Sans,sans-serif;">{content}</div>',
                    unsafe_allow_html=True,
                )
