from typing import Dict, Any
import logging
from services.gmail_client import GmailClient
from state import AppState

logger = logging.getLogger(__name__)

def fetch_emails_node(state: AppState) -> AppState:
    max_fetch = int(state.get("MAX_FETCH", 10))
    gmail = GmailClient()
    emails = gmail.fetch_unread_emails(max_results=max_fetch)
    logger.info("Fetched %d emails", len(emails))
    return {**state, "emails": emails}