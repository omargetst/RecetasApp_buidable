import streamlit as st
import markdown
from chat.ollama_api import chat_with_ollama
from chat.extractors import extract_text_from_images, extract_text_from_pdfs
from chat.utils import render_copy_button, apply_view_mode_styles
from chat.state import init_session_state

st.set_page_config(page_title="Asistente con Ollama", page_icon="🧠")
init_session_state()
apply_view_mode_styles(st.session_state.view_mode)

st.title("🧠 Asistente con Ollama")

with st.container():
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("🔁 Vista", help="Cambiar entre vista centrada y amplia"):
            st.session_state.view_mode = (
                "wide" if st.session_state.view_mode == "centered" else "centered"
            )
    with col2:
        st.caption(f"🔍 Modo actual: **{st.session_state.view_mode}**")

with st.sidebar:
    if st.button("🧹 Limpiar conversación"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    if st.session_state.get("history"):
        st.markdown("## 🕓 Historial")
        for i, pair in enumerate(reversed(st.session_state.history)):
            index = len(st.session_state.history) - i
            st.markdown(f"**Mensaje #{index}**")
            st.markdown(f"**🗨️ Pregunta:** {pair['user']}")
            resumen = pair['assistant'][:120] + ("..." if len(pair['assistant']) > 120 else "")
            st.caption(f"🧠 {resumen}")
            render_copy_button(pair["assistant"])

st.markdown("<div class='chat-bar'>", unsafe_allow_html=True)
with st.form("message_form", clear_on_submit=True):
    user_input = st.text_input("✍️ Escribe tu mensaje")
    uploaded_files = st.file_uploader(
        "📎 Adjunta imágenes o PDFs (opcional)",
        type=["pdf", "jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    submitted = st.form_submit_button("Enviar")
st.markdown("</div>", unsafe_allow_html=True)

if submitted and user_input:
    st.session_state.messages = []

    files_info = []
    context = ""

    if uploaded_files:
        context += extract_text_from_pdfs([f for f in uploaded_files if f.name.endswith(".pdf")])
        context += extract_text_from_images([f for f in uploaded_files if f.name.lower().endswith((".jpg", ".jpeg", ".png"))])
        for file in uploaded_files:
            files_info.append({
                "type": "image" if file.name.lower().endswith((".jpg", ".jpeg", ".png")) else "pdf",
                "name": file.name,
                "data": file.read() if file.name.lower().endswith((".jpg", ".jpeg", ".png")) else None
            })

    full_prompt = f"{user_input}\n\n[Contexto extraído de archivos]:\n{context.strip()}" if context else user_input
    user_msg = {"role": "user", "content": full_prompt, "files": files_info}
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.markdown(f"<div class='chat-message user'>{user_input}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Pensando..."):
            result = chat_with_ollama(
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            html_result = markdown.markdown(result)
            st.markdown(f"""
            <div class='chat-message assistant'>
                {html_result}
            </div>
            """, unsafe_allow_html=True)
            render_copy_button(result)

    st.session_state.messages.append({"role": "assistant", "content": result})
    st.session_state.history = st.session_state.get("history", []) + [{
        "user": user_input,
        "assistant": result
    }]

st.markdown("<div id='bottom-scroll'></div>", unsafe_allow_html=True)
st.components.v1.html("""
<script>
  var scroll = document.getElementById('bottom-scroll');
  scroll.scrollIntoView({ behavior: 'smooth' });
</script>
""", height=0)

st.markdown("""
<style>
.chat-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem 2rem;
    background-color: #0e1117;
    border-top: 1px solid #333;
    z-index: 999;
}
.chat-bar .stForm {
    background: none;
}
.block-container {
    padding-bottom: 180px;
}
.chat-message {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 10px;
    line-height: 1.5;
    font-size: 1rem;
}
.chat-message.user {
    background-color: #1c202b;
    color: #fff;
    border-left: 4px solid #6c63ff;
}
.chat-message.assistant {
    background-color: #1a1d26;
    color: #e6e6e6;
    border-left: 4px solid #00bfa6;
}

/* NUEVO: Mejoras de formato */
.chat-message.assistant h1,
.chat-message.assistant h2,
.chat-message.assistant h3 {
    font-size: 1.1rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.chat-message.assistant p,
.chat-message.assistant li {
    font-size: 0.95rem;
    line-height: 1.6;
}

.chat-message.assistant code {
    background-color: #2b2b2b;
    padding: 2px 5px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
}

.chat-message.assistant pre {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.9rem;
}

.copy-button {
    background-color: #262730;
    color: #ffffff;
    border: 1px solid #444;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}
.copy-button:hover {
    background-color: #444c66;
}
button[kind="primary"] {
    background-color: #6c63ff;
    border: none;
}
button[kind="primary"]:hover {
    background-color: #5a52e0;
}
</style>
""", unsafe_allow_html=True)
