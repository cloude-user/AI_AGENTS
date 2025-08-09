from typing import TypedDict, Optional, List

class EmailData(TypedDict, total=False):
    id: str
    threadId: str
    labelIds: List[str]
    snippet: str
    payload: dict
    classification: Optional[str]
    is_important: Optional[bool]

class AppState(TypedDict, total=False):
    emails: List[EmailData]
    processed_count: int
