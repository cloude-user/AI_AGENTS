import base64
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_gmail_service():
    creds = Credentials(
        token=os.environ["GMAIL_TOKEN"],
        refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GMAIL_CLIENT_ID"],
        client_secret=os.environ["GMAIL_CLIENT_SECRET"]
    )
    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(max_results=15):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results).execute()
    messages = results.get("messages", [])
    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        subject = next(h["value"] for h in msg_data["payload"]["headers"] if h["name"] == "Subject")
        sender = next(h["value"] for h in msg_data["payload"]["headers"] if h["name"] == "From")
        body = get_email_body(msg_data)
        email_data.append({"id": msg["id"], "subject": subject, "sender": sender, "body": body})
    return email_data

def get_email_body(msg_data):
    parts = msg_data["payload"].get("parts", [])
    if parts:
        data = parts[0]["body"].get("data")
    else:
        data = msg_data["payload"]["body"].get("data")
    return base64.urlsafe_b64decode(data).decode("utf-8")

def draft_reply(original_email, reply_body):
    service = get_gmail_service()
    message = f"Subject: Re: {original_email['subject']}\n\n{reply_body}"
    raw_message = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")
    service.users().drafts().create(userId="me", body={"message": {"raw": raw_message}}).execute()
