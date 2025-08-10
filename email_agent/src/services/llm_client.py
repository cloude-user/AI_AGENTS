import os, logging
import openai
logger=logging.getLogger("llm_client")
logger.setLevel(logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL","gpt-4o-mini")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY env var required")
openai.api_key = OPENAI_API_KEY

class LLMClient:
    def __init__(self, model: str = MODEL):
        self.model = model

    def classify_email(self, subject: str, body: str) -> dict:
        """
        Returns: { label: 'promotional'|'important'|'personal', confidence:float }
        """
        prompt = f"""
You are an email triage assistant. Classify this email into one of:
- promotional (ads, offers, newsletters, unsubscribe)
- important (job, interview, urgent request)
- personal (friend, social)
Return JSON only like: {{ "label": "important", "confidence": 0.93 }}
Subject: {subject}
Body: {body[:3000]}
"""
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}],
            temperature=0.0,
            max_tokens=80
        )
        text = resp["choices"][0]["message"]["content"].strip()
        try:
            import json
            j=json.loads(text)
            return {"label": j.get("label","other"), "confidence": float(j.get("confidence",0.5))}
        except Exception:
            # fallback heuristics
            txt=(subject+" "+body).lower()
            if any(k in txt for k in ["unsubscribe","sale","offer","discount","promo"]):
                return {"label":"promotional","confidence":0.9}
            if any(k in txt for k in ["job","interview","position","opportunity","hiring"]):
                return {"label":"important","confidence":0.9}
            return {"label":"promotional","confidence":0.5}

    def generate_reply(self, subject: str, body: str, tone: str="professional") -> str:
        prompt = f"""
You are an assistant that writes an email reply. Tone: {tone}.
Subject: {subject}
Message: {body[:4000]}
Write a clear, concise reply. If the message is a job opportunity ask for role/location if missing.
Return only the reply text.
"""
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=600
        )
        return resp["choices"][0]["message"]["content"].strip()
