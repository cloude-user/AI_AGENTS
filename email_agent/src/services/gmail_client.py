import os, json, base64, logging, re
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

logger = logging.getLogger("gmail_client")
logger.setLevel(logging.INFO)

class GmailClient:
    def __init__(self):
        token_str = os.getenv("GMAIL_JSON_TOKEN")
        if not token_str:
            raise ValueError("GMAIL_JSON_TOKEN env var not set")
        try:
            token_info = json.loads(token_str)
        except Exception:
            raise ValueError("GMAIL_JSON_TOKEN must be valid JSON (single-line)")

        self.creds = Credentials.from_authorized_user_info(token_info, token_info.get("scopes"))
        # Refresh if expired
        try:
            if not self.creds.valid or self.creds.expired:
                if self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    raise RefreshError("No refresh token available")
        except RefreshError:
            logger.exception("RefreshError: refresh token expired or revoked")
            raise
        except Exception:
            logger.exception("Unexpected error refreshing token")
            raise

        self.service = build("gmail", "v1", credentials=self.creds)

    def fetch_unread_emails(self, max_results:int=10) -> List[Dict[str,Any]]:
        try:
            resp = self.service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=max_results).execute()
            msgs = resp.get("messages", []) or []
            out=[]
            for m in msgs:
                full = self.service.users().messages().get(userId="me", id=m["id"], format="full").execute()
                out.append(self._parse_message(full))
            logger.info("Fetched %d messages", len(out))
            return out
        except HttpError:
            logger.exception("Gmail API error during fetch_unread_emails")
            return []

    def _parse_message(self, msg)->Dict[str,Any]:
        payload = msg.get("payload",{})
        headers = payload.get("headers",[])
        header_map = {h.get("name"): h.get("value") for h in headers}
        subject = header_map.get("Subject","")
        sender = header_map.get("From","")
        to = header_map.get("To","")
        date = header_map.get("Date","")
        snippet = msg.get("snippet","")
        body = self._get_body_text(payload)
        return {
            "id": msg.get("id"),
            "threadId": msg.get("threadId"),
            "subject": subject,
            "from": sender,
            "to": to,
            "date": date,
            "snippet": snippet,
            "body": body,
            "labelIds": msg.get("labelIds", [])
        }

    def _get_body_text(self, payload)->str:
        parts_text=[]
        def walk(p):
            if not p:
                return
            if p.get("parts"):
                for x in p["parts"]:
                    walk(x)
            else:
                data = p.get("body",{}).get("data")
                mime = p.get("mimeType","")
                if data:
                    try:
                        txt = base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")
                    except Exception:
                        txt = ""
                    if mime=="text/html":
                        txt = re.sub("<[^<]+?>","",txt)
                    parts_text.append(txt)
        walk(payload)
        return "\n".join([p.strip() for p in parts_text if p and p.strip()])

    def mark_as_important(self, message_id:str)->bool:
        try:
            self.service.users().messages().modify(userId="me", id=message_id, body={"addLabelIds":["IMPORTANT"]}).execute()
            return True
        except Exception:
            logger.exception("mark_as_important failed")
            return False

    def archive_email(self, message_id:str)->bool:
        try:
            self.service.users().messages().modify(userId="me", id=message_id, body={"removeLabelIds":["INBOX"]}).execute()
            return True
        except Exception:
            logger.exception("archive_email failed")
            return False

    def delete_message(self, message_id:str)->bool:
        try:
            self.service.users().messages().delete(userId="me", id=message_id).execute()
            return True
        except Exception:
            logger.exception("delete_message failed")
            return False

    def create_draft(self, to_addr:str, subject:str, body_text:str, thread_id:Optional[str]=None)->Dict[str,Any]:
        from email.mime.text import MIMEText
        msg = MIMEText(body_text, "plain")
        msg["to"]=to_addr
        msg["subject"]=subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        body={"message":{"raw":raw}}
        if thread_id:
            body["message"]["threadId"]=thread_id
        draft = self.service.users().drafts().create(userId="me", body=body).execute()
        return draft

    def send_message(self, to_addr:str, subject:str, body_text:str, thread_id:Optional[str]=None)->Dict[str,Any]:
        from email.mime.text import MIMEText
        msg = MIMEText(body_text, "plain")
        msg["to"]=to_addr
        msg["subject"]=subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        body={"raw":raw}
        if thread_id:
            body["threadId"]=thread_id
        sent = self.service.users().messages().send(userId="me", body=body).execute()
        return sent
