import openai
from pathlib import Path
import os

# Obtener la API key de variable de entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("❌ No se encontró la variable de entorno OPENAI_API_KEY")

openai.api_key = api_key

# Ruta al Swagger
swagger_path = "../openapi/swaggeradvanta.json"
output_path = "../ApiTests/Tests/GeneratedTests.cs"

# Leer archivo Swagger
try:
    swagger_content = Path(swagger_path).read_text()
except FileNotFoundError:
    print(f"❌ Archivo Swagger no encontrado: {swagger_path}")
    exit(1)

# Construir prompt
prompt = f"""
Quiero que generes pruebas automatizadas en C# usando RestSharp, NUnit y FluentAssertions.

📌 A partir del siguiente archivo Swagger, crea una clase llamada `GeneratedTests` que:
- Use RestSharp para hacer peticiones HTTP
- Use NUnit como framework de pruebas
- Valide respuestas HTTP 200
- Cree al menos una prueba por endpoint

✅ Solo quiero el código fuente. No escribas explicaciones ni comentarios.

Aquí está el Swagger:

{swagger_content}
"""

# Llamar a GPT-4
print("🚀 Llamando a GPT-4...")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

# Obtener y guardar el resultado
output = response["choices"][0]["message"]["content"]
Path(output_path).write_text(output)

print(f"✅ Pruebas generadas en: {output_path}")
