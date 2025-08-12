import streamlit as st
import requests
import pdfplumber
from PIL import Image
import pytesseract
import json
import io

OLLAMA_URL = "http://localhost:11434/api/chat"

# Configuración inicial
st.set_page_config(page_title="Asistente con Ollama", page_icon="🧠")

# Inicializa modo de vista si no existe
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "centered"

# Configura el modo de vista boton
col1, col2 = st.columns([1, 8])
with col1:
    if st.button("🔁"):
        st.session_state.view_mode = "wide" if st.session_state.view_mode == "centered" else "centered"

# Muestra el modo actual
st.caption(f"🔍 Modo actual: **{st.session_state.view_mode}**")

# CSS dinámico según modo
if st.session_state.view_mode == "centered":
    st.markdown("""
        <style>
        .block-container {
            max-width: 750px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .block-container {
            max-width: 95%;
        }
        </style>
    """, unsafe_allow_html=True)

# Inicializa historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_text_from_pdfs(files):
    text = ""
    for f in files:
        with pdfplumber.open(f) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    return text

def extract_text_from_images(files):
    text = ""
    for f in files:
        image = Image.open(f)
        text += pytesseract.image_to_string(image) + "\n"
    return text

def chat_with_ollama(messages):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "stream": True,
        "messages": messages
    }, stream=True)

    result = ""
    placeholder = st.empty()
    with st.spinner("Pensando..."):
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data and "content" in data["message"]:
                        result += data["message"]["content"]
                        placeholder.markdown(result + "▌")
                except:
                    pass
        placeholder.markdown(result)
    return result

# Título de la app
st.markdown("## 🧠 Asistente con Ollama")

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "files" in msg:
            for file in msg["files"]:
                if file["type"] == "image":
                    st.image(file["data"], caption=file.get("name", ""), width=300)
                elif file["type"] == "pdf":
                    st.markdown(f"📎 Documento PDF: `{file['name']}`")

# Entrada de usuario (mensaje)
user_input = st.chat_input("Escribe tu mensaje aquí...")

# Subida de archivos adjuntos
uploaded_files = st.file_uploader("Adjunta imágenes o PDFs (opcional)", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

if user_input:
    # Inicializa entrada de usuario
    user_msg = {
        "role": "user",
        "content": user_input,
        "files": []
    }

    # Procesa archivos adjuntos
    extracted_context = ""
    for file in uploaded_files or []:
        file_bytes = file.read()
        file.seek(0)
        ext = file.name.lower()
        if ext.endswith(".pdf"):
            extracted_context += extract_text_from_pdfs([file])
            user_msg["files"].append({
                "type": "pdf",
                "name": file.name
            })
        elif ext.endswith((".jpg", ".jpeg", ".png")):
            extracted_context += extract_text_from_images([file])
            user_msg["files"].append({
                "type": "image",
                "name": file.name,
                "data": file_bytes
            })

    # Agrega contexto extraído (si lo hay)
    if extracted_context:
        user_msg["content"] += f"\n\n[Contexto extraído de archivos]:\n{extracted_context.strip()}"

    # Agrega mensaje al historial
    st.session_state.messages.append(user_msg)

    # Construye historial para enviar a Ollama
    ollama_input = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    # Muestra el mensaje del usuario y procesa la respuesta
    with st.chat_message("user"):
        st.markdown(user_msg["content"])
        for f in user_msg["files"]:
            if f["type"] == "image":
                st.image(f["data"], caption=f.get("name", ""), width=300)
            elif f["type"] == "pdf":
                st.markdown(f"📎 Documento PDF: `{f['name']}`")

    # Muestra la respuesta del asistente
    with st.chat_message("assistant"):
        result = chat_with_ollama(ollama_input)
        
        # Mostrar respuesta
        st.markdown(result)
        
        # Botón para copiar
        button_id = f"copy-button-{len(st.session_state.messages)}"
        copy_code = f"""
            <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(() => {{
                    alert('✅ Respuesta copiada al portapapeles');
                }});
            }}
            </script>
            <button onclick="copyToClipboard(`{result.replace("`", "\\`").replace("\\", "\\\\")}`)">📋 Copiar respuesta</button>
        """
        st.components.v1.html(copy_code, height=35)

    # Guarda la respuesta en historial
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })
