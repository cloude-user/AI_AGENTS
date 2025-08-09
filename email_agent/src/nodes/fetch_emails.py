from services.gmail_client import GmailClient
from state import AppState

def fetch_emails_node(state: AppState) -> AppState:
    gmail = GmailClient()
    emails = gmail.fetch_unread_emails()
    state["emails"] = emails
    return state
