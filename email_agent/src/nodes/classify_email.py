from services.llm_client import LLMClient
from typing import Dict, Any

def classify_email_node(state: Dict[str,Any]) -> Dict[str,Any]:
    emails = state.get("emails",[])
    llm = LLMClient()
    results=[]
    for e in emails:
        subj = e.get("subject","")
        body = e.get("body", e.get("snippet",""))
        c = llm.classify_email(subj, body)
        e["classification"]=c["label"]
        e["classification_confidence"]=c["confidence"]
        results.append(e)
    state["emails"]=results
    return state
