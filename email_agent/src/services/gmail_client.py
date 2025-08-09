import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class GmailClient:
    def __init__(self):
        """
        Initializes Gmail client using credentials stored in Lambda environment variable.
        Environment variable:
            GMAIL_TOKEN_JSON -> A single-line JSON string containing:
                token, refresh_token, token_uri, client_id, client_secret, scopes, expiry
        """
        token_json = os.environ.get("GMAIL_TOKEN_JSON")
        if not token_json:
            raise ValueError("GMAIL_TOKEN_JSON environment variable is not set")

        try:
            token_info = json.loads(token_json)
        except json.JSONDecodeError:
            raise ValueError("GMAIL_TOKEN_JSON is not valid JSON")

        # Build credentials from token info
        creds = Credentials.from_authorized_user_info(token_info)

        # Refresh the token if it’s expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

            # Save refreshed token back to env var (optional — for next invocation)
            os.environ["GMAIL_TOKEN_JSON"] = json.dumps(json.loads(creds.to_json()))

        # Create Gmail service
        self.service = build("gmail", "v1", credentials=creds)

    def list_messages(self, query="", max_results=10, user_id="me"):
        """List Gmail messages with optional search query."""
        results = (
            self.service.users()
            .messages()
            .list(userId=user_id, q=query, maxResults=max_results)
            .execute()
        )
        return results.get("messages", [])

    def get_message(self, message_id, user_id="me"):
        """Get a specific Gmail message by ID."""
        return self.service.users().messages().get(userId=user_id, id=message_id).execute()

    def send_message(self, raw_message, user_id="me"):
        """Send an email (raw base64 encoded MIME)."""
        return self.service.users().messages().send(userId=user_id, body={"raw": raw_message}).execute()

    def delete_message(self, message_id, user_id="me"):
        """Delete a specific Gmail message."""
        self.service.users().messages().delete(userId=user_id, id=message_id).execute()
        return True
