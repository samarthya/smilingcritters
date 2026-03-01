"""
Smiling Critters — Home Screen (v5 — Carousel)
One critter shown at a time with animated slide-in.
Prev / Next arrows navigate; a big "Chat!" button starts the session.
"""

import streamlit as st
import streamlit.components.v1 as components
from critters.personas import get_all_critters
from db.queries import get_setting
from theme import get_critter_avatar, get_critter_icon_img, get_critter_pil_avatar


def _go_to_chat(critter_id: str):
    st.session_state.update({
        "current_critter": critter_id,
        "page":            "chat",
        "chat_messages":   [],
        "session_id":      None,
        "session_start":   None,
        "wellness_shown":  set(),
    })
    st.rerun()


def render_home():
    child_name = get_setting("child_name", "Friend")
    critters   = get_all_critters()
    n          = len(critters)

    # ── Carousel index ─────────────────────────────────────────────────────────
    if "home_idx" not in st.session_state:
        st.session_state.home_idx = 0
    idx     = st.session_state.home_idx
    critter = critters[idx]

    # ── Greeting ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding: 1.2rem 0 0.6rem 0;">
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

    # ── Dot indicators ─────────────────────────────────────────────────────────
    dots_html = "".join(
        f'<span style="display:inline-block; width:10px; height:10px; border-radius:50%; '
        f'margin:0 4px; background:{"" + critters[i]["color"] if i == idx else "#D1C4E9"}; '
        f'transition:background 0.3s;"></span>'
        for i in range(n)
    )
    st.markdown(
        f'<div style="text-align:center; margin-bottom:0.6rem;">{dots_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Featured card (iframe) + nav arrows ────────────────────────────────────
    svg = get_critter_avatar(critter["id"], size=140)

    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent; display: flex; justify-content: center; align-items: center; height: 100%; }}

        .card {{
            background: white;
            border-radius: 28px;
            padding: 2rem 2.5rem 1.8rem;
            text-align: center;
            border: 3px solid {critter['color']}30;
            box-shadow: 0 8px 32px {critter['color']}22;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.55rem;
            width: 320px;
            animation: slideIn 0.35s cubic-bezier(.34,1.46,.64,1) both;
        }}

        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(24px) scale(0.96); }}
            to   {{ opacity: 1; transform: translateY(0)    scale(1); }}
        }}
        @keyframes floatBounce {{
            0%, 100% {{ transform: translateY(0); }}
            50%       {{ transform: translateY(-10px); }}
        }}

        .avatar {{
            animation: floatBounce 3s ease-in-out infinite;
            width: 130px;
        }}
        .name {{
            font-family: 'Nunito', sans-serif;
            font-size: 1.6rem;
            font-weight: 900;
            color: {critter['color']};
        }}
        .badge {{
            font-size: 0.72rem;
            font-weight: 800;
            color: white;
            background: {critter['color']};
            border-radius: 20px;
            padding: 0.2rem 0.85rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .tagline {{
            font-family: 'Nunito Sans', sans-serif;
            font-size: 0.88rem;
            color: #666;
            line-height: 1.5;
            max-width: 240px;
        }}
    </style>
    </head>
    <body>
    <div class="card">
        <div class="avatar">{svg}</div>
        <div class="name">{critter['name']}</div>
        <span class="badge">{critter['specialty']}</span>
        <div class="tagline">{critter['description']}</div>
    </div>
    </body>
    </html>
    """

    col_prev, col_card, col_next = st.columns([1, 4, 1])

    with col_prev:
        st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)
        if st.button("◀", key="prev_critter", help="Previous critter", use_container_width=True):
            st.session_state.home_idx = (idx - 1) % n
            st.rerun()

    with col_card:
        components.html(card_html, height=380, scrolling=False)

    with col_next:
        st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)
        if st.button("▶", key="next_critter", help="Next critter", use_container_width=True):
            st.session_state.home_idx = (idx + 1) % n
            st.rerun()

    # ── Chat button ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <style>
    div[data-testid="stButton"][key="chat_with"] button,
    div[data-testid="stButton"] button[kind="primary"] {{
        background: linear-gradient(135deg, {critter['color']}, {critter['color']}BB) !important;
        color: white !important;
        border-radius: 24px !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        padding: 0.65rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 4px 16px {critter['color']}44 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    _, col_cta, _ = st.columns([2, 3, 2])
    with col_cta:
        # Show icon above the CTA button
        icon_html = get_critter_icon_img(critter["id"], size=36, style="display:block;margin:0 auto 4px auto;")
        if icon_html:
            st.markdown(f'<div style="text-align:center;">{icon_html}</div>', unsafe_allow_html=True)
        if st.button(
            f"Chat with {critter['name']}!",
            key="chat_with",
            use_container_width=True,
        ):
            _go_to_chat(critter["id"])

    # ── Quick-pick strip (all critters, small) ─────────────────────────────────
    st.markdown(
        '<div style="text-align:center; color:#B0A0CC; font-size:0.78rem; '
        'margin: 0.8rem 0 0.3rem;">or jump straight to</div>',
        unsafe_allow_html=True,
    )
    strip_cols = st.columns(n, gap="small")
    for i, c in enumerate(critters):
        with strip_cols[i]:
            is_active = i == idx
            st.markdown(f"""
            <style>
            div[data-testid="column"]:nth-child({i+1}) div[data-testid="stButton"] button {{
                background: {"linear-gradient(135deg," + c['color'] + "," + c['color'] + "AA)" if is_active else "rgba(108,63,200,0.08)"} !important;
                color: {"white" if is_active else c['color']} !important;
                border-radius: 18px !important;
                font-weight: 700 !important;
                border: {"none" if is_active else "1.5px solid " + c['color'] + "44"} !important;
                font-size: 0.8rem !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            # Icon above each strip button
            icon_html = get_critter_icon_img(c["id"], size=32, style="display:block;margin:0 auto 2px auto;")
            if icon_html:
                st.markdown(f'<div style="text-align:center;">{icon_html}</div>', unsafe_allow_html=True)
            if st.button(
                c["name"],
                key=f"strip_{c['id']}",
                use_container_width=True,
            ):
                if is_active:
                    _go_to_chat(c["id"])
                else:
                    st.session_state.home_idx = i
                    st.rerun()

    # ── Journal ────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_j, _ = st.columns([2, 1, 2])
    with col_j:
        if st.button("📖 My Journal", use_container_width=True):
            st.session_state.page = "journal"
            st.rerun()
