import streamlit as st
import streamlit.components.v1 as components
import uuid

def render_copy_button(text):
    button_id = str(uuid.uuid4()).replace("-", "")
    html_code = f"""
    <textarea id="copy-target-{button_id}" style="position:absolute; left:-9999px;">{text}</textarea>
    <button id="copy-btn-{button_id}" class="copy-button">📋 Copiar respuesta</button>
    <script>
    const btn = document.getElementById("copy-btn-{button_id}");
    btn.addEventListener("click", () => {{
        const textarea = document.getElementById("copy-target-{button_id}");
        textarea.select();
        document.execCommand('copy');
        btn.innerText = "✅ Copiado";
        setTimeout(() => {{
            btn.innerText = "📋 Copiar respuesta";
        }}, 2000);
    }});
    </script>
    """
    components.html(html_code, height=40)

def apply_view_mode_styles(view_mode):
    if view_mode == "centered":
        st.markdown("""
            <style>
                .block-container {
                    max-width: 800px;
                    margin: auto;
                }
            </style>
        """, unsafe_allow_html=True)