import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY"))

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Create by Ashish Coder",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Hide default Streamlit header/footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* Title card */
    .title-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 18px;
        padding: 20px 30px;
        text-align: center;
        margin-bottom: 24px;
    }
    .title-card h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
    }
    .title-card p {
        color: rgba(255,255,255,0.55);
        font-size: 0.85rem;
        margin: 6px 0 0;
    }
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0%,100% { opacity: 1; }
        50%      { opacity: 0.3; }
    }

    /* Chat container */
    .chat-area {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        max-height: 58vh;
        overflow-y: auto;
    }

    /* Message bubbles */
    .msg-row { display: flex; margin-bottom: 14px; align-items: flex-end; gap: 10px; }
    .msg-row.user  { flex-direction: row-reverse; }

    .avatar {
        width: 34px; height: 34px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; flex-shrink: 0;
    }
    .avatar.bot  { background: linear-gradient(135deg,#6366f1,#8b5cf6); }
    .avatar.user { background: linear-gradient(135deg,#0ea5e9,#38bdf8); }

    .bubble {
        max-width: 72%;
        padding: 11px 16px;
        border-radius: 18px;
        font-size: 0.92rem;
        line-height: 1.55;
        word-break: break-word;
    }
    .bubble.bot {
        background: rgba(99,102,241,0.18);
        border: 1px solid rgba(99,102,241,0.3);
        color: #e2e8f0;
        border-bottom-left-radius: 4px;
    }
    .bubble.user {
        background: linear-gradient(135deg,#0ea5e9,#6366f1);
        color: #ffffff;
        border-bottom-right-radius: 4px;
    }

    /* Input box */
    .stChatInput > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 14px !important;
    }
    .stChatInput textarea {
        color: #ffffff !important;
        font-size: 0.93rem !important;
    }
    .stChatInput textarea::placeholder { color: rgba(255,255,255,0.4) !important; }

    /* Scrollbar */
    .chat-area::-webkit-scrollbar { width: 5px; }
    .chat-area::-webkit-scrollbar-track { background: transparent; }
    .chat-area::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; }

    /* Sidebar */
    .stSidebar { background: rgba(15,12,41,0.95) !important; }
    .stSidebar * { color: #e2e8f0 !important; }

    /* Clear button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg,#ef4444,#dc2626);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px;
        font-weight: 500;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    model_choice = st.selectbox(
        "🧠 Model",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"],
        index=0
    )

    temperature = st.slider("🌡️ Creativity", 0.0, 1.0, 0.7, 0.05)

    st.markdown("---")
    st.markdown("**💬 Chat Stats**")
    msg_count = len(st.session_state.get("messages", []))
    st.markdown(f"Messages: `{msg_count}`")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.3)'>Made by Ashish Coder 🚀</small>", unsafe_allow_html=True)

# ── Header card ──────────────────────────────────────────────
st.markdown("""
<div class="title-card">
    <h1>🤖 Ai Chatbot create by Ashish Coder</h1>
    <p><span class="status-dot"></span>Powered by Groq · Lightning fast responses</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Chat display ─────────────────────────────────────────────
chat_html = '<div class="chat-area">'

if not st.session_state.messages:
    chat_html += """
    <div style="text-align:center;padding:40px 0;color:rgba(255,255,255,0.3);">
        <div style="font-size:2.5rem">💬</div>
        <div style="margin-top:10px;font-size:0.9rem">Start a conversation below!</div>
    </div>"""
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="msg-row user">
                <div class="avatar user">🧑</div>
                <div class="bubble user">{msg["content"]}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-row">
                <div class="avatar bot">🤖</div>
                <div class="bubble bot">{msg["content"]}</div>
            </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Input & response ─────────────────────────────────────────
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=model_choice,
            messages=st.session_state.messages,
            temperature=temperature
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()