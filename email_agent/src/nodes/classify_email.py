from services.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

llm = LLMClient()

def classify_email_node(state):
    emails = state.get("emails", [])
    classified_emails = []

    for email in emails:
        subj = email.get("subject", "")
        body = email.get("body", "")
        classification = llm.classify_email(subj, body)
        email["classification"] = classification
        classified_emails.append(email)

    logger.info(f"Classified {len(classified_emails)} emails")
    return {**state, "emails": classified_emails}
