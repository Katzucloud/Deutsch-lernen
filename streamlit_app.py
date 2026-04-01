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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0e0e12 !important;
    color: #e8e6e0 !important;
    font-family: 'IBM Plex Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #13131a !important;
    border-right: 1px solid #2a2a3a;
}
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #f0ede6 !important; }

.phrase-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #c9a84c44;
    border-left: 4px solid #c9a84c;
    border-radius: 12px;
    padding: 32px 36px;
    margin: 16px 0 24px 0;
}
.phrase-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: #c9a84c; margin-bottom: 12px;
}
.phrase-text {
    font-family: 'Playfair Display', serif;
    font-size: 26px; color: #f5f0e8; line-height: 1.4; margin: 0;
}
.phrase-meta {
    font-size: 11px; color: #55556a; margin-top: 10px;
    font-family: 'IBM Plex Mono', monospace;
}
.stButton > button {
    background: #1e1e2e !important; color: #c9a84c !important;
    border: 1px solid #c9a84c55 !important; border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important; letter-spacing: 1.5px !important;
    padding: 10px 22px !important; transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #c9a84c !important; color: #0e0e12 !important;
    border-color: #c9a84c !important;
}
.stTextArea textarea, .stTextInput input {
    background-color: #1a1a2e !important; color: #e8e6e0 !important;
    border: 1px solid #2a2a4a !important; border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important; font-size: 15px !important;
}
.stTextArea textarea:focus { border-color: #c9a84c !important; box-shadow: 0 0 0 2px #c9a84c22 !important; }

.feedback-correct {
    background: #0d2b1d; border-left: 4px solid #2ecc71; border-radius: 8px;
    padding: 14px 18px; color: #7dffb3;
    font-family: 'IBM Plex Mono', monospace; font-size: 13px; margin: 8px 0;
}
.feedback-wrong {
    background: #2b0d0d; border-left: 4px solid #e74c3c; border-radius: 8px;
    padding: 14px 18px; color: #ff9999;
    font-family: 'IBM Plex Mono', monospace; font-size: 13px; margin: 8px 0;
}
.feedback-reveal {
    background: #1a1428; border-left: 4px solid #8855cc; border-radius: 8px;
    padding: 14px 18px; color: #cc99ff;
    font-family: 'IBM Plex Mono', monospace; font-size: 13px; margin: 8px 0;
}
.notebook-entry {
    background: #1a1a2e; border: 1px solid #2a2a4a; border-radius: 8px;
    padding: 12px 16px; margin: 6px 0; font-size: 13px;
}
.notebook-de { font-family: 'IBM Plex Mono', monospace; color: #c9a84c; font-weight: 500; }
.notebook-en { color: #aaa8c0; font-size: 12px; margin-top: 2px; }
.mode-badge {
    display: inline-block; background: #c9a84c22; color: #c9a84c;
    border: 1px solid #c9a84c55; border-radius: 20px;
    padding: 3px 14px; font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; letter-spacing: 1px; margin-bottom: 6px;
}
.loading-msg {
    color: #666680; font-family: 'IBM Plex Mono', monospace;
    font-size: 13px; padding: 20px 0; text-align: center;
}
hr { border-color: #2a2a3a !important; }
label { color: #aaa8c0 !important; font-size: 13px !important; }
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
        return genai.GenerativeModel("gemini-2.0-flash-lite")
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
            note_html = f"<div style='color:#55556a; font-size:11px; margin-top:4px;'>📌 {entry['note']}</div>" if entry.get("note") else ""
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

st.markdown(f'<div class="mode-badge">{mode}</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="phrase-card">
    <div class="phrase-label">{display_label}</div>
    <p class="phrase-text">{display_text}</p>
    <div class="phrase-meta">
        {'📌 ' + grammar_note + ' &nbsp;·&nbsp; ' if grammar_note else ''}🏷 {topic_str}
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
    key="answer_box"
)
st.session_state.user_answer = user_answer

# Action buttons
c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
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
