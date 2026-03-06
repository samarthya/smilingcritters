"""
Smiling Critters 🐾
A safe, joyful AI companion app for kids — Python/Streamlit prototype.
"""

# load_dotenv MUST be called before any other import that uses os.getenv()
from dotenv import load_dotenv
load_dotenv()

import time
import streamlit as st
from db.queries import init_db
from theme import apply_theme

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Smiling Critters 🐾",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global theme (Nunito fonts, sidebar gradient, animations, card hover) ──────
apply_theme()

# ── Initialise DB ─────────────────────────────────────────────────────────────
init_db()

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_critter" not in st.session_state:
    st.session_state.current_critter = "bubba"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "parent_authenticated" not in st.session_state:
    st.session_state.parent_authenticated = False
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# ── Secret knock state (hidden parent dashboard access) ───────────────────────
if "secret_taps" not in st.session_state:
    st.session_state.secret_taps = 0
if "secret_tap_t" not in st.session_state:
    st.session_state.secret_tap_t = 0.0

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🐾 Smiling Critters")
    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📖 My Journal", use_container_width=True):
        st.session_state.page = "journal"
        st.rerun()

    # ── Hidden gem — secret knock to open parent dashboard ────────────────────
    # The paw button looks like a decorative icon.
    # Click it 5× within 4 seconds to unlock the parent dashboard.
    # Parents know the pattern; children won't know to try.
    st.markdown("<br>" * 6, unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Make the secret paw look like a faint decorative icon, not a button */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: rgba(255,255,255,0.18) !important;
        font-size: 0.85rem !important;
        padding: 0.15rem 0.5rem !important;
        min-height: unset !important;
        width: auto !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type button:hover {
        background: transparent !important;
        box-shadow: none !important;
        transform: none !important;
        color: rgba(255,255,255,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🐾", key="secret_knock"):
        _now = time.time()
        _elapsed = _now - st.session_state.secret_tap_t
        if _elapsed > 4.0:
            st.session_state.secret_taps = 1   # timeout — restart count
        else:
            st.session_state.secret_taps += 1
        st.session_state.secret_tap_t = _now

        if st.session_state.secret_taps >= 5:
            st.session_state.secret_taps = 0
            st.session_state.page = "parent"
            st.rerun()

    # Barely-visible progress dots during the knock sequence
    taps = st.session_state.secret_taps
    if 0 < taps < 5:
        st.markdown(
            f'<div style="text-align:center; color:rgba(255,255,255,0.18); '
            f'font-size:0.5rem; letter-spacing:3px; margin-top:-0.3rem;">'
            f'{"●" * taps}{"○" * (5 - taps)}</div>',
            unsafe_allow_html=True,
        )

# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    from pages.home import render_home
    render_home()

elif page == "chat":
    from pages.chat import render_chat
    render_chat()

elif page == "journal":
    from pages.journal import render_journal
    render_journal()

elif page == "parent":
    from pages.parent_dashboard import render_parent_dashboard
    render_parent_dashboard()

else:
    st.session_state.page = "home"
    st.rerun()
