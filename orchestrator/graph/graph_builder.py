from langgraph.graph import StateGraph
from orchestrator.state.context import WorkflowState
from orchestrator.graph.nodes import (
    jd_analyzer_node,
    resume_parser_node,
    candidate_ranker_node,
    email_generator_node,
    calendar_node,
    slack_notifier_node,
)

def create_graph(config):
    workflow = StateGraph(WorkflowState)

    workflow.add_node("jd_analyzer", lambda s: jd_analyzer_node(s, config))
    workflow.add_node("resume_parser", lambda s: resume_parser_node(s, config))
    workflow.add_node("candidate_ranker", lambda s: candidate_ranker_node(s, config))
    workflow.add_node("email_generator", lambda s: email_generator_node(s, config))
    workflow.add_node("calendar", lambda s: calendar_node(s, config))
    workflow.add_node("slack_notifier", lambda s: slack_notifier_node(s, config))

    workflow.add_edge("jd_analyzer", "resume_parser")
    workflow.add_edge("resume_parser", "candidate_ranker")
    workflow.add_edge("candidate_ranker", "email_generator")

    def email_next_step(state: WorkflowState):
        high_scores = [r["score"] for r in state["rankings"] if r["score"] >= 75]
        return "calendar" if high_scores else "slack_notifier"

    workflow.add_conditional_edges(
        "email_generator",
        email_next_step,
        {"calendar": "calendar", "slack_notifier": "slack_notifier"}
    )

    workflow.add_edge("calendar", "slack_notifier")
    workflow.set_entry_point("jd_analyzer")
    workflow.set_finish_point("slack_notifier")

    return workflow.compile()
