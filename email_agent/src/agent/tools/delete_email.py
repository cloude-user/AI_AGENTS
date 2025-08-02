# agent/tools/delete_email.py

from typing import Dict, Any
from agent.tools.gmail_fetcher import get_gmail_service


def delete_email(state: Dict[str, Any]) -> Dict[str, Any]:
    """Delete the email from Gmail using its ID."""
    service = get_gmail_service()
    email_id = state.get("email_id")

    if not email_id:
        raise ValueError("Missing email_id in state.")

    try:
        service.users().messages().delete(userId='me', id=email_id).execute()
        print(f"Deleted email: {email_id}")
        state["deleted"] = True
    except Exception as e:
        print(f"Error deleting email: {e}")
        state["deleted"] = False
        state["error"] = str(e)

    return state
