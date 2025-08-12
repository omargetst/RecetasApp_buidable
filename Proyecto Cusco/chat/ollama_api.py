import requests
import json
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"

def chat_with_ollama(messages):
    """
    Envía una conversación a Ollama y devuelve la respuesta generada por el modelo.
    Usa streaming para mostrar la respuesta progresivamente.
    """
    payload = {
        "model": "llama3",
        "stream": True,
        "messages": messages
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con Ollama: {e}")
        return "⚠️ Error al conectar con Ollama. Asegúrate de que el servidor esté activo."

    result = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    result += data["message"]["content"]
            except json.JSONDecodeError as e:
                logger.warning(f"Error al decodificar JSON: {e}")
                continue
            except Exception as e:
                logger.exception(f"Error inesperado procesando la respuesta: {e}")
                continue

    return result or "⚠️ No se recibió respuesta del modelo."
