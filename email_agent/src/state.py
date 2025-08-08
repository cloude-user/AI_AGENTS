from langgraph.graph import State
from typing import List, Dict, Optional

class EmailState(State):
    # List of email objects being processed
    emails: List[Dict] = []
    # Current email index (for processing in sequence)
    current_email: Optional[Dict] = None
    # Classification result for the current email
    classification: Optional[str] = None
    # Generated reply if applicable
    reply: Optional[str] = None
