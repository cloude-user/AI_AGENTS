from typing import TypedDict, List, Dict, Any

class AppState(TypedDict, total=False):
    MAX_FETCH: int
    emails: List[Dict[str, Any]]
    label: str