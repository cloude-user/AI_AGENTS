from services.llm_client import classify_email

def classify_email_node(state):
    email = state.current_email
    category = classify_email(email["subject"], email["body"])
    state.classification = category
    return state
