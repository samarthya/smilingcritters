"""
Smiling Critters — Global Theme & CSS
Warm, bubbly, child-friendly aesthetic with gentle animations.
Import and call apply_theme() at the top of app.py.
"""

CRITTER_SVGS = {
    "pip": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Hedgehog Pip -->
      <ellipse cx="60" cy="72" rx="38" ry="28" fill="#8B6914"/>
      <!-- Spines -->
      <ellipse cx="60" cy="50" rx="30" ry="32" fill="#5D4037"/>
      <ellipse cx="38" cy="45" rx="8" ry="18" fill="#4E342E" transform="rotate(-20,38,45)"/>
      <ellipse cx="50" cy="36" rx="8" ry="18" fill="#4E342E" transform="rotate(-8,50,36)"/>
      <ellipse cx="62" cy="33" rx="8" ry="18" fill="#4E342E"/>
      <ellipse cx="74" cy="36" rx="8" ry="18" fill="#4E342E" transform="rotate(8,74,36)"/>
      <ellipse cx="84" cy="45" rx="8" ry="18" fill="#4E342E" transform="rotate(20,84,45)"/>
      <!-- Face -->
      <ellipse cx="60" cy="72" rx="30" ry="24" fill="#FFCC80"/>
      <!-- Eyes -->
      <circle cx="50" cy="67" r="5" fill="#fff"/>
      <circle cx="70" cy="67" r="5" fill="#fff"/>
      <circle cx="51" cy="67" r="3" fill="#333"/>
      <circle cx="71" cy="67" r="3" fill="#333"/>
      <circle cx="52" cy="66" r="1" fill="#fff"/>
      <circle cx="72" cy="66" r="1" fill="#fff"/>
      <!-- Nose -->
      <ellipse cx="60" cy="75" rx="6" ry="4" fill="#E91E63"/>
      <!-- Smile -->
      <path d="M 52 80 Q 60 87 68 80" stroke="#5D4037" stroke-width="2" fill="none" stroke-linecap="round"/>
      <!-- Blush -->
      <circle cx="42" cy="74" r="6" fill="#FFB3C6" opacity="0.5"/>
      <circle cx="78" cy="74" r="6" fill="#FFB3C6" opacity="0.5"/>
      <!-- Star sparkle -->
      <text x="88" y="35" font-size="16">✨</text>
    </svg>""",

    "luna": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Butterfly Luna -->
      <!-- Left wings -->
      <ellipse cx="35" cy="52" rx="28" ry="22" fill="#CE93D8" transform="rotate(-25,35,52)" opacity="0.9"/>
      <ellipse cx="30" cy="75" rx="20" ry="15" fill="#F48FB1" transform="rotate(15,30,75)" opacity="0.9"/>
      <!-- Right wings -->
      <ellipse cx="85" cy="52" rx="28" ry="22" fill="#CE93D8" transform="rotate(25,85,52)" opacity="0.9"/>
      <ellipse cx="90" cy="75" rx="20" ry="15" fill="#F48FB1" transform="rotate(-15,90,75)" opacity="0.9"/>
      <!-- Wing patterns -->
      <circle cx="35" cy="50" r="8" fill="#fff" opacity="0.3"/>
      <circle cx="85" cy="50" r="8" fill="#fff" opacity="0.3"/>
      <!-- Body -->
      <ellipse cx="60" cy="65" rx="10" ry="25" fill="#6A1B9A"/>
      <!-- Head -->
      <circle cx="60" cy="42" r="18" fill="#F3E5F5"/>
      <!-- Antennae -->
      <line x1="54" y1="26" x2="44" y2="12" stroke="#6A1B9A" stroke-width="2"/>
      <circle cx="44" cy="12" r="3" fill="#E91E63"/>
      <line x1="66" y1="26" x2="76" y2="12" stroke="#6A1B9A" stroke-width="2"/>
      <circle cx="76" cy="12" r="3" fill="#E91E63"/>
      <!-- Eyes -->
      <circle cx="54" cy="42" r="5" fill="#fff"/>
      <circle cx="66" cy="42" r="5" fill="#fff"/>
      <circle cx="55" cy="42" r="3" fill="#4A148C"/>
      <circle cx="67" cy="42" r="3" fill="#4A148C"/>
      <circle cx="56" cy="41" r="1" fill="#fff"/>
      <circle cx="68" cy="41" r="1" fill="#fff"/>
      <!-- Gentle smile -->
      <path d="M 53 50 Q 60 56 67 50" stroke="#880E4F" stroke-width="2" fill="none" stroke-linecap="round"/>
      <!-- Blush -->
      <circle cx="46" cy="48" r="5" fill="#F48FB1" opacity="0.5"/>
      <circle cx="74" cy="48" r="5" fill="#F48FB1" opacity="0.5"/>
    </svg>""",

    "finn": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Fox Finn -->
      <!-- Tail -->
      <ellipse cx="95" cy="85" rx="20" ry="14" fill="#E07B39" transform="rotate(-30,95,85)"/>
      <ellipse cx="98" cy="80" rx="12" ry="8" fill="#fff" transform="rotate(-30,98,80)"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="28" ry="22" fill="#E07B39"/>
      <!-- Head -->
      <ellipse cx="60" cy="55" rx="28" ry="26" fill="#E07B39"/>
      <!-- Ears -->
      <polygon points="38,34 30,14 50,28" fill="#E07B39"/>
      <polygon points="40,34 34,18 48,28" fill="#FFB3C6"/>
      <polygon points="82,34 90,14 70,28" fill="#E07B39"/>
      <polygon points="80,34 86,18 72,28" fill="#FFB3C6"/>
      <!-- Face mask white -->
      <ellipse cx="60" cy="60" rx="20" ry="18" fill="#FFF8E1"/>
      <!-- Eyes -->
      <circle cx="52" cy="52" r="5" fill="#fff"/>
      <circle cx="68" cy="52" r="5" fill="#fff"/>
      <circle cx="53" cy="52" r="3.5" fill="#1A237E"/>
      <circle cx="69" cy="52" r="3.5" fill="#1A237E"/>
      <circle cx="54" cy="51" r="1" fill="#fff"/>
      <circle cx="70" cy="51" r="1" fill="#fff"/>
      <!-- Nose -->
      <ellipse cx="60" cy="62" rx="5" ry="3.5" fill="#333"/>
      <!-- Big grin -->
      <path d="M 50 68 Q 60 77 70 68" stroke="#5D3A00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <!-- Blush -->
      <circle cx="42" cy="60" r="6" fill="#FFB3C6" opacity="0.45"/>
      <circle cx="78" cy="60" r="6" fill="#FFB3C6" opacity="0.45"/>
      <!-- Sparkle -->
      <text x="86" y="28" font-size="14">🌟</text>
    </svg>""",

    "shelby": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Turtle Shelby -->
      <!-- Shell -->
      <ellipse cx="60" cy="68" rx="40" ry="32" fill="#2E7D32"/>
      <!-- Shell pattern -->
      <ellipse cx="60" cy="65" rx="24" ry="19" fill="#388E3C"/>
      <line x1="60" y1="46" x2="60" y2="84" stroke="#1B5E20" stroke-width="2" opacity="0.5"/>
      <line x1="36" y1="65" x2="84" y2="65" stroke="#1B5E20" stroke-width="2" opacity="0.5"/>
      <line x1="42" y1="50" x2="78" y2="80" stroke="#1B5E20" stroke-width="1.5" opacity="0.4"/>
      <line x1="78" y1="50" x2="42" y2="80" stroke="#1B5E20" stroke-width="1.5" opacity="0.4"/>
      <!-- Legs -->
      <ellipse cx="28" cy="80" rx="12" ry="8" fill="#66BB6A" transform="rotate(-20,28,80)"/>
      <ellipse cx="92" cy="80" rx="12" ry="8" fill="#66BB6A" transform="rotate(20,92,80)"/>
      <ellipse cx="35" cy="100" rx="10" ry="7" fill="#66BB6A" transform="rotate(10,35,100)"/>
      <ellipse cx="85" cy="100" rx="10" ry="7" fill="#66BB6A" transform="rotate(-10,85,100)"/>
      <!-- Head -->
      <circle cx="60" cy="40" r="22" fill="#66BB6A"/>
      <!-- Eyes - half closed, serene -->
      <circle cx="52" cy="38" r="5" fill="#fff"/>
      <circle cx="68" cy="38" r="5" fill="#fff"/>
      <circle cx="52" cy="39" r="3" fill="#1B5E20"/>
      <circle cx="68" cy="39" r="3" fill="#1B5E20"/>
      <!-- Serene eyelids -->
      <path d="M 47 37 Q 52 33 57 37" fill="#66BB6A"/>
      <path d="M 63 37 Q 68 33 73 37" fill="#66BB6A"/>
      <!-- Calm smile -->
      <path d="M 53 46 Q 60 51 67 46" stroke="#1B5E20" stroke-width="2" fill="none" stroke-linecap="round"/>
    </svg>""",

    "stella": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Star Stella -->
      <!-- Glow -->
      <circle cx="60" cy="60" r="45" fill="#FFF9C4" opacity="0.4"/>
      <!-- Star body -->
      <polygon points="60,8 72,45 110,45 80,68 92,105 60,83 28,105 40,68 10,45 48,45"
               fill="#F9A825"/>
      <!-- Inner star shine -->
      <polygon points="60,25 67,48 92,48 72,62 79,85 60,71 41,85 48,62 28,48 53,48"
               fill="#FFD54F"/>
      <!-- Face on star -->
      <!-- Eyes - wide and excited -->
      <circle cx="52" cy="58" r="6" fill="#fff"/>
      <circle cx="68" cy="58" r="6" fill="#fff"/>
      <circle cx="53" cy="58" r="4" fill="#1A237E"/>
      <circle cx="69" cy="58" r="4" fill="#1A237E"/>
      <circle cx="54" cy="57" r="1.5" fill="#fff"/>
      <circle cx="70" cy="57" r="1.5" fill="#fff"/>
      <!-- Big excited smile -->
      <path d="M 48 67 Q 60 78 72 67" stroke="#E65100" stroke-width="2.5" fill="#FFB300" stroke-linecap="round"/>
      <!-- Blush -->
      <circle cx="42" cy="65" r="6" fill="#FF8F00" opacity="0.35"/>
      <circle cx="78" cy="65" r="6" fill="#FF8F00" opacity="0.35"/>
      <!-- Sparkle dots -->
      <circle cx="20" cy="25" r="3" fill="#FFD54F"/>
      <circle cx="100" cy="20" r="4" fill="#FFF176"/>
      <circle cx="15" cy="80" r="2.5" fill="#FFD54F"/>
      <circle cx="105" cy="85" r="3" fill="#FFF176"/>
    </svg>""",
}


GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@400;600&display=swap');

/* ── Reset & base ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Nunito Sans', 'Segoe UI', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
    max-width: 960px;
}

/* ── Bubbly buttons ───────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 24px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    background: linear-gradient(135deg, #6C3FC8, #9B6FE8) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(108,63,200,0.25) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 6px 18px rgba(108,63,200,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) scale(0.99) !important;
}

/* ── Chat messages ────────────────────────────────────────────────────── */
.stChatMessage {
    border-radius: 20px !important;
    margin-bottom: 0.6rem !important;
}

/* ── Inputs ───────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stChatInputContainer textarea {
    border-radius: 16px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    border: 2px solid #E0D7F5 !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stChatInputContainer textarea:focus {
    border-color: #6C3FC8 !important;
    box-shadow: 0 0 0 3px rgba(108,63,200,0.12) !important;
}

/* ── Page background ──────────────────────────────────────────────────── */
.main {
    background: linear-gradient(160deg, #F8F4FF 0%, #FFF8F0 50%, #F0FFF8 100%);
    min-height: 100vh;
}

/* ── Critter card hover ───────────────────────────────────────────────── */
.critter-card {
    transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s ease;
    cursor: pointer;
}
.critter-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 12px 32px rgba(0,0,0,0.12) !important;
}

/* ── Animations ───────────────────────────────────────────────────────── */
@keyframes floatBounce {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
@keyframes sparkle {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(1.2) rotate(15deg); }
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.float-anim { animation: floatBounce 3s ease-in-out infinite; }
.sparkle-anim { animation: sparkle 2s ease-in-out infinite; }
.fade-in { animation: fadeSlideIn 0.4s ease forwards; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2D1B69 0%, #6C3FC8 100%) !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15) !important;
    box-shadow: none !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.25) !important;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* ── Divider ──────────────────────────────────────────────────────────── */
hr { border-color: #E8E0F5 !important; }

/* ── Metric cards ─────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Expander ─────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}
</style>
"""


def get_critter_svg(critter_id: str) -> str:
    return CRITTER_SVGS.get(critter_id, CRITTER_SVGS["pip"])


def apply_theme():
    """Call once at the top of app.py after st.set_page_config."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
