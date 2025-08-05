import os
import tempfile
import time
import streamlit as st
from dotenv import load_dotenv
from orchestrator.graph.graph_builder import create_graph

# --- Load environment ---
load_dotenv()

def load_config():
    return {
        "gemini_key": os.getenv("GEMINI_API_KEY"),
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "slack_token": os.getenv("SLACK_BOT_TOKEN"),
        "llm_provider": "gemini",
    }

# --- Streamlit page setup ---
st.set_page_config(
    page_title="Hiring Copilot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Hiring Copilot – Multi-Agent AI Workflow")
st.markdown(
    """
    Analyze a job description, process multiple resumes, rank candidates,
    generate emails, suggest interview slots, and post updates to Slack.
    """
)

# --- Input Section ---
st.header("1. Provide Job Description")
jd_text = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="Paste your job description..."
)

st.header("2. Upload Resumes (PDF)")
uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes:",
    type=["pdf"],
    accept_multiple_files=True
)

run_button = st.button("🚀 Run Pipeline")

def show_stage(status_placeholder, stage_text, delay=0.8):
    status_placeholder.info(stage_text)
    time.sleep(delay)

if run_button:
    if not jd_text.strip():
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one PDF resume.")
    else:
        # Placeholder for progress messages
        status_placeholder = st.empty()

        # Stage 1: Setup
        show_stage(status_placeholder, "Setting up pipeline...")
        config = load_config()
        graph = create_graph(config)

        # Stage 2: Saving uploaded files
        show_stage(status_placeholder, "Preparing resumes...")
        resume_paths = []
        for file in uploaded_files:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(file.read())
            temp_file.flush()
            resume_paths.append(temp_file.name)

        # Stage 3: Parsing JD
        show_stage(status_placeholder, "Parsing job description...")

        # Stage 4: Parsing resumes
        show_stage(status_placeholder, "Analyzing resumes...")

        # Stage 5: Ranking candidates
        show_stage(status_placeholder, "Ranking candidates and generating results...")

        # Stage 6: Running the graph
        final_state = graph.invoke({
            "jd_text": jd_text,
            "resume_paths": resume_paths
        })

        status_placeholder.success("All stages completed!")

        # --- Display Results ---
        st.header("Results")

        # JD Parsed
        jd_result = final_state.get("jd_result", {})
        st.subheader("Parsed Job Description")
        st.write(f"**Role:** {jd_result.get('role', 'N/A')}")
        st.write(f"**Skills:** {', '.join(jd_result.get('skills', []))}")
        st.write(f"**Tools:** {', '.join(jd_result.get('tools', []))}")
        st.write(f"**Experience (years):** {jd_result.get('experience_years', 'N/A')}")
        st.write(f"**Soft Skills:** {', '.join(jd_result.get('soft_skills', []))}")

        # Candidates
        st.subheader("Candidate Results")
        for idx, resume in enumerate(final_state.get("resume_results", [])):
            st.divider()
            st.markdown(f"### Candidate {idx+1}: {resume.get('name', 'Unknown')}")

            ranking = final_state["rankings"][idx]
            email = final_state["emails"][idx]
            calendar = final_state["calendars"][idx]
            slack = final_state["slacks"][idx]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Ranking:**")
                st.write(f"Score: {ranking['score']}")
                st.write(ranking['summary'])

            with col2:
                st.markdown("**Generated Email:**")
                st.write(f"Subject: {email['subject']}")
                st.text_area("Email Body", email["body"], height=180, key=f"email_{idx}")

            if ranking['score'] >= 75 and "calendar_event" in calendar:
                st.markdown(f"**Calendar Event:** {calendar['calendar_event']}")
            else:
                st.markdown("**Calendar Event:** Not scheduled")

            st.markdown("**Slack Notification:**")
            st.write(f"Status: {slack['status']}")
            st.write(f"Channel: {slack['channel']}")

        st.info("Check Slack and Google Calendar for notifications and events.")
