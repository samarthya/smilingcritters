"""
Smiling Critters — My Journal
Saved chat session cards. A keepsake for the child.
"""

import streamlit as st
from critters.personas import get_critter


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
        st.rerun()

    st.markdown("---")

    entries = st.session_state.get("journal_entries", [])

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
            st.markdown(f"""
            <div style="
                background: {entry.get('critter_color', '#6C3FC8')}11;
                border-left: 5px solid {entry.get('critter_color', '#6C3FC8')};
                border-radius: 10px;
                padding: 1rem 1.2rem;
                margin-bottom: 1rem;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:1.5rem;">{entry.get('critter_emoji','🐾')}</span>
                        <strong style="color:{entry.get('critter_color','#6C3FC8')}; margin-left:0.5rem;">
                            Chat with {entry.get('critter_name','Critter')}
                        </strong>
                    </div>
                    <div style="color:#aaa; font-size:0.8rem;">
                        {entry.get('date','')} at {entry.get('time','')}
                    </div>
                </div>
                <div style="margin-top:0.5rem; color:#555; font-size:0.9rem;">
                    "{entry.get('preview', '')}"
                </div>
                <div style="margin-top:0.5rem; color:#aaa; font-size:0.78rem;">
                    💬 {entry.get('message_count', 0)} messages &nbsp;·&nbsp; ⏱️ {entry.get('duration_min', 0)} minutes
                </div>
            </div>
            """, unsafe_allow_html=True)
