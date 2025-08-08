from services.gmail_client import fetch_unread_emails

def fetch_emails_node(state):
    emails = fetch_unread_emails()
    if not emails:
        print("No unread emails found.")
        return state
    # Set the list of emails, process first one
    state.emails = emails
    state.current_email = emails[0]
    return state
