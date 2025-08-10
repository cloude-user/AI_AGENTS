from typing import TypedDict, List, Dict, Any

class AppState(TypedDict, total=False):
    emails: List[Dict[str, Any]]
    label: str
