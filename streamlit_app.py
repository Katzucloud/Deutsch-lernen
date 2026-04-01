import streamlit as st
import google.generativeai as genai
import json
import re
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deutsch Lernen",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark theme CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Serif+Display&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #1a1a1a !important;
    color: #ececec !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #141414 !important;
    border-right: 1px solid #2e2e2e;
}
h1 {
    font-family: 'DM Serif Display', serif !important;
    color: #f5f5f0 !important;
    font-size: 42px !important;
    letter-spacing: -0.5px !important;
}
h2, h3 {
    font-family: 'Inter', sans-serif !important;
    color: #e0e0e0 !important;
}

/* ── Phrase card — Claude warm amber accent ── */
.phrase-card {
    background: #212121;
    border: 1px solid #333;
    border-left: 4px solid #d4956a;
    border-radius: 14px;
    padding: 28px 32px;
    margin: 14px 0 20px 0;
}
.phrase-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: #d4956a; margin-bottom: 14px;
}
.phrase-text {
    font-family: 'Inter', sans-serif;
    font-size: 22px; font-weight: 500;
    color: #f0ede8; line-height: 1.55; margin: 0;
}
.phrase-meta {
    font-size: 12px; color: #666; margin-top: 12px;
    font-family: 'JetBrains Mono', monospace;
}
.grammar-tag {
    display: inline-block;
    background: #d4956a18; color: #d4956a;
    border: 1px solid #d4956a33;
    border-radius: 6px; padding: 2px 10px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    margin-right: 6px;
}
.topic-tag {
    display: inline-block;
    background: #7eb8d418; color: #7eb8d4;
    border: 1px solid #7eb8d433;
    border-radius: 6px; padding: 2px 10px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
}

/* ── Mode badge ── */
.mode-badge {
    display: inline-block;
    background: #2a2a2a; color: #aaa;
    border: 1px solid #3a3a3a; border-radius: 20px;
    padding: 4px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: 1px; margin-bottom: 8px;
}

/* ── Buttons — each with its own pastel colour ── */
/* New Phrase — pastel teal */
div[data-testid="column"]:nth-of-type(1) .stButton > button {
    background: #1e2e2c !important;
    color: #80cbc4 !important;
    border: 1px solid #80cbc455 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"]:nth-of-type(1) .stButton > button:hover {
    background: #80cbc4 !important; color: #0e1f1e !important;
    border-color: #80cbc4 !important;
}

/* Flip — pastel lavender */
div[data-testid="column"]:nth-of-type(2) .stButton > button {
    background: #1f1e2e !important;
    color: #b39ddb !important;
    border: 1px solid #b39ddb55 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
    background: #b39ddb !important; color: #1a1428 !important;
    border-color: #b39ddb !important;
}

/* Check — pastel green */
div[data-testid="column"]:nth-of-type(3) .stButton > button {
    background: #1a2a1e !important;
    color: #a5d6a7 !important;
    border: 1px solid #a5d6a755 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"]:nth-of-type(3) .stButton > button:hover {
    background: #a5d6a7 !important; color: #0e1f12 !important;
    border-color: #a5d6a7 !important;
}

/* Reveal — pastel peach/amber */
div[data-testid="column"]:nth-of-type(4) .stButton > button {
    background: #2a2018 !important;
    color: #ffcc80 !important;
    border: 1px solid #ffcc8055 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"]:nth-of-type(4) .stButton > button:hover {
    background: #ffcc80 !important; color: #1a1000 !important;
    border-color: #ffcc80 !important;
}

/* Save — pastel rose */
div[data-testid="column"]:nth-of-type(5) .stButton > button {
    background: #2a1a1e !important;
    color: #f48fb1 !important;
    border: 1px solid #f48fb155 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"]:nth-of-type(5) .stButton > button:hover {
    background: #f48fb1 !important; color: #1a000a !important;
    border-color: #f48fb1 !important;
}

/* Clear notebook — muted red */
[data-testid="stSidebar"] .stButton > button {
    background: #2a1515 !important;
    color: #ef9a9a !important;
    border: 1px solid #ef9a9a44 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    padding: 8px 16px !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #ef9a9a !important; color: #1a0000 !important;
}

/* ── Text input ── */
.stTextArea textarea {
    background-color: #212121 !important;
    color: #ececec !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #d4956a !important;
    box-shadow: 0 0 0 2px #d4956a1a !important;
}

