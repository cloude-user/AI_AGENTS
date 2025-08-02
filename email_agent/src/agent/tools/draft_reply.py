# agent/tools/draft_reply.py

from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from agent.tools.gmail_fetcher import get_gmail_service
import base64
import email.utils


def generate_reply(subject: str, body: str) -> str:
    """Generate a reply using the LLM."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that writes professional email replies."),
        ("user", "Write a reply to the following job email:\nSubject: {subject}\nBody: {body}")
    ])
    chain = prompt | ChatOpenAI(model="gpt-4o", temperature=0.3)
    return chain.invoke({"subject": subject, "body": body}).content


def create_draft(service, to_email, reply_body, original_subject) -> None:
    """Create a draft reply in Gmail."""
    message_text = f"To: {to_email}\r\n" \
                   f"Subject: Re: {original_subject}\r\n" \
                   f"\r\n{reply_body}"

    raw = base64.urlsafe_b64encode(message_text.encode("utf-8")).decode("utf-8")

    draft = {
        'message': {
            'raw': raw
        }
    }

    service.users().drafts().create(userId='me', body=draft).execute()


def draft_reply(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate and draft a reply for job emails."""
    subject = state.get("subject", "")
    body = state.get("body", "")
    sender = state.get("sender", "")

    if not sender:
        raise ValueError("Missing sender in email state.")

    service = get_gmail_service()

    reply_body = generate_reply(subject, body)
    create_draft(service, to_email=sender, reply_body=reply_body, original_subject=subject)

    state["drafted"] = True
    return state
