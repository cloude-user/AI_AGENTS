import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

llm = LLMClient()

def decide_action_node(state):
    emails = state.get("emails", [])
    processed = []

    for email in emails:
        label = email.get("classification", {}).get("label", "unknown")

        if label == "important":
            # Generate reply draft
            reply = llm.generate_reply(email.get("subject", ""), email.get("body", ""))
            email["draft_reply"] = reply
            logger.info(f"Drafted reply for: {email.get('subject')}")
        elif label in ["promotion", "spam"]:
            # Mark for deletion
            email["delete"] = True
            logger.info(f"Marked for deletion: {email.get('subject')}")

        processed.append(email)

    return {**state, "emails": processed}
