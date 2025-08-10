from services.gmail_client import GmailClient
from state import AppState

def handle_other_node(state: AppState) -> AppState:
    gmail = GmailClient()

    for email in state.get("emails", []):
        if not email.get("is_important"):
            gmail.archive_email(email["id"])

    return state
