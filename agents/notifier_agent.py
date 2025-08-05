from tools.slack_notifier import SlackNotifier, SlackResult

class NotifierAgent:
    def __init__(self, config: dict):
        self.notifier = SlackNotifier(
            token=config.get("slack_token"),
            channel="#hiring"
        )

    def send_notification(self, candidate: dict, ranking: dict, email: dict, calendar: dict) -> SlackResult:
        decision = "Invite" if ranking["score"] >= 75 else "Rejection"

        message = f"""
*Candidate Update: {candidate.get('name', 'Unknown')}*
Score: {ranking['score']}
Decision: {decision}

Summary: {ranking['summary']}

Email Prepared: {email['subject']}
"""

        if calendar.get("calendar_event"):
            message += f"\nCalendar Event: {calendar['calendar_event']}"

        return self.notifier.send_message(message)
