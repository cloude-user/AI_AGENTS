from ..services.llm_client import LLMClient
from ..state import AppState

def classify_email_node(state: AppState) -> AppState:
    llm = LLMClient()
    for email in state.get("emails", []):
        classification = llm.classify(email["snippet"])
        email["classification"] = classification
        email["is_important"] = classification.lower() == "important"
    return state
