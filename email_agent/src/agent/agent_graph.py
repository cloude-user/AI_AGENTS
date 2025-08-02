# agent/agent_graph.py

from langgraph.graph import StateGraph, END
from agent.tools.gmail_fetcher import fetch_emails
from agent.tools.classifier import classify_email
from agent.tools.deleter import delete_email
from agent.tools.responder import generate_reply
from agent.tools.notifier import notify_user

from agent.tools.gmail_fetcher import fetch_emails
from agent.tools.classifier import classify_email
from agent.tools.delete_email import delete_promotions
from agent.tools.draft_reply import draft_response
from agent.tools.notifier import notify_user


# Define your custom state schema
class EmailState(dict):
    # email_id, label, content, etc. can be stored dynamically
    pass

# Create LangGraph nodes
graph = StateGraph(EmailState)

graph.add_node("fetch_emails", fetch_emails)
graph.add_node("classify", classify_email)
graph.add_node("delete", delete_email)
graph.add_node("respond", generate_reply)
graph.add_node("notify", notify_user)

# Add edges between the nodes
graph.set_entry_point("fetch_emails")
graph.add_edge("fetch_emails", "classify")

# Conditional branching based on classification
graph.add_conditional_edges("classify", lambda state:
    {
        "delete": state["label"] == "promotions",
        "respond": state["label"] == "job",
        END: state["label"] == "other"
    })

graph.add_edge("delete", "notify")
graph.add_edge("respond", "notify")
graph.add_edge("notify", END)

# Export the graph to be run
agent_executor = graph.compile()
