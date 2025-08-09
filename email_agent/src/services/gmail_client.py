import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class GmailClient:
    def __init__(self):
        creds = None

        if os.environ.get("GMAIL_TOKEN_JSON"):
            creds_data = json.loads(os.environ["GMAIL_TOKEN_JSON"])
            creds = Credentials.from_authorized_user_info(creds_data)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        self.service = build("gmail", "v1", credentials=creds)

    def fetch_unread_emails(self):
        results = self.service.users().messages().list(
            userId="me",
            labelIds=["UNREAD"],
            maxResults=10
        ).execute()
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()
            emails.append(msg_data)
        return emails

    def mark_as_important(self, email_id):
        self.service.users().messages().modify(
            userId="me",
            id=email_id,
            body={"addLabelIds": ["IMPORTANT"]}
        ).execute()

    def archive_email(self, email_id):
        self.service.users().messages().modify(
            userId="me",
            id=email_id,
            body={"removeLabelIds": ["INBOX"]}
        ).execute()
