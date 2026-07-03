import requests


class LLMService:

    def __init__(self):
        self.url = "http://57.159.31.11/v1/chat/completions"
        self.model = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"

    def generate(self, context, question):

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not present in the context, reply:
"I couldn't find the answer in the provided documents."

Context:
----------------------
{context}
----------------------

Question:
{question}
"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(self.url, json=payload)

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]