import logging
from services.llm_client import LLMClient
from state import AppState

logger = logging.getLogger(__name__)
llm = LLMClient()

def decide_action_node(state: AppState) -> AppState:
    emails = state.get("emails", [])
    processed = []

    for email in emails:
        label = email.get("classification", {}).get("label", "unknown")

        if label == "important":
            reply = llm.generate_reply(
                email.get("subject", ""),
                email.get("body", ""),
                tone="professional"
            )
            email["draft_reply"] = reply
            logger.info("Drafted reply for: %s", email.get("subject"))
        elif label in ("promotion", "spam"):
            email["delete"] = True
            logger.info("Marked for deletion: %s", email.get("subject"))

        processed.append(email)

    return {**state, "emails": processed}