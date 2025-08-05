from orchestrator.state.context import WorkflowState
from agents.jd_analyzer import JDAnalyzer
from agents.resume_parser import ResumeParser
from agents.candidate_ranker import CandidateRanker
from agents.email_generator import EmailGenerator
from agents.calendar_agent import CalendarAgent
from agents.notifier_agent import NotifierAgent

def jd_analyzer_node(state: WorkflowState, config):
    print("\n[Node Start] JD Analyzer Agent running...")
    jd_agent = JDAnalyzer(config)
    result = jd_agent.analyze(state["jd_text"])
    state["jd_result"] = result.model_dump()
    print("[Node Complete] JD Analyzer Agent finished.")
    return state

def resume_parser_node(state: WorkflowState, config):
    print("\n[Node Start] Resume Parser Agent running...")
    parser = ResumeParser(config)
    results = [parser.parse(path.strip()).model_dump() for path in state["resume_paths"]]
    state["resume_results"] = results
    print(f"[Node Complete] Resume Parser Agent finished. Parsed {len(results)} resumes.")
    return state

def candidate_ranker_node(state: WorkflowState, config):
    print("\n[Node Start] Candidate Ranker Agent running...")
    ranker = CandidateRanker(config)
    jd_data = state["jd_result"]
    rankings = [ranker.rank(jd_data, resume).model_dump() for resume in state["resume_results"]]
    state["rankings"] = rankings
    print("[Node Complete] Candidate Ranker Agent finished.")
    return state

def email_generator_node(state: WorkflowState, config):
    print("\n[Node Start] Email Generator Agent running...")
    email_gen = EmailGenerator(config)
    jd_data = state["jd_result"]
    emails = [
        email_gen.generate(resume, jd_data, ranking).model_dump()
        for resume, ranking in zip(state["resume_results"], state["rankings"])
    ]
    state["emails"] = emails
    print("[Node Complete] Email Generator Agent finished.")
    return state

def calendar_node(state: WorkflowState, config):
    print("\n[Node Start] Calendar Agent running...")
    cal_agent = CalendarAgent(config)
    calendars = []
    for resume, ranking in zip(state["resume_results"], state["rankings"]):
        if ranking["score"] >= 75:
            cal = cal_agent.schedule(resume, ranking)
        else:
            cal = {"status": "skipped"}
        calendars.append(cal if isinstance(cal, dict) else cal.model_dump())
    state["calendars"] = calendars
    print("[Node Complete] Calendar Agent finished.")
    return state

def slack_notifier_node(state: WorkflowState, config):
    print("\n[Node Start] Slack Notifier Agent running...")
    notifier = NotifierAgent(config)
    slacks = []
    for resume, ranking, email, calendar in zip(
        state["resume_results"], state["rankings"], state["emails"], state["calendars"]
    ):
        slack = notifier.send_notification(resume, ranking, email, calendar)
        slacks.append(slack.model_dump())
    state["slacks"] = slacks
    print("[Node Complete] Slack Notifier Agent finished.")
    return state
