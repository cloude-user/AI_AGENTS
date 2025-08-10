import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def classify_email(self, subject: str, body: str) -> dict:
        """
        Classify email as 'important', 'promotion', 'spam', etc.
        """
        prompt = (
            "Classify the following email into categories:\n"
            "1. important (job-related, personal)\n"
            "2. promotion (ads, offers)\n"
            "3. spam (irrelevant, phishing)\n\n"
            f"Subject: {subject}\nBody: {body}\n"
            "Respond in JSON format: {\"label\": \"<category>\", \"reason\": \"<short reason>\"}"
        )

        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = resp.choices[0].message.content.strip()
        try:
            import json
            return json.loads(content)
        except Exception:
            return {"label": "unknown", "reason": "Could not parse LLM response"}

    def generate_reply(self, subject: str, body: str, tone="professional") -> str:
        """
        Generate a draft reply to an important email.
        """
        prompt = (
            f"You are an assistant drafting a {tone} reply to the following email.\n"
            f"Subject: {subject}\nBody: {body}\n"
            "Draft a short and clear reply."
        )

        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return resp.choices[0].message.content.strip()
