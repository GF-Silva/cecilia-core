from google import genai

class GenEngine:
    def __init__(self, client_config):
        self.client = genai.Client(**client_config)
        self.model = "gemini-2.5-flash"
    
    async def process_prompt(self, contents):
        response = await self.client.aio.models.generate_content(
            model = self.model,
            contents = contents,
            config = {
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "acao": {"type": "string"},
                        "parametros": {
                            "type": "object",
                            "properties": {
                                "artista": {"type": "string"}
                            }
                        }
                    },
                "required": ["acao", "parametros"]
                }
            }
        )

        return response.text