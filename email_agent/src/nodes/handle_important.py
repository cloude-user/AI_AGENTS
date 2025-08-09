from services.gmail_client import GmailClient
from state import AppState

def handle_important_node(state: AppState) -> AppState:
    gmail = GmailClient()
    for email in state.get("emails", []):
        if email.get("is_important"):
            gmail.mark_as_important(email["id"])
            state["processed_count"] = state.get("processed_count", 0) + 1
    return state
