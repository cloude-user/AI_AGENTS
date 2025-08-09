from langgraph.graph import StateGraph, START, END
from state import AppState
from nodes.fetch_emails import fetch_emails_node
from nodes.classify_email import classify_email_node
from nodes.handle_important import handle_important_node
from nodes.handle_other import handle_other_node

def build_graph():
    workflow = StateGraph(AppState)

    workflow.add_node("fetch_emails", fetch_emails_node)
    workflow.add_node("classify_email", classify_email_node)
    workflow.add_node("handle_important", handle_important_node)
    workflow.add_node("handle_other", handle_other_node)

    workflow.add_edge(START, "fetch_emails")
    workflow.add_edge("fetch_emails", "classify_email")

    # Conditional branching
    def route_email(state: AppState) -> str:
        if state.get("emails"):
            for email in state["emails"]:
                if email.get("is_important"):
                    return "handle_important"
            return "handle_other"
        return END

    workflow.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "handle_important": "handle_important",
            "handle_other": "handle_other",
            END: END
        }
    )

    workflow.add_edge("handle_important", END)
    workflow.add_edge("handle_other", END)

    return workflow.compile()
