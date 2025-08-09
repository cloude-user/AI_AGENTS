import os
import openai

class LLMClient:
    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def classify(self, text: str) -> str:
        prompt = f"Classify this email as Important or Other:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        return response["choices"][0]["message"]["content"].strip()
