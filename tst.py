import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyD2Ha-DCccWwu1BHyRfvNfwYTmXO1NKW3c")

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = """
Responda APENAS em JSON no formato:
{
  "acao": "...",
  "parametros": {}
}

Texto: "toca música do Eminem"
"""

response = model.generate_content(prompt)

texto = response.text

print(texto)

# tentar converter pra JSON
data = json.loads(texto)

print(data["acao"])