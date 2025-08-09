import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GmailClient:
    def __init__(self):
        creds = Credentials(
            token=os.environ["GMAIL_ACCESS_TOKEN"],
            refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ["GMAIL_CLIENT_ID"],
            client_secret=os.environ["GMAIL_CLIENT_SECRET"],
            scopes=["https://www.googleapis.com/auth/gmail.modify"]
        )
        self.service = build("gmail", "v1", credentials=creds)

    def fetch_unread_emails(self):
        results = self.service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=10).execute()
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
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
