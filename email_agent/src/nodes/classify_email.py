import logging
from services.llm_client import LLMClient
from state import AppState

logger = logging.getLogger(__name__)
llm = LLMClient()

def classify_email_node(state: AppState) -> AppState:
    emails = state.get("emails", [])
    classified = []

    for email in emails:
        subj = email.get("subject", "")
        body = email.get("body", "")
        classification = llm.classify_email(subj, body)
        email["classification"] = classification
        classified.append(email)

    logger.info("Classified %d emails", len(classified))
    return {**state, "emails": classified}