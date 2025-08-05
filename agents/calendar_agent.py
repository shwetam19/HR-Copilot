import datetime
from tools.google_calendar import create_event

class CalendarAgent:
    def __init__(self, config):
        self.config = config

    def schedule(self, resume: dict, ranking: dict):
        """
        Schedule an interview for candidates with a high score.
        Returns available slots and a confirmed event link for the first slot.
        """
        print(f"\n[CalendarAgent] Scheduling for candidate: {resume.get('name')}")

        # Generate 3 interview slots dynamically: tomorrow, day after, and next day at 3 PM
        base_date = datetime.datetime.now() + datetime.timedelta(days=1)
        slots = [
            (base_date + datetime.timedelta(days=i)).replace(
                hour=15, minute=0, second=0, microsecond=0
            )
            for i in range(3)
        ]

        # First slot is chosen for creating a real event
        first_slot = slots[0]

        # Create a Google Calendar event (real)
        event_link = create_event(
            summary=f"Interview: {resume['name']}",
            description=(
                f"Interview for {resume['name']} "
                f"(Score: {ranking['score']})"
            ),
            start_time=first_slot,
            duration_minutes=30,
        )

        slot_strings = [dt.isoformat() for dt in slots]

        result = {
            "slots": slot_strings,
            "calendar_event": event_link,
            "status": "slots_suggested",
        }

        print(f"[CalendarAgent] Event created: {event_link}")
        return result
