"""
Smiling Critters 🐾
A safe, joyful AI companion app for kids — Python/Streamlit prototype.
"""

import streamlit as st
from db.queries import init_db

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Smiling Critters 🐾",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Apply global theme ────────────────────────────────────────────────────────
from theme import apply_theme
apply_theme()

# ── Initialise DB ─────────────────────────────────────────────────────────────
init_db()

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "page":                "home",
    "current_critter":     "pip",
    "chat_messages":       [],
    "parent_authenticated": False,
    "journal_entries":     [],
    "show_emotion_wheel":  False,
    "selected_emotion":    None,
    "wellness_shown":      set(),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem 0;">
        <div style="font-size:2.5rem;">🐾</div>
        <div style="font-family:'Nunito',sans-serif; font-size:1.2rem;
                    font-weight:900; color:white; margin-top:0.2rem;">
            Smiling Critters
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    # Critter quick-pick in sidebar
    st.markdown("---")
    st.markdown('<div style="color:rgba(255,255,255,0.6); font-size:0.75rem; text-align:center; margin-bottom:0.4rem;">Quick Chat</div>', unsafe_allow_html=True)

    from critters.personas import get_all_critters
    for c in get_all_critters():
        if st.button(f"{c['emoji']} {c['name']}", use_container_width=True, key=f"sidebar_{c['id']}"):
            st.session_state.current_critter = c["id"]
            st.session_state.page            = "chat"
            st.session_state.chat_messages   = []
            st.session_state.session_id      = None
            st.session_state.session_start   = None
            st.session_state.wellness_shown  = set()
            st.rerun()

# ── Page router ───────────────────────────────────────────────────────────────
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
