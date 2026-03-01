"""
Smiling Critters — Global Theme & CSS
Warm, bubbly, child-friendly aesthetic with gentle animations.
Import and call apply_theme() at the top of app.py.
"""

CRITTER_SVGS = {
    "bubba": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Bubba Bubbaphant - Blue Elephant -->
      <!-- Big round ears -->
      <ellipse cx="22" cy="58" rx="18" ry="22" fill="#3AAAC8"/>
      <ellipse cx="98" cy="58" rx="18" ry="22" fill="#3AAAC8"/>
      <ellipse cx="22" cy="58" rx="11" ry="14" fill="#5BD0EE" opacity="0.6"/>
      <ellipse cx="98" cy="58" rx="11" ry="14" fill="#5BD0EE" opacity="0.6"/>
      <!-- Body -->
      <ellipse cx="60" cy="80" rx="32" ry="26" fill="#4DBDE0"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#4DBDE0"/>
      <!-- Trunk -->
      <path d="M 55 78 Q 48 90 52 100 Q 56 108 62 100 Q 66 92 60 78" fill="#3AAAC8"/>
      <!-- Eyes -->
      <circle cx="48" cy="48" r="7" fill="#fff"/>
      <circle cx="72" cy="48" r="7" fill="#fff"/>
      <circle cx="49" cy="48" r="4" fill="#1A237E"/>
      <circle cx="73" cy="48" r="4" fill="#1A237E"/>
      <circle cx="50" cy="47" r="1.5" fill="#fff"/>
      <circle cx="74" cy="47" r="1.5" fill="#fff"/>
      <!-- Big Smiling Critters grin -->
      <path d="M 42 62 Q 60 80 78 62 Z" fill="#1A1A1A"/>
      <path d="M 44 62 Q 60 74 76 62" fill="white" stroke="none"/>
      <!-- Lightbulb emblem on belly -->
      <circle cx="60" cy="85" r="7" fill="#FFE040"/>
      <rect x="57" y="88" width="6" height="4" rx="1" fill="#B8860B"/>
      <path d="M 56 85 Q 60 79 64 85" fill="#FFE040" stroke="#B8860B" stroke-width="1"/>
      <!-- Blush -->
      <circle cx="36" cy="60" r="7" fill="#AEE4EF" opacity="0.5"/>
      <circle cx="84" cy="60" r="7" fill="#AEE4EF" opacity="0.5"/>
    </svg>""",

    "bobby": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Bobby Bearhug - Red Bear -->
      <!-- Bear ears -->
      <circle cx="34" cy="26" r="14" fill="#C53030"/>
      <circle cx="86" cy="26" r="14" fill="#C53030"/>
      <circle cx="34" cy="26" r="8" fill="#E84040"/>
      <circle cx="86" cy="26" r="8" fill="#E84040"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#E84040"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#E84040"/>
      <!-- Muzzle -->
      <ellipse cx="60" cy="62" rx="18" ry="13" fill="#C53030" opacity="0.5"/>
      <!-- Eyes -->
      <circle cx="48" cy="46" r="7" fill="#fff"/>
      <circle cx="72" cy="46" r="7" fill="#fff"/>
      <circle cx="49" cy="46" r="4" fill="#1A1A1A"/>
      <circle cx="73" cy="46" r="4" fill="#1A1A1A"/>
      <circle cx="50" cy="45" r="1.5" fill="#fff"/>
      <circle cx="74" cy="45" r="1.5" fill="#fff"/>
      <!-- Nose -->
      <ellipse cx="60" cy="60" rx="5" ry="3.5" fill="#1A1A1A"/>
      <!-- Big Smiling Critters grin -->
      <path d="M 42 66 Q 60 84 78 66 Z" fill="#1A1A1A"/>
      <path d="M 44 66 Q 60 78 76 66" fill="white" stroke="none"/>
      <!-- Heart emblem on belly -->
      <path d="M 60 88 C 60 88 52 82 52 78 C 52 74 60 76 60 76 C 60 76 68 74 68 78 C 68 82 60 88 60 88 Z" fill="#fff" opacity="0.9"/>
      <!-- Blush -->
      <circle cx="36" cy="58" r="7" fill="#FFB3B3" opacity="0.5"/>
      <circle cx="84" cy="58" r="7" fill="#FFB3B3" opacity="0.5"/>
    </svg>""",

    "dogday": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- DogDay - Orange Dog -->
      <!-- Floppy ears -->
      <ellipse cx="28" cy="50" rx="14" ry="28" fill="#C35F1A" transform="rotate(-15,28,50)"/>
      <ellipse cx="92" cy="50" rx="14" ry="28" fill="#C35F1A" transform="rotate(15,92,50)"/>
      <ellipse cx="28" cy="50" rx="8" ry="20" fill="#E88030" opacity="0.7" transform="rotate(-15,28,50)"/>
      <ellipse cx="92" cy="50" rx="8" ry="20" fill="#E88030" opacity="0.7" transform="rotate(15,92,50)"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#E07B39"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#E07B39"/>
      <!-- Muzzle -->
      <ellipse cx="60" cy="62" rx="18" ry="13" fill="#FFF0E6"/>
      <!-- Eyes -->
      <circle cx="48" cy="45" r="7" fill="#fff"/>
      <circle cx="72" cy="45" r="7" fill="#fff"/>
      <circle cx="49" cy="45" r="4" fill="#1A1A1A"/>
      <circle cx="73" cy="45" r="4" fill="#1A1A1A"/>
      <circle cx="50" cy="44" r="1.5" fill="#fff"/>
      <circle cx="74" cy="44" r="1.5" fill="#fff"/>
      <!-- Nose -->
      <ellipse cx="60" cy="59" rx="5" ry="3.5" fill="#333"/>
      <!-- Big grin -->
      <path d="M 42 66 Q 60 84 78 66 Z" fill="#1A1A1A"/>
      <path d="M 44 66 Q 60 78 76 66" fill="white" stroke="none"/>
      <!-- Sunflower emblem -->
      <circle cx="60" cy="86" r="6" fill="#FFD700"/>
      <circle cx="60" cy="86" r="3" fill="#B8860B"/>
      <ellipse cx="60" cy="79" rx="2.5" ry="4" fill="#FFD700"/>
      <ellipse cx="60" cy="93" rx="2.5" ry="4" fill="#FFD700"/>
      <ellipse cx="53" cy="86" rx="4" ry="2.5" fill="#FFD700"/>
      <ellipse cx="67" cy="86" rx="4" ry="2.5" fill="#FFD700"/>
      <!-- Blush -->
      <circle cx="36" cy="56" r="7" fill="#FFD4A8" opacity="0.5"/>
      <circle cx="84" cy="56" r="7" fill="#FFD4A8" opacity="0.5"/>
    </svg>""",

    "catnap": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- CatNap - Purple Cat -->
      <!-- Pointy cat ears -->
      <polygon points="36,30 26,8 52,26" fill="#7048B8"/>
      <polygon points="38,28 32,14 50,26" fill="#A070D0" opacity="0.7"/>
      <polygon points="84,30 94,8 68,26" fill="#7048B8"/>
      <polygon points="82,28 88,14 70,26" fill="#A070D0" opacity="0.7"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#8B5BD4"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#8B5BD4"/>
      <!-- Tail -->
      <path d="M 85 90 Q 108 75 105 55 Q 102 42 95 48" stroke="#7048B8" stroke-width="8" fill="none" stroke-linecap="round"/>
      <!-- Muzzle -->
      <ellipse cx="60" cy="62" rx="16" ry="12" fill="#A070D0" opacity="0.4"/>
      <!-- Sleepy half-closed eyes -->
      <circle cx="48" cy="47" r="7" fill="#fff"/>
      <circle cx="72" cy="47" r="7" fill="#fff"/>
      <circle cx="49" cy="48" r="4" fill="#2D1B69"/>
      <circle cx="73" cy="48" r="4" fill="#2D1B69"/>
      <!-- Sleepy eyelids -->
      <path d="M 41 47 Q 48 41 55 47" fill="#8B5BD4"/>
      <path d="M 65 47 Q 72 41 79 47" fill="#8B5BD4"/>
      <!-- Nose -->
      <polygon points="60,60 57,63 63,63" fill="#E91E63"/>
      <!-- Peaceful smile -->
      <path d="M 44 66 Q 60 80 76 66 Z" fill="#1A1A1A"/>
      <path d="M 46 66 Q 60 76 74 66" fill="white" stroke="none"/>
      <!-- "C" emblem -->
      <path d="M 66 84 A 7 7 0 1 0 66 92" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- Blush -->
      <circle cx="36" cy="58" r="6" fill="#D4AAFF" opacity="0.45"/>
      <circle cx="84" cy="58" r="6" fill="#D4AAFF" opacity="0.45"/>
      <!-- ZZZ -->
      <text x="88" y="28" font-size="11" fill="#C0A0E8" font-weight="bold">z</text>
      <text x="94" y="20" font-size="9" fill="#C0A0E8" font-weight="bold">z</text>
    </svg>""",

    "kickin": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- KickinChicken - Yellow Chicken -->
      <!-- Red comb on top -->
      <ellipse cx="52" cy="22" rx="7" ry="11" fill="#E53935" transform="rotate(-15,52,22)"/>
      <ellipse cx="60" cy="18" rx="7" ry="13" fill="#E53935"/>
      <ellipse cx="68" cy="22" rx="7" ry="11" fill="#E53935" transform="rotate(15,68,22)"/>
      <!-- Wings -->
      <ellipse cx="22" cy="68" rx="14" ry="22" fill="#E6C000" transform="rotate(-20,22,68)"/>
      <ellipse cx="98" cy="68" rx="14" ry="22" fill="#E6C000" transform="rotate(20,98,68)"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#FFD700"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#FFD700"/>
      <!-- Beak -->
      <polygon points="60,62 50,68 70,68" fill="#E65100"/>
      <polygon points="60,68 50,68 70,68" fill="#BF360C" opacity="0.6"/>
      <!-- Wattle (red chin) -->
      <ellipse cx="60" cy="74" rx="7" ry="5" fill="#E53935"/>
      <!-- Eyes -->
      <circle cx="47" cy="46" r="7" fill="#fff"/>
      <circle cx="73" cy="46" r="7" fill="#fff"/>
      <circle cx="48" cy="46" r="4" fill="#1A1A1A"/>
      <circle cx="74" cy="46" r="4" fill="#1A1A1A"/>
      <circle cx="49" cy="45" r="1.5" fill="#fff"/>
      <circle cx="75" cy="45" r="1.5" fill="#fff"/>
      <!-- Big grin above beak -->
      <path d="M 43 58 Q 60 72 77 58 Z" fill="#1A1A1A"/>
      <path d="M 45 58 Q 60 68 75 58" fill="white" stroke="none"/>
      <!-- Blush -->
      <circle cx="34" cy="56" r="7" fill="#FFE066" opacity="0.5"/>
      <circle cx="86" cy="56" r="7" fill="#FFE066" opacity="0.5"/>
      <!-- Sparkle -->
      <text x="88" y="28" font-size="14">&#x2728;</text>
    </svg>""",

    "hoppy": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- Hoppy Hopscotch - Green Rabbit -->
      <!-- Long tall ears -->
      <ellipse cx="44" cy="22" rx="10" ry="26" fill="#1DAA1D"/>
      <ellipse cx="76" cy="22" rx="10" ry="26" fill="#1DAA1D"/>
      <ellipse cx="44" cy="22" rx="5" ry="20" fill="#A8EDA8" opacity="0.6"/>
      <ellipse cx="76" cy="22" rx="5" ry="20" fill="#A8EDA8" opacity="0.6"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#3ECF3E"/>
      <!-- Head -->
      <circle cx="60" cy="56" r="28" fill="#3ECF3E"/>
      <!-- Muzzle -->
      <ellipse cx="60" cy="64" rx="14" ry="10" fill="#A8EDA8" opacity="0.5"/>
      <!-- Eyes -->
      <circle cx="49" cy="50" r="7" fill="#fff"/>
      <circle cx="71" cy="50" r="7" fill="#fff"/>
      <circle cx="50" cy="50" r="4" fill="#1A1A1A"/>
      <circle cx="72" cy="50" r="4" fill="#1A1A1A"/>
      <circle cx="51" cy="49" r="1.5" fill="#fff"/>
      <circle cx="73" cy="49" r="1.5" fill="#fff"/>
      <!-- Nose -->
      <ellipse cx="60" cy="62" rx="4" ry="3" fill="#E91E63"/>
      <!-- Big grin -->
      <path d="M 44 68 Q 60 86 76 68 Z" fill="#1A1A1A"/>
      <path d="M 46 68 Q 60 80 74 68" fill="white" stroke="none"/>
      <!-- Lightning bolt emblem -->
      <polygon points="63,77 57,86 62,86 57,95 67,84 61,84" fill="#FFD700"/>
      <!-- Blush -->
      <circle cx="36" cy="60" r="7" fill="#A8F0A8" opacity="0.5"/>
      <circle cx="84" cy="60" r="7" fill="#A8F0A8" opacity="0.5"/>
    </svg>""",

    "piggy": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- PickyPiggy - Pink Pig -->
      <!-- Bow on top -->
      <polygon points="48,20 60,28 48,36" fill="#E8589A"/>
      <polygon points="72,20 60,28 72,36" fill="#E8589A"/>
      <circle cx="60" cy="28" r="5" fill="#FF80B4"/>
      <!-- Round pig ears -->
      <circle cx="34" cy="32" r="12" fill="#E8589A"/>
      <circle cx="34" cy="32" r="7" fill="#FF80B4" opacity="0.6"/>
      <circle cx="86" cy="32" r="12" fill="#E8589A"/>
      <circle cx="86" cy="32" r="7" fill="#FF80B4" opacity="0.6"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#F879A4"/>
      <!-- Head -->
      <circle cx="60" cy="54" r="28" fill="#F879A4"/>
      <!-- Snout -->
      <ellipse cx="60" cy="64" rx="16" ry="12" fill="#E8589A"/>
      <circle cx="55" cy="64" r="4" fill="#C0356E" opacity="0.5"/>
      <circle cx="65" cy="64" r="4" fill="#C0356E" opacity="0.5"/>
      <!-- Eyes -->
      <circle cx="48" cy="48" r="7" fill="#fff"/>
      <circle cx="72" cy="48" r="7" fill="#fff"/>
      <circle cx="49" cy="48" r="4" fill="#1A1A1A"/>
      <circle cx="73" cy="48" r="4" fill="#1A1A1A"/>
      <circle cx="50" cy="47" r="1.5" fill="#fff"/>
      <circle cx="74" cy="47" r="1.5" fill="#fff"/>
      <!-- Big grin -->
      <path d="M 43 70 Q 60 86 77 70 Z" fill="#1A1A1A"/>
      <path d="M 45 70 Q 60 80 75 70" fill="white" stroke="none"/>
      <!-- Apple emblem -->
      <circle cx="60" cy="88" r="6" fill="#E53935"/>
      <path d="M 60 82 Q 63 79 66 83" stroke="#388E3C" stroke-width="2" fill="none"/>
      <!-- Blush -->
      <circle cx="36" cy="58" r="7" fill="#FFC0D0" opacity="0.5"/>
      <circle cx="84" cy="58" r="7" fill="#FFC0D0" opacity="0.5"/>
    </svg>""",

    "crafty": """
    <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="90" height="90">
      <!-- CraftyCorn - Unicorn -->
      <!-- Rainbow mane -->
      <ellipse cx="38" cy="36" rx="10" ry="18" fill="#FF6B6B" transform="rotate(-20,38,36)"/>
      <ellipse cx="44" cy="30" rx="9" ry="16" fill="#FF9F43" transform="rotate(-10,44,30)"/>
      <ellipse cx="52" cy="26" rx="8" ry="15" fill="#FFE033" transform="rotate(0,52,26)"/>
      <!-- Horn (rainbow tip) -->
      <polygon points="60,5 54,30 66,30" fill="#29C9E0"/>
      <polygon points="60,5 55,20 65,20" fill="#A8EFFF"/>
      <!-- Body -->
      <ellipse cx="60" cy="82" rx="30" ry="24" fill="#E8FAFD"/>
      <!-- Head -->
      <circle cx="60" cy="52" r="30" fill="#FFFFFF"/>
      <!-- Rainbow badge on belly -->
      <path d="M 50 84 Q 60 78 70 84" stroke="#E53935" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 49 87 Q 60 80 71 87" stroke="#FF9800" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 50 90 Q 60 84 70 90" stroke="#4CAF50" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 51 93 Q 60 88 69 93" stroke="#2196F3" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- Eyes -->
      <circle cx="48" cy="48" r="7" fill="#fff"/>
      <circle cx="72" cy="48" r="7" fill="#fff"/>
      <circle cx="49" cy="48" r="4" fill="#1A237E"/>
      <circle cx="73" cy="48" r="4" fill="#1A237E"/>
      <circle cx="50" cy="47" r="1.5" fill="#fff"/>
      <circle cx="74" cy="47" r="1.5" fill="#fff"/>
      <!-- Big grin -->
      <path d="M 42 62 Q 60 80 78 62 Z" fill="#1A1A1A"/>
      <path d="M 44 62 Q 60 74 76 62" fill="white" stroke="none"/>
      <!-- Blush -->
      <circle cx="36" cy="56" r="7" fill="#B8F0F8" opacity="0.6"/>
      <circle cx="84" cy="56" r="7" fill="#B8F0F8" opacity="0.6"/>
      <!-- Sparkles -->
      <text x="86" y="30" font-size="12">&#x2728;</text>
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
    return CRITTER_SVGS.get(critter_id, CRITTER_SVGS["bubba"])


def get_critter_avatar(critter_id: str, size: int = 140) -> str:
    """
    Returns an HTML image tag for the critter.
    Prefers the real PNG sprite from assets/sprites/{id}.png when it exists;
    falls back to the inline SVG so the app works before sprites are extracted.
    """
    import base64
    import os

    sprite_path = os.path.join(
        os.path.dirname(__file__), "assets", "sprites", f"{critter_id}.png"
    )

    if os.path.isfile(sprite_path):
        with open(sprite_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return (
            f'<img src="data:image/png;base64,{data}" '
            f'width="{size}" height="{size}" '
            f'style="object-fit:contain; image-rendering:auto;" '
            f'alt="{critter_id}" />'
        )

    # Fallback: inline SVG at the requested size
    svg = CRITTER_SVGS.get(critter_id, CRITTER_SVGS["bubba"])
    # Patch the width/height attributes in the SVG
    import re
    svg = re.sub(r'width="\d+"', f'width="{size}"', svg)
    svg = re.sub(r'height="\d+"', f'height="{size}"', svg)
    return svg


def get_critter_icon_b64(critter_id: str) -> str:
    """
    Returns a base64-encoded PNG data URI string for the 48px icon.
    Used to build <img src="..."> tags in HTML blocks.
    Falls back to the 200px sprite, then to None (caller should handle).
    """
    import base64, os
    for subdir in ("icons", "sprites"):
        path = os.path.join(os.path.dirname(__file__), "assets", subdir, f"{critter_id}.png")
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""


def get_critter_icon_img(critter_id: str, size: int = 28, style: str = "") -> str:
    """
    Returns a complete <img> HTML tag for an inline icon.
    size  — rendered px size (CSS width/height)
    style — any extra inline CSS (e.g. 'vertical-align:middle; margin-right:4px;')
    Falls back to the emoji from CRITTERS if no PNG is available.
    """
    b64 = get_critter_icon_b64(critter_id)
    if b64:
        base_style = f"width:{size}px;height:{size}px;object-fit:contain;vertical-align:middle;"
        return f'<img src="data:image/png;base64,{b64}" style="{base_style}{style}" alt="" />'
    # Fallback: blank (caller keeps its own emoji)
    return ""


def get_critter_pil_avatar(critter_id: str):
    """
    Returns a PIL Image object for use as a Streamlit chat_message avatar.
    Streamlit accepts PIL.Image.Image directly in st.chat_message(avatar=...).
    Falls back to None (Streamlit will use a generic avatar) if PIL/file unavailable.
    """
    try:
        from PIL import Image
        import os
        for subdir in ("icons", "sprites"):
            path = os.path.join(os.path.dirname(__file__), "assets", subdir, f"{critter_id}.png")
            if os.path.isfile(path):
                img = Image.open(path).convert("RGBA")
                img.thumbnail((48, 48))
                return img
    except Exception:
        pass
    return None


def apply_theme():
    """Call once at the top of app.py after st.set_page_config."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
