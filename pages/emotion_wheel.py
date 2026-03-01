"""
Smiling Critters — Emotion Wheel
Visual emotion picker for Luna's chat.
Returns the selected emotion string or None.
"""

import streamlit as st

# Emotions grouped by quadrant: (emoji, label, color, description)
EMOTIONS = {
    "Happy 😊": [
        ("😄", "Happy",     "#FFD700", "I feel good!"),
        ("🥰", "Loved",     "#FF69B4", "Warm and cared for"),
        ("🤩", "Excited",   "#FF8C00", "Can't wait!"),
        ("😌", "Peaceful",  "#98FB98", "Calm and okay"),
        ("😎", "Proud",     "#4169E1", "I did something great"),
        ("🤗", "Grateful",  "#DDA0DD", "Thankful"),
    ],
    "Sad 😢": [
        ("😢", "Sad",       "#6495ED", "Feeling blue"),
        ("😞", "Disappointed","#708090","Things didn't go my way"),
        ("😔", "Lonely",    "#9370DB", "Wish I had a friend"),
        ("😟", "Worried",   "#20B2AA", "Something might go wrong"),
        ("😿", "Hurt",      "#DC143C", "My feelings got hurt"),
        ("😩", "Tired",     "#A0A0A0", "Really low energy"),
    ],
    "Angry 😠": [
        ("😠", "Angry",     "#FF4500", "Really mad"),
        ("😤", "Frustrated","#FF6347", "It's not working!"),
        ("🙄", "Annoyed",   "#FFA07A", "Ugh, that's annoying"),
        ("😒", "Grumpy",    "#DAA520", "Not in the mood"),
        ("😡", "Furious",   "#DC143C", "REALLY mad"),
        ("😤", "Stubborn",  "#8B4513", "I don't want to"),
    ],
    "Scared 😨": [
        ("😨", "Scared",    "#4682B4", "Something feels scary"),
        ("😰", "Anxious",   "#5F9EA0", "My tummy hurts with worry"),
        ("😬", "Nervous",   "#66CDAA", "Butterflies inside"),
        ("🫣", "Shy",       "#9ACD32", "Hard to be seen"),
        ("😓", "Overwhelmed","#6A5ACD","Too much at once"),
        ("😳", "Surprised", "#FF7F50", "Didn't see that coming"),
    ],
}


def render_emotion_wheel(critter_id: str = "bobby") -> str | None:
    """
    Renders the emotion wheel UI.
    Returns the selected emotion label string, or None if nothing selected.
    """

    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;" class="fade-in">
        <div style="font-size:1.8rem;">🐻</div>
        <div style="font-family:'Nunito',sans-serif; font-size:1.2rem; font-weight:800; color:#E84040;">
            How are you feeling right now?
        </div>
        <div style="color:#aaa; font-size:0.85rem; margin-top:0.2rem;">
            Tap the feeling that's closest to yours
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected = None

    for group_name, emotions in EMOTIONS.items():
        group_color = {
            "Happy 😊":  "#FFD700",
            "Sad 😢":    "#6495ED",
            "Angry 😠":  "#FF4500",
            "Scared 😨": "#4682B4",
        }.get(group_name, "#888")

        st.markdown(f"""
        <div style="
            font-family:'Nunito',sans-serif;
            font-size:0.9rem;
            font-weight:800;
            color:{group_color};
            letter-spacing:0.04em;
            text-transform:uppercase;
            margin: 0.8rem 0 0.4rem 0.2rem;
        ">{group_name}</div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(emotions), gap="small")
        for i, (emoji, label, color, description) in enumerate(emotions):
            with cols[i]:
                # Highlight if currently selected
                is_selected = st.session_state.get("selected_emotion") == label
                border = f"3px solid {color}" if is_selected else f"2px solid {color}33"
                bg = f"{color}22" if is_selected else "white"

                st.markdown(f"""
                <div style="
                    background:{bg};
                    border:{border};
                    border-radius:16px;
                    padding:0.6rem 0.2rem;
                    text-align:center;
                    cursor:pointer;
                    transition:all 0.2s;
                ">
                    <div style="font-size:1.8rem;">{emoji}</div>
                    <div style="font-size:0.7rem; font-weight:700; color:#555; margin-top:0.2rem;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    label,
                    key=f"emotion_{label}_{group_name}",
                    use_container_width=True,
                    help=description,
                ):
                    st.session_state.selected_emotion = label
                    selected = label

    # If something was selected this render, show confirmation
    if selected or st.session_state.get("selected_emotion"):
        active = selected or st.session_state.get("selected_emotion")
        # Find the emotion details
        for emotions in EMOTIONS.values():
            for emoji, label, color, description in emotions:
                if label == active:
                    st.markdown(f"""
                    <div class="fade-in" style="
                        background: linear-gradient(135deg, {color}22, {color}11);
                        border: 2px solid {color}55;
                        border-radius: 20px;
                        padding: 1rem 1.5rem;
                        margin-top: 1rem;
                        text-align: center;
                    ">
                        <div style="font-size:2.5rem;">{emoji}</div>
                        <div style="font-family:'Nunito',sans-serif; font-size:1.1rem; font-weight:800; color:#555;">
                            You're feeling <span style="color:{color};">{label}</span>
                        </div>
                        <div style="color:#888; font-size:0.85rem; margin-top:0.3rem;">{description}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💬 Tell Bobby about it", use_container_width=True):
                            return label
                    with col2:
                        if st.button("↩️ Pick a different feeling", use_container_width=True):
                            st.session_state.selected_emotion = None
                            st.rerun()
                    break

    return selected if selected else None
