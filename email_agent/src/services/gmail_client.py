import os
import json
import base64
import logging
import re
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from email.mime.text import MIMEText

logger = logging.getLogger("gmail_client")

class GmailClient:
    def __init__(self):
        token_str = os.getenv("GMAIL_JSON_TOKEN")
        if not token_str:
            raise ValueError("GMAIL_JSON_TOKEN env var not set")
        try:
            token_info = json.loads(token_str)
        except Exception as e:
            raise ValueError("GMAIL_JSON_TOKEN must be valid JSON") from e

        self.creds = Credentials.from_authorized_user_info(token_info, token_info.get("scopes"))

        try:
            if not self.creds.valid or self.creds.expired:
                if self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    raise RefreshError("No refresh token")
        except RefreshError:
            logger.exception("RefreshError")
            raise
        except Exception:
            logger.exception("Unexpected error")
            raise

        self.service = build("gmail", "v1", credentials=self.creds)

    # ------------- public methods -------------
    def fetch_unread_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        try:
            resp = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["UNREAD"], maxResults=max_results)
                .execute()
            )
            msgs = resp.get("messages", [])
            out = [self._parse_message(self._get_raw(m["id"])) for m in msgs]
            logger.info("Fetched %d messages", len(out))
            return out
        except HttpError:
            logger.exception("Gmail API error")
            return []

    def mark_as_important(self, message_id: str) -> bool:
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"addLabelIds": ["IMPORTANT"]},
            ).execute()
            return True
        except Exception:
            logger.exception("mark_as_important failed")
            return False

    def archive_email(self, message_id: str) -> bool:
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"removeLabelIds": ["INBOX"]},
            ).execute()
            return True
        except Exception:
            logger.exception("archive_email failed")
            return False

    def delete_message(self, message_id: str) -> bool:
        try:
            self.service.users().messages().delete(userId="me", id=message_id).execute()
            return True
        except Exception:
            logger.exception("delete_message failed")
            return False

    def create_draft(
        self,
        to_addr: str,
        subject: str,
        body_text: str,
        thread_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        raw = self._build_raw_message(to_addr, subject, body_text, thread_id)
        body = {"message": {"raw": raw}}
        return self.service.users().drafts().create(userId="me", body=body).execute()

    def send_message(
        self,
        to_addr: str,
        subject: str,
        body_text: str,
        thread_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        raw = self._build_raw_message(to_addr, subject, body_text, thread_id)
        body = {"raw": raw}
        return self.service.users().messages().send(userId="me", body=body).execute()

    # ------------- private helpers -------------
    def _get_raw(self, message_id: str) -> Dict[str, Any]:
        return (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )

    def _parse_message(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        payload = msg.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        return {
            "id": msg["id"],
            "threadId": msg.get("threadId"),
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
            "body": self._extract_body(payload),
            "labelIds": msg.get("labelIds", []),
        }

    def _extract_body(self, payload: Dict[str, Any]) -> str:
        parts_text = []

        def walk(p):
            if not p:
                return
            if p.get("parts"):
                for part in p["parts"]:
                    walk(part)
            else:
                data = p.get("body", {}).get("data")
                mime = p.get("mimeType", "")
                if data:
                    try:
                        txt = base64.urlsafe_b64decode(data.encode()).decode(errors="replace")
                    except Exception:
                        txt = ""
                    if mime == "text/html":
                        txt = re.sub(r"<[^<]+?>", "", txt)
                    parts_text.append(txt.strip())

        walk(payload)
        return "\n".join([p for p in parts_text if p])

    def _build_raw_message(
        self,
        to_addr: str,
        subject: str,
        body_text: str,
        thread_id: Optional[str] = None,
    ) -> str:
        msg = MIMEText(body_text, "plain")
        msg["to"] = to_addr
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        return raw