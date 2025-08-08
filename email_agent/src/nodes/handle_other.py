def handle_other_node(state):
    print(f"Email '{state.current_email['subject']}' is {state.classification}, skipping...")
    return state
