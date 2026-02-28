"""
Smiling Critters — Home / Critter Select Screen (v2)
Beautiful SVG critter cards with animations and warm design.
"""

import streamlit as st
from critters.personas import get_all_critters
from db.queries import get_setting
from theme import get_critter_svg


def render_home():
    child_name = get_setting("child_name", "Friend")
    critters   = get_all_critters()

    # ── Hero greeting ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="fade-in" style="text-align:center; padding: 1.5rem 0 1rem 0;">
        <div style="
            font-family: 'Nunito', cursive;
            font-size: 2.6rem;
            font-weight: 900;
            background: linear-gradient(135deg, #6C3FC8 0%, #E07B39 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
            line-height: 1.1;
        ">
            Hi {child_name}! 🐾
        </div>
        <div style="
            font-size: 1.15rem;
            color: #7B68A6;
            font-family: 'Nunito Sans', sans-serif;
            font-weight: 600;
        ">
            Who would you like to talk to today?
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Critter grid ───────────────────────────────────────────────────────────
    cols = st.columns(len(critters), gap="small")

    for i, critter in enumerate(critters):
        with cols[i]:
            svg = get_critter_svg(critter["id"])
            # Staggered animation delay
            delay = i * 0.08

            st.markdown(f"""
            <div class="critter-card fade-in" style="
                background: white;
                border-radius: 24px;
                padding: 1.4rem 0.8rem 1rem 0.8rem;
                text-align: center;
                border: 2.5px solid {critter['color']}22;
                box-shadow: 0 4px 20px {critter['color']}18;
                min-height: 280px;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.4rem;
                animation-delay: {delay}s;
            ">
                <div class="float-anim" style="animation-delay: {delay + 0.3}s;">
                    {svg}
                </div>

                <div style="
                    font-family: 'Nunito', sans-serif;
                    font-size: 1.25rem;
                    font-weight: 900;
                    color: {critter['color']};
                    margin-top: 0.2rem;
                ">
                    {critter['name']}
                </div>

                <div style="
                    font-size: 0.75rem;
                    font-weight: 700;
                    color: white;
                    background: {critter['color']};
                    border-radius: 20px;
                    padding: 0.15rem 0.7rem;
                    letter-spacing: 0.03em;
                ">
                    {critter['specialty']}
                </div>

                <div style="
                    font-size: 0.78rem;
                    color: #888;
                    line-height: 1.4;
                    padding: 0 0.2rem;
                ">
                    {critter['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Inject per-critter button colour using a unique key class
            st.markdown(f"""
            <style>
            [data-testid="stButton"] button[kind="secondary"]#btn_{critter['id']},
            div.critter-btn-{critter['id']} button {{
                background: linear-gradient(135deg, {critter['color']}, {critter['color']}CC) !important;
            }}
            </style>
            <div class="critter-btn-{critter['id']}">
            """, unsafe_allow_html=True)

            if st.button(
                f"Chat with {critter['name']}! {critter['emoji']}",
                key=f"pick_{critter['id']}",
                use_container_width=True,
            ):
                st.session_state.current_critter = critter["id"]
                st.session_state.page            = "chat"
                st.session_state.chat_messages   = []
                st.session_state.session_id      = None
                st.session_state.session_start   = None
                st.session_state.wellness_shown  = set()
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # ── Bottom nav ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📖 My Journal", use_container_width=True):
            st.session_state.page = "journal"
            st.rerun()

    # ── Fun footer tip ─────────────────────────────────────────────────────────
    tips = [
        "💡 Pip loves helping with tricky homework!",
        "💜 Luna is great when you have big feelings.",
        "🌟 Ask Stella for an amazing fun fact!",
        "🐢 Shelby can help you feel calm and cosy.",
        "🦊 Finn wants to go on an adventure with you!",
    ]
    import random
    tip = random.choice(tips)
    st.markdown(f"""
    <div style="text-align:center; margin-top:1rem; color:#B0A0CC; font-size:0.82rem; font-style:italic;">
        {tip}
    </div>
    """, unsafe_allow_html=True)
