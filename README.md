# 🎒 Campus Buddy — College Assistant AI Agent

**Campus Buddy** is an agentic AI college assistant built with [Google ADK (Agent Development Kit)](https://adk.dev) and [LiteLLM](https://docs.litellm.ai/) backed by Groq's high-speed inference engine (`groq/qwen/qwen3.8-27b`).

---

## 🌟 Capabilities & Tools

1. **Class Timetables (`get_timetable`)**: Retrieves scheduled classes for any weekday (Monday through Friday) with input normalization.
2. **Canteen Menus (`get_canteen_menu`)**: Looks up daily food and meal menus.
3. **Accurate CGPA Calculation (`calculate_cgpa`)**: Computes exact credit-weighted grade point averages, strictly validating inputs against non-finite values, out-of-range grades (0–10), and non-positive credits.
4. **Session Reminders (`add_reminder` & `list_reminders`)**: Saves and retrieves to-do items directly within ADK's conversation session state.

---

## 📁 Project Structure

```text
.
├── campus_buddy/
│   ├── __init__.py                     # Package entry point exporting root_agent
│   ├── agent.py                        # ADK agent configuration and prompt instructions
│   ├── tools.py                        # Python tool implementations with type hints & docstrings
│   ├── sample_data.py                  # Demo college schedule and menu dataset
│   ├── campus_buddy_golden.evalset.json # Golden evaluation dataset for ADK eval
│   ├── test_config.json                # ADK evaluation scoring criteria
│   └── requirements.txt                # Agent dependency manifest
├── scripts/
│   ├── cloud_shell_setup.sh            # Automated Cloud Shell setup script
│   └── cloud_shell_run.sh              # Cloud Shell Web Preview server runner
├── tests/
│   ├── test_tools.py                   # Pytest suite for tool logic, validation & session state
│   └── test_agent_config.py            # Pytest suite for agent registration and tool binding
├── .env.example                        # Template for environment configuration (placeholders only)
├── .gitignore                          # Git ignore rules (strictly excludes .env and caches)
├── .gcloudignore                       # Excludes secrets from Google Cloud deployments
├── CLOUD_SHELL.md                      # Complete guide for Google Cloud Shell Web Preview
├── DEPLOYMENT.md                       # Cloud Run deployment reference (deferred)
├── deploy_cloud_run.sh                 # Cloud Run deployment script (deferred)
├── requirements.txt                    # Top-level dependencies
└── README.md                           # Documentation and usage guide
```

---

## ☁️ Google Cloud Shell Development (Recommended — No Billing Required)

If developing in **Google Cloud Console** without a billing account, use our streamlined Cloud Shell setup:
👉 See the step-by-step guide in **[CLOUD_SHELL.md](CLOUD_SHELL.md)**.

Quick summary:
```bash
# 1. Setup virtual environment and configure Groq API key
./scripts/cloud_shell_setup.sh

# 2. Run server
./scripts/cloud_shell_run.sh

# 3. Click 'Web Preview' -> 'Preview on port 8080' in Cloud Shell
```

---

## 💻 Local Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- A free **Groq API Key** from [console.groq.com/keys](https://console.groq.com/keys)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your Groq API key:
# GROQ_API_KEY=gsk_your_key_here
# ADK_MODEL=groq/qwen/qwen3.8-27b
```

### 4. Run Unit Tests (No Credentials Needed)
```bash
pytest tests/ -v
```

### 5. Launch ADK Web Dev UI Locally
```bash
adk web --host 127.0.0.1 --port 8000 .
```
Open **`http://localhost:8000/dev-ui/`** and select `campus_buddy`.

### 6. Run ADK Golden Evaluations
```bash
python -m google.adk.cli eval campus_buddy campus_buddy/campus_buddy_golden.evalset.json --config_file_path campus_buddy/test_config.json --print_detailed_results
```

---

## 💬 4 Core Demo Queries to Try

1. **Schedule & Menu:**
   > *"What classes and food do I have on Friday?"*
2. **GPA Calculation:**
   > *"Calculate my CGPA: grades 9, 8, 10; credits 4, 3, 3."*
3. **Save Session Reminder:**
   > *"Remember to submit my lab record."*
4. **List Reminders:**
   > *"What do I need to remember?"*

---

## 🚀 Cloud Run Deployment (Deferred)

Cloud Run deployment files are preserved in **[DEPLOYMENT.md](DEPLOYMENT.md)** and **[deploy_cloud_run.sh](deploy_cloud_run.sh)** for when a billing-enabled GCP project is ready.
