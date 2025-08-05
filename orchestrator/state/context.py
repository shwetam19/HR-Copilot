from typing import TypedDict, List, Dict, Any

class WorkflowState(TypedDict):
    jd_text: str
    resume_paths: List[str]

    jd_result: Dict[str, Any]
    resume_results: List[Dict[str, Any]]
    rankings: List[Dict[str, Any]]
    emails: List[Dict[str, Any]]
    calendars: List[Dict[str, Any]]
    slacks: List[Dict[str, Any]]
