from services.gmail_client import GmailClient
from typing import Dict, Any

def fetch_emails_node(state: Dict[str,Any]) -> Dict[str,Any]:
    max_fetch = int(state.get("MAX_FETCH", 10))
    gmail = GmailClient()
    emails = gmail.fetch_unread_emails(max_results=max_fetch)
    state["emails"]=emails
    return state
