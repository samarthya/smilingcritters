"""
Smiling Critters — Home Screen (v4)
Uses st.components.v1.html() for the visual cards (always renders correctly)
and plain st.button() for interaction. No unsafe_allow_html needed for cards.
"""

import random
import streamlit as st
import streamlit.components.v1 as components
from critters.personas import get_all_critters
from db.queries import get_setting
from theme import get_critter_svg


def render_home():
    child_name = get_setting("child_name", "Friend")
    critters   = get_all_critters()

    # ── Greeting (simple markdown — always safe) ───────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 1.2rem 0 0.8rem 0;">
        <div style="
            font-family: 'Nunito', cursive;
            font-size: 2.4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #6C3FC8 0%, #E07B39 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
            margin-bottom: 0.2rem;
        ">Hi {child_name}! 🐾</div>
        <div style="font-size:1.05rem; color:#7B68A6; font-weight:600;">
            Who would you like to talk to today?
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Critter cards via components.html ─────────────────────────────────────
    # components.v1.html renders in an iframe — immune to Streamlit's sanitizer.
    card_htmls = []
    for i, critter in enumerate(critters):
        svg   = get_critter_svg(critter["id"])
        delay = i * 0.1
        card_htmls.append(f"""
        <div class="card" style="
            background: white;
            border-radius: 22px;
            padding: 1.2rem 0.8rem 1rem;
            text-align: center;
            border: 2.5px solid {critter['color']}25;
            box-shadow: 0 4px 18px {critter['color']}18;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.3rem;
            animation: fadeUp 0.45s ease both;
            animation-delay: {delay}s;
            cursor: default;
            transition: transform 0.22s cubic-bezier(.34,1.56,.64,1),
                        box-shadow 0.22s ease;
        "
        onmouseover="this.style.transform='translateY(-5px) scale(1.02)';this.style.boxShadow='0 12px 32px {critter['color']}35';"
        onmouseout="this.style.transform='none';this.style.boxShadow='0 4px 18px {critter['color']}18';">

            <div style="animation: floatBounce 3.2s ease-in-out infinite;
                        animation-delay:{delay + 0.4}s; width:90px;">
                {svg}
            </div>

            <div style="
                font-family: 'Nunito', sans-serif;
                font-size: 1.15rem;
                font-weight: 900;
                color: {critter['color']};
                margin-top: 0.1rem;
            ">{critter['name']}</div>

            <span style="
                font-size: 0.68rem;
                font-weight: 800;
                color: white;
                background: {critter['color']};
                border-radius: 20px;
                padding: 0.1rem 0.6rem;
                letter-spacing: 0.03em;
                white-space: nowrap;
            ">{critter['specialty']}</span>

            <div style="
                font-size: 0.76rem;
                color: #888;
                line-height: 1.4;
                padding: 0.05rem 0.1rem 0;
            ">{critter['description']}</div>
        </div>
        """)

    grid_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent; font-family: 'Nunito', sans-serif; }}

        .grid {{
            display: grid;
            grid-template-columns: repeat({len(critters)}, 1fr);
            gap: 10px;
            padding: 4px 2px;
        }}

        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(18px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes floatBounce {{
            0%, 100% {{ transform: translateY(0); }}
            50%       {{ transform: translateY(-7px); }}
        }}
    </style>
    </head>
    <body>
    <div class="grid">
        {''.join(card_htmls)}
    </div>
    </body>
    </html>
    """

    # height = card content height, no scrollbar
    components.html(grid_html, height=340, scrolling=False)

    # ── Chat buttons — plain Streamlit, no HTML needed ─────────────────────────
    cols = st.columns(len(critters), gap="small")
    for i, critter in enumerate(critters):
        with cols[i]:
            # Scoped CSS for this critter's button colour
            st.markdown(f"""
            <style>
            div[data-testid="column"]:nth-child({i+1}) div[data-testid="stButton"] button {{
                background: linear-gradient(135deg, {critter['color']}, {critter['color']}AA) !important;
                color: white !important;
                border-radius: 20px !important;
                font-weight: 700 !important;
                border: none !important;
                font-size: 0.88rem !important;
            }}
            div[data-testid="column"]:nth-child({i+1}) div[data-testid="stButton"] button:hover {{
                opacity: 0.88 !important;
                transform: translateY(-1px) !important;
            }}
            </style>
            """, unsafe_allow_html=True)

            if st.button(
                f"{critter['emoji']} {critter['name']}",
                key=f"pick_{critter['id']}",
                use_container_width=True,
            ):
                st.session_state.update({
                    "current_critter": critter["id"],
                    "page":            "chat",
                    "chat_messages":   [],
                    "session_id":      None,
                    "session_start":   None,
                    "wellness_shown":  set(),
                })
                st.rerun()

    # ── Journal + tip ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([2, 1, 2])
    with col_mid:
        if st.button("📖 My Journal", use_container_width=True):
            st.session_state.page = "journal"
            st.rerun()

    tips = [
        "💡 Pip loves helping with tricky homework!",
        "💜 Luna is great when you have big feelings.",
        "🌟 Ask Stella for an amazing fun fact!",
        "🐢 Shelby can help you feel calm and cosy.",
        "🦊 Finn wants to go on an adventure with you!",
    ]
    st.markdown(f"""
    <div style="text-align:center; margin-top:0.6rem;
                color:#B0A0CC; font-size:0.82rem; font-style:italic;">
        {random.choice(tips)}
    </div>
    """, unsafe_allow_html=True)
