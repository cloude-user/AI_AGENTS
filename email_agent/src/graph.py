from langgraph.graph import StateGraph
from state import EmailState
from nodes.fetch_emails import fetch_emails_node
from nodes.classify_email import classify_email_node
from nodes.handle_important import handle_important_node
from nodes.handle_other import handle_other_node

def build_graph():
    graph = StateGraph(EmailState)

    graph.add_node("fetch_emails", fetch_emails_node)
    graph.add_node("classify_email", classify_email_node)
    graph.add_node("handle_important", handle_important_node)
    graph.add_node("handle_other", handle_other_node)

    graph.set_entry_point("fetch_emails")
    graph.add_edge("fetch_emails", "classify_email")

    graph.add_conditional_edges(
        "classify_email",
        lambda state: "handle_important" if state.classification.lower() == "important" else "handle_other"
    )

    return graph.compile()
