"""
Smiling Critters — Home / Critter Select Screen
The main landing page your daughter sees. Big, friendly, colourful critter cards.
"""

import streamlit as st
from critters.personas import get_all_critters
from db.queries import get_setting


def render_home():
    child_name = get_setting("child_name", "Friend")

    # ── Greeting ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 1.5rem 0 0.5rem 0;">
        <div style="font-size: 3.5rem; margin-bottom: 0.3rem;">🐾</div>
        <h1 style="font-size: 2.2rem; color: #6C3FC8; margin: 0; font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;">
            Hi {child_name}! 👋
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin-top: 0.4rem;">
            Who would you like to talk to today?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Critter cards ─────────────────────────────────────────────────────────
    critters = get_all_critters()
    cols = st.columns(len(critters), gap="medium")

    for i, critter in enumerate(critters):
        with cols[i]:
            # Card container
            st.markdown(f"""
            <div style="
                background: {critter['bg_color']};
                border-radius: 20px;
                padding: 1.5rem 1rem;
                text-align: center;
                border: 3px solid {critter['color']}33;
                margin-bottom: 0.5rem;
                min-height: 220px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">{critter['emoji']}</div>
                <div style="font-size: 1.3rem; font-weight: bold; color: {critter['color']}; margin-bottom: 0.2rem;">
                    {critter['name']}
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.6rem;">
                    {critter['tagline']}
                </div>
                <div style="font-size: 0.78rem; color: #555; line-height: 1.4;">
                    {critter['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"Chat with {critter['name']}! {critter['emoji']}",
                key=f"pick_{critter['id']}",
                use_container_width=True,
            ):
                st.session_state.current_critter = critter['id']
                st.session_state.page = "chat"
                # Clear any previous chat
                st.session_state.chat_messages = []
                st.session_state.session_id = None
                st.session_state.session_start = None
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Journal shortcut ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📖 My Journal", use_container_width=True):
            st.session_state.page = "journal"
            st.rerun()
