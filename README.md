# 🤖 HR Copilot – AI-Powered Resume Screening Workflow

<div align="center">

**A fully autonomous, multi-agent AI workflow that streamlines the hiring pipeline**

📄 **Resume Parsing** → 🔍 **JD Analysis** → 🎯 **Candidate Ranking** → ✉️ **Email Generation** → 📆 **Google Calendar Scheduling** → 📢 **Slack Notifications**

Built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangSmith](https://smith.langchain.com), Gemini/OpenAI, and Streamlit.

---

![System Architecture](D:\Codes\ai-agent\archi.png)

</div>

---

## 🧠 Core Features

<table>
<tr>
<td>

✅ **JD Understanding**  
✅ **Multi-Resume Processing**  
✅ **Candidate Ranking System**  

</td>
<td>

✅ **Automated Email Writing**  
✅ **Calendar Slot Suggestion** (Google API)  
✅ **Slack Channel Notifications**  

</td>
<td>

✅ **Visual Streamlit UI**  
✅ **LangGraph Workflow**  
✅ **LangSmith Observability**  

</td>
</tr>
</table>

---

## 🗂️ Project Structure

```
AI-AGENT/
│
├── agents/                    # Individual autonomous agents
│   ├── calendar_agent.py      # Google Calendar integration agent
│   ├── candidate_ranker.py    # Resume-JD matching and scoring
│   ├── email_generator.py     # Automated email composition
│   ├── jd_analyzer.py         # Job description parsing and analysis
│   ├── notifier_agent.py      # Slack notification handling
│   └── resume_parser.py       # PDF resume extraction and parsing
│
├── orchestrator/
│   ├── graph/
│   │   ├── graph_builder.py   # LangGraph workflow definition
│   │   └── nodes.py           # Task-specific node logic
│   └── state/
│       └── context.py         # Shared LangGraph state schema
│
├── tools/                     # External utilities
│   ├── google_calendar.py     # Google Calendar API integration
│   └── slack_notifier.py      # Slack message handling
│
├── data/resumes/              # Sample resumes (PDFs)
├── env/                       # Your virtualenv folder
├── .env                       # Your environment variables
├── credentials.json           # Google Cloud credentials
├── token.pickle               # Google OAuth token
├── app.py                     # Streamlit UI entry point
├── main.py                    # (Optional) CLI script
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔁 Workflow Agents

| Stage | Agent Class | Description |
|-------|-------------|-------------|
| 🧾 **JD Parsing** | `JDAnalyzer` | Extracts role, skills, experience from job description |
| 📄 **Resume Parsing** | `ResumeParser` | Parses candidate resumes into structured format |
| 🎯 **Candidate Ranking** | `CandidateRanker` | Compares resume to JD and gives a match score |
| ✉️ **Email Generator** | `EmailGenerator` | Creates custom invite/reject emails |
| 📆 **Calendar Scheduler** | `CalendarAgent` | Suggests slots and generates Google Calendar event |
| 📢 **Slack Notifier** | `NotifierAgent` | Posts Slack message in a channel with candidate status |

---

## ⚙️ Setup Instructions

### 🐍 1. Create & Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate     # Windows: env\Scripts\activate
```

### 📦 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 3. Configure .env File

```bash
cp .env.example .env
```

Fill in your API keys:

```env
GEMINI_API_KEY=your_google_gemini_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_api_key
SLACK_BOT_TOKEN=your_slack_token
```

### 🔗 4. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project → Enable Calendar API
3. Create OAuth credentials (desktop app)
4. Download `credentials.json` and place in project root
5. First-time login will create `token.pickle` automatically
6. Ensure scopes allow access to your calendar

### 💬 5. Slack Bot Setup

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Create a new bot → Enable OAuth permissions:
   - `chat:write`
3. Install app to your workspace
4. Get the Bot Token and paste in `.env`
5. Set channel = `"#hiring"` (default) or configure in `NotifierAgent`

---

## ▶️ Run the App

```bash
streamlit run app.py
```

**Access it at:** http://localhost:8501

---

## 🧪 Sample Usage

| Step | Action |
|------|--------|
| 1️⃣ | Paste the JD in textarea |
| 2️⃣ | Upload 1 or more resumes (PDF) |
| 3️⃣ | Click "🚀 Run Pipeline" |
| 4️⃣ | Watch each step in the workflow live |

---

### Output Includes:
- 📊 Scores & summaries
- ✉️ Email drafts
- 📆 Interview slots booked 
- 📢 Slack updates

---

## 🧠 Tech Stack

<table>
<tr>
<th>Technology</th>
<th>Role</th>
</tr>
<tr>
<td><strong>LangGraph</strong></td>
<td>Agent workflow orchestration</td>
</tr>
<tr>
<td><strong>LangSmith</strong></td>
<td>Monitoring & debugging</td>
</tr>
<tr>
<td><strong>Gemini</strong></td>
<td>LLM provider for reasoning</td>
</tr>
<tr>
<td><strong>Streamlit</strong></td>
<td>Interactive UI</td>
</tr>
<tr>
<td><strong>Google API</strong></td>
<td>Calendar events</td>
</tr>
<tr>
<td><strong>Slack SDK</strong></td>
<td>Notifications</td>
</tr>
</table>

---


## 📝 Final Note

> **This project is a production-grade AI assistant tailored for HR teams and recruiters to drastically reduce manual screening effort. Plug in more agents, build UI logic, or deploy it on the cloud — it's built to scale.**

<div align="center">

### 🎉 **Happy hiring!** 🎉

---

⭐ **Star this repo if you found it helpful!** ⭐

</div>