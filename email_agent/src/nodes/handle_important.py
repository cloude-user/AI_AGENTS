from services.llm_client import generate_reply
from services.gmail_client import draft_reply

def handle_important_node(state):
    email = state.current_email
    reply = generate_reply(email["subject"], email["body"])
    state.reply = reply
    draft_reply(email, reply)
    return state