/* ── Feedback banners ── */
.feedback-correct {
    background: #152318; border-left: 4px solid #66bb6a; border-radius: 10px;
    padding: 14px 18px; color: #a5d6a7;
    font-family: 'Inter', sans-serif; font-size: 14px; margin: 10px 0;
}
.feedback-wrong {
    background: #231515; border-left: 4px solid #ef5350; border-radius: 10px;
    padding: 14px 18px; color: #ef9a9a;
    font-family: 'Inter', sans-serif; font-size: 14px; margin: 10px 0;
}
.feedback-reveal {
    background: #1e1828; border-left: 4px solid #ab47bc; border-radius: 10px;
    padding: 14px 18px; color: #ce93d8;
    font-family: 'Inter', sans-serif; font-size: 14px; margin: 10px 0;
}

/* ── Notebook entries ── */
.notebook-entry {
    background: #1e1e1e; border: 1px solid #2e2e2e; border-radius: 10px;
    padding: 12px 16px; margin: 6px 0;
}
.notebook-de {
    font-family: 'Inter', sans-serif; font-weight: 600;
    color: #d4956a; font-size: 13px;
}
.notebook-en { color: #888; font-size: 12px; margin-top: 3px; font-family: 'Inter', sans-serif; }
.notebook-note { color: #555; font-size: 11px; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

/* ── Misc ── */
.loading-msg {
    color: #555; font-family: 'JetBrains Mono', monospace;
    font-size: 13px; padding: 30px 0; text-align: center;
}
hr { border-color: #2e2e2e !important; }
label { color: #888 !important; font-size: 13px !important; }
p { color: #ececec !important; }
</style>
""", unsafe_allow_html=True)

# ── Gemini setup ──────────────────────────────────────────────────────────────
TOPICS = [
    "philosophy and ethics", "politics and society", "environmental issues",
    "technology and AI", "culture and identity", "work and economics",
    "relationships and communication", "history and memory",
    "literature and art", "science and research",
    "law and justice", "psychology and behavior",
]

def get_gemini_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.5-flash-lite")
    except Exception:
        return None

def generate_phrase(model, topic: str, mode: str) -> dict | None:
    """Ask Gemini for a single B2-C1 German phrase with translation."""
    prompt = f"""Generate a single authentic German phrase or sentence at CEFR B2-C1 level.
Topic: {topic}

Requirements:
- Natural, idiomatic German that a native speaker would actually say or write
- Complex grammar: subjunctive (Konjunktiv II), passive, relative clauses, or nuanced connectors
- 10-20 words in length
- Include a precise, natural English translation

Respond ONLY with valid JSON in this exact format, no other text:
{{
  "de": "German phrase here",
  "en": "English translation here",
  "topic": "{topic}",
  "grammar_note": "One short grammar tip about a key feature (max 10 words)"
}}"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        # strip markdown code fences if present
        raw = re.sub(r"```json\s*|```", "", raw).strip()
        data = json.loads(raw)
        if "de" in data and "en" in data:
            return data
    except Exception:
        pass
    return None

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "phrase": None,
    "mode": "DE→EN",
    "notebook": [],
    "feedback": None,
    "answer_revealed": False,
    "user_answer": "",
    "loading": False,
    "api_error": False,
    "input_key": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────
def normalize(s: str) -> str:
    return s.lower().strip().rstrip(".!?").replace("  ", " ")

def check_answer(user: str, correct: str) -> bool:
    u, c = normalize(user), normalize(correct)
    return u == c or (len(u) > 8 and (u in c or c in u))

def add_to_notebook(phrase: dict, reason: str = ""):
    if not any(n["de"] == phrase["de"] for n in st.session_state.notebook):
        st.session_state.notebook.append({
            "de": phrase["de"],
            "en": phrase["en"],
            "note": phrase.get("grammar_note", ""),
            "reason": reason,
        })

def reset_answer_state():
    st.session_state.feedback = None
    st.session_state.answer_revealed = False
    st.session_state.user_answer = ""
    st.session_state.input_key += 1

def fetch_new_phrase():
    model = get_gemini_client()
    if model is None:
        st.session_state.api_error = True
        return
    topic = random.choice(TOPICS)
    phrase = generate_phrase(model, topic, st.session_state.mode)
    if phrase:
        st.session_state.phrase = phrase
        st.session_state.api_error = False
        reset_answer_state()
    else:
        st.session_state.api_error = True

# Load first phrase on first run
if st.session_state.phrase is None and not st.session_state.api_error:
    fetch_new_phrase()

# ── Sidebar: Notebook ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📓 Mein Notizbuch")
    st.markdown("<hr>", unsafe_allow_html=True)

    if not st.session_state.notebook:
        st.markdown(
            "<p style='color:#55556a; font-size:13px; font-family:IBM Plex Mono;'>"
            "No entries yet.<br>Wrong answers & revealed phrases appear here.</p>",
            unsafe_allow_html=True
        )
    else:
        count = len(st.session_state.notebook)
        st.markdown(
            f"<p style='color:#c9a84c; font-size:11px; font-family:IBM Plex Mono; letter-spacing:2px;'>"
            f"{count} ENTR{'Y' if count == 1 else 'IES'}</p>",
            unsafe_allow_html=True
        )
        for entry in reversed(st.session_state.notebook):
            note_html = f"<div class='notebook-note'>📌 {entry['note']}</div>" if entry.get("note") else ""
            st.markdown(f"""
            <div class="notebook-entry">
                <div class="notebook-de">{entry['de']}</div>
                <div class="notebook-en">{entry['en']}</div>
                {note_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑  Clear notebook"):
            st.session_state.notebook = []
            st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom:0'>Deutsch Lernen</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#666680; font-family:IBM Plex Mono; font-size:12px; letter-spacing:2px; margin-top:4px;'>"
    "B2–C1 PHRASE TRAINER · POWERED BY GEMINI</p>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# Controls
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("🔄  New Phrase"):
        fetch_new_phrase()
        st.rerun()
with col2:
    flip_label = "🔀  Flip → EN→DE" if st.session_state.mode == "DE→EN" else "🔀  Flip → DE→EN"
    if st.button(flip_label):
        st.session_state.mode = "EN→DE" if st.session_state.mode == "DE→EN" else "DE→EN"
        reset_answer_state()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# API error state
if st.session_state.api_error:
    st.markdown("""
    <div style='background:#2b1500; border-left:4px solid #e67e22; border-radius:8px; 
    padding:16px 20px; color:#ffb347; font-family:IBM Plex Mono; font-size:13px;'>
    ⚠️ Could not reach Gemini API.<br><br>
    Make sure your <strong>GEMINI_API_KEY</strong> is set in Streamlit Secrets.<br>
    Get a free key at: <a href="https://aistudio.google.com/apikey" target="_blank" 
    style="color:#c9a84c;">aistudio.google.com/apikey</a>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Phrase display
phrase = st.session_state.phrase
if phrase is None:
    st.markdown('<div class="loading-msg">⏳ Generating your first phrase…</div>', unsafe_allow_html=True)
    st.stop()

mode = st.session_state.mode
if mode == "DE→EN":
    display_text = phrase["de"]
    display_label = "GERMAN — translate to English"
    correct_answer = phrase["en"]
    placeholder = "Type your English translation…"
else:
    display_text = phrase["en"]
    display_label = "ENGLISH — translate to German"
    correct_answer = phrase["de"]
    placeholder = "Ihre deutsche Übersetzung…"

topic_str = phrase.get("topic", "").title()
grammar_note = phrase.get("grammar_note", "")

grammar_html = f'<span class="grammar-tag">📌 {grammar_note}</span>' if grammar_note else ""
topic_html = f'<span class="topic-tag">🏷 {topic_str}</span>'

st.markdown(f'<div class="mode-badge">{mode}</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="phrase-card">
    <div class="phrase-label">{display_label}</div>
    <p class="phrase-text">{display_text}</p>
    <div class="phrase-meta" style="margin-top:14px;">
        {grammar_html}{topic_html}
    </div>
</div>
""", unsafe_allow_html=True)

# Answer area
user_answer = st.text_area(
    "Your translation",
    value=st.session_state.user_answer,
    placeholder=placeholder,
    height=80,
    label_visibility="collapsed",
    key=f"answer_box_{st.session_state.input_key}"
)
st.session_state.user_answer = user_answer

# Action buttons — 5 columns so CSS nth-of-type targets work correctly
# cols 1+2 = New Phrase & Flip (top row already rendered above)
# cols 3+4+5 = Check, Reveal, Save
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 3])
with c1:
    check_clicked = st.button("✓  Check")
with c2:
    reveal_clicked = st.button("👁  Reveal")
with c3:
    save_clicked = st.button("💾  Save")

if check_clicked and user_answer.strip():
    correct = check_answer(user_answer, correct_answer)
    st.session_state.feedback = "correct" if correct else "wrong"
    if not correct:
        add_to_notebook(phrase, reason="wrong answer")
    st.rerun()

if reveal_clicked:
    st.session_state.answer_revealed = True
    add_to_notebook(phrase, reason="revealed")
    st.rerun()

if save_clicked:
    add_to_notebook(phrase, reason="manually saved")
    st.rerun()

# Feedback
if st.session_state.feedback == "correct":
    st.markdown('<div class="feedback-correct">✓ Richtig! Well done.</div>', unsafe_allow_html=True)
elif st.session_state.feedback == "wrong":
    st.markdown(
        f'<div class="feedback-wrong">✗ Not quite. &nbsp;<strong>Answer:</strong> {correct_answer}</div>',
        unsafe_allow_html=True
    )

if st.session_state.answer_revealed:
    st.markdown(
        f'<div class="feedback-reveal">👁 Answer: {correct_answer}</div>',
        unsafe_allow_html=True
    )
