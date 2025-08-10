from services.llm_client import LLMClient
import logging

logger = logging.getLogger("handle_important_node")
logger.setLevel(logging.INFO)

llm = LLMClient()

def handle_important_node(state):
    emails = state.get("emails", [])
    updated = []

    for email in emails:
        if email["classification"]["label"] == "important":
            subj = email.get("subject", "")
            body = email.get("body", "")
            reply = llm.generate_reply(subj, body, tone="professional")
            email["draft_reply"] = reply
            logger.info(f"Drafted reply for: {subj}")

        updated.append(email)

    return {**state, "emails": updated}
