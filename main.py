import os
from dotenv import load_dotenv
from orchestrator.graph.graph_builder import create_graph

# Load API keys and configs
load_dotenv()

def load_config():
    return {
        "gemini_key": os.getenv("GEMINI_API_KEY"),
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "slack_token": os.getenv("SLACK_BOT_TOKEN"),
        "llm_provider": "gemini"
    }

def main():
    print("🔁 Starting Hiring Copilot (LangGraph powered)...")
    config = load_config()

    # Collect inputs
    jd_text = input("Paste job description text: ")
    resume_paths = input("Enter resume PDF path(s) (comma-separated for multiple): ").split(",")

    # Build the graph
    graph = create_graph(config)

    # Run the graph
    final_state = graph.invoke({
        "jd_text": jd_text,
        "resume_paths": [path.strip() for path in resume_paths],
    })

    print("\n=== Workflow completed! ===")

    # Print JD
    jd = final_state.get("jd_result", {})
    print("\nJob Description Parsed:")
    print(jd)

    # Print results for each resume
    for idx, resume in enumerate(final_state.get("resume_results", [])):
        print("\n" + "="*50)
        print(f"Candidate {idx+1}: {resume.get('name','Unknown')}")
        print("="*50)

        ranking = final_state["rankings"][idx]
        email = final_state["emails"][idx]
        calendar = final_state["calendars"][idx]
        slack = final_state["slacks"][idx]

        print("\n📝Resume Summary:")
        print(resume)

        print("\n🧑‍💻Candidate Ranking:")
        print(f"Score: {ranking['score']}")
        print(f"Summary: {ranking['summary']}")

        print("\n📧Generated Email:")
        print(f"Subject: {email['subject']}")
        print(f"Body:\n{email['body']}")

        print("\n📆Calendar Suggestions:")
        print(calendar)

        print("\n🔔Slack Notification Status:")
        print(slack)


if __name__ == "__main__":
    main()
