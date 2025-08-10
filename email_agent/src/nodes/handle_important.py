from services.gmail_client import GmailClient
from state import AppState

def handle_important_node(state: AppState) -> AppState:
    gmail = GmailClient()

    for email in state.get("emails", []):
        if email.get("is_important"):
            gmail.mark_as_important(email["id"])
            # Example: auto-reply
            gmail.send_message(
                to=email["sender"],
                subject="Re: " + email["subject"],
                body="Thank you for your email. I will get back to you shortly."
            )

    return state
