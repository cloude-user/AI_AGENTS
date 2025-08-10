from services.gmail_client import GmailClient
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def fetch_emails_node(state: Dict[str,Any]) -> Dict[str,Any]:
    max_fetch = int(state.get("MAX_FETCH", 10))
    gmail = GmailClient()
    emails = gmail.fetch_unread_emails(max_results=max_fetch)
    state["emails"]=emails
    logger.info("Fetched %d emails", len(emails))
    logger.info("Fetched %d emails", emails)
    return state
