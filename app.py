"""
Smiling Critters 🐾
A safe, joyful AI companion app for kids — Python/Streamlit prototype.
"""

# load_dotenv MUST be called before any other import that uses os.getenv()
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from db.queries import init_db

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Smiling Critters 🐾",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; max-width: 900px; }

    /* Friendly font feel */
    body, .stMarkdown { font-family: 'Segoe UI', 'Arial Rounded MT Bold', Arial, sans-serif; }

    /* Rounder buttons */
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
        transition: transform 0.1s;
    }
    .stButton > button:hover { transform: scale(1.02); }

    /* Critter chat bubble override */
    .stChatMessage { border-radius: 16px; }

    /* Softer inputs */
    .stTextInput > div > div > input {
        border-radius: 12px;
    }

    /* Chat input */
    .stChatInputContainer { border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

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

# ── Sidebar navigation (parent access, minimal) ───────────────────────────────
with st.sidebar:
    st.markdown("### 🐾 Smiling Critters")
    st.markdown("---")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📖 My Journal", use_container_width=True):
        st.session_state.page = "journal"
        st.rerun()
    st.markdown("---")
    if st.button("👨‍👧 Parent Dashboard", use_container_width=True):
        st.session_state.page = "parent"
        st.rerun()

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
