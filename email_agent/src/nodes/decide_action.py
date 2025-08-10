from services.llm_client import LLMClient
from services.gmail_client import GmailClient
from typing import Dict, Any
import os

AUTO_DELETE = os.getenv("AUTO_DELETE_PROMOTIONS","false").lower() in ("1","true","yes")
AUTO_SEND = os.getenv("AUTO_SEND","false").lower() in ("1","true","yes")

def decide_action_node(state: Dict[str,Any]) -> Dict[str,Any]:
    gmail = GmailClient()
    llm = LLMClient()
    out=[]
    for e in state.get("emails",[]):
        label = e.get("classification","promotional")
        conf = e.get("classification_confidence",0.0)
        msg_id = e.get("id")
        sender = e.get("from")
        thread_id = e.get("threadId")
        # promotional / useless
        if label=="promotional" and conf>0.6:
            if AUTO_DELETE:
                gmail.delete_message(msg_id)
                e["_action"]="deleted"
            else:
                gmail.archive_email(msg_id)
                e["_action"]="archived"
        else:
            # important or personal -> generate draft
            tone = "professional"
            if label=="personal":
                tone="friendly"
            draft_text = llm.generate_reply(e.get("subject",""), e.get("body",""), tone=tone)
            gmail.create_draft(to_addr=sender, subject="Re: "+e.get("subject",""), body_text=draft_text, thread_id=thread_id)
            e["_action"]="draft_created"
            if AUTO_SEND:
                gmail.send_message(to_addr=sender, subject="Re: "+e.get("subject",""), body_text=draft_text, thread_id=thread_id)
                e["_action"]="sent"
        out.append(e)
    state["emails"]=out
    return state
