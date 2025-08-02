# agent/tools/gmail_fetcher.py

import base64
from typing import Dict, Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_gmail_service():
    """Initialize Gmail API service using token.json credentials."""
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.modify"])
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_emails(state: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch unread emails from the Gmail inbox."""
    service = get_gmail_service()

    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No unread emails found.")
        return {**state, "label": "none"}

    # Fetch the first email's details
    message_id = messages[0]["id"]
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()

    headers = msg["payload"].get("headers", [])
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    snippet = msg.get("snippet", "")

    # Decode body content (if available)
    body_data = ""
    try:
        parts = msg["payload"].get("parts", [])
        if parts:
            part = parts[0]
            data = part["body"]["data"]
            body_data = base64.urlsafe_b64decode(data).decode("utf-8")
    except Exception as e:
        print(f"Warning: Could not decode email body. {e}")

    # Mark as read (optional)
    service.users().messages().modify(
        userId="me", id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()

    return {
        **state,
        "email_id": message_id,
        "subject": subject,
        "sender": sender,
        "body": body_data or snippet,
    }
