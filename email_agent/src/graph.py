# 
# from langgraph.graph import StateGraph
# from langgraph.constants import START, END
from langgraph.graph import StateGraph, START, END


from nodes.fetch_emails import fetch_emails_node
from nodes.classify_email import classify_email_node
from nodes.decide_action import decide_action_node

def build_graph():
    workflow = StateGraph(dict)  # Use dict-backed state for simplicity

    # Add nodes
    workflow.add_node("fetch_emails", fetch_emails_node)
    workflow.add_node("classify_email", classify_email_node)
    workflow.add_node("decide_action", decide_action_node)

    # Define flow
    workflow.add_edge(START, "fetch_emails")
    workflow.add_edge("fetch_emails", "classify_email")
    workflow.add_edge("classify_email", "decide_action")
    workflow.add_edge("decide_action", END)

    return workflow.compile()
