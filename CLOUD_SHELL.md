# ☁️ Google Cloud Shell Development Guide for Campus Buddy

This guide explains how to run, test, and preview **Campus Buddy** inside **[Google Cloud Shell](https://shell.cloud.google.com)** using the built-in **Web Preview** feature.

> 💡 **No GCP Billing Account or Credit Card Required!**  
> Google Cloud Shell provides a free Linux VM in your browser. This development workflow does **not** create billable GCP resources, require Secret Manager, or use Cloud Run.

---

## 1. Open Google Cloud Shell

1. Navigate to **[https://shell.cloud.google.com](https://shell.cloud.google.com)** in your web browser.
2. Sign in with your Google account.

---

## 2. Clone the GitHub Repository

In the Cloud Shell terminal, clone your repository:

### For Public Repositories:
```bash
git clone https://github.com/YOUR_USERNAME/campus-buddy.git
cd campus-buddy
```

### For Private Repositories:
Authenticate with GitHub using the GitHub CLI (`gh`), which is pre-installed in Cloud Shell:
```bash
gh auth login
# Follow the prompts: select GitHub.com -> HTTPS -> Login with a web browser
# Paste the one-time code shown in Cloud Shell to authenticate
```
Then clone:
```bash
gh repo clone YOUR_USERNAME/campus-buddy
cd campus-buddy
```

---

## 3. Run One-Time Environment Setup

Run the automated setup script:
```bash
./scripts/cloud_shell_setup.sh
```

### What this script does:
1. Creates an isolated Python virtual environment (`.venv`).
2. Installs compatible versions of `google-adk`, `litellm`, and `pytest`.
3. Prompts securely for your **Groq API Key** (input is hidden with `read -s` and never saved in shell history or committed to Git).
4. Saves the key in a local `.env` file (protected with `chmod 600`).

*(If you ever need to update your key later, simply edit `.env` using `nano .env`.)*

---

## 4. Start the ADK Server & Web Preview

Launch the ADK Dev UI server:
```bash
./scripts/cloud_shell_run.sh
```

### Accessing the Web Preview:
1. Look at the top-right toolbar of Cloud Shell and click the **Web Preview** icon (looks like a screen with an eye: `[o]`).
2. Select **"Preview on port 8080"** (or click "Change port" $\rightarrow$ `8080` $\rightarrow$ "Change and Preview").
3. A new browser tab will open with the **ADK Web UI**.
4. In the top-left dropdown menu, select **`campus_buddy`**.

---

## 5. Try the 4 Demo Queries

Try sending these messages to Campus Buddy:

1. **Schedule & Canteen Query:**
   > *"What classes and food do I have on Friday?"*
   > *(Invokes `get_timetable` + `get_canteen_menu`)*

2. **CGPA Computation:**
   > *"Calculate my CGPA: grades 9, 8, 10; credits 4, 3, 3."*
   > *(Invokes `calculate_cgpa` and returns 9.0)*

3. **Save Session Reminder:**
   > *"Remember to submit my lab record."*
   > *(Invokes `add_reminder` and confirms storage in session state)*

4. **Retrieve Reminders:**
   > *"What do I need to remember?"*
   > *(Invokes `list_reminders` and lists saved items)*

---

## 6. Running Tests & Evaluations in Cloud Shell

Open a second Cloud Shell terminal tab (or stop the server with `Ctrl+C`) and run:

### Run Unit Tests (No API Key Required):
```bash
source .venv/bin/activate
pytest tests/ -v
```

### Run ADK Golden Evaluation (Uses Groq):
```bash
source .venv/bin/activate
python -m google.adk.cli eval campus_buddy campus_buddy/campus_buddy_golden.evalset.json --config_file_path campus_buddy/test_config.json --print_detailed_results
```

---

## 7. Stopping, Restarting & Pulling Updates

### Stopping the Server
Press **`Ctrl + C`** in the terminal where the server is running.

### Restarting the Server
```bash
./scripts/cloud_shell_run.sh
```

### Pulling Future Updates from GitHub
To pull changes without losing your local `.env` configuration:
```bash
git pull origin main
```
If you made local edits in Cloud Shell, you can safely sync with:
```bash
git stash
git pull origin main
git stash pop
```

---

## ⚠️ Important Details About Cloud Shell Web Preview

1. **Access & Security:**
   - Web Preview is **private** to your Google account session and requires you to be logged into Google.
   - It does **not** create a permanent public URL for outside users.
2. **Session State & Inactivity:**
   - Conversation sessions and reminders are stored in-memory (`InMemorySessionService`).
   - Active reminders persist throughout your chat session.
   - If Cloud Shell disconnects due to 20+ minutes of inactivity or the terminal container restarts, active session state resets cleanly.
3. **Cloud Run Deployment Status:**
   - Production Cloud Run deployment is currently **deferred** until a GCP billing account is activated.
   - All Cloud Run deployment configurations remain preserved in [DEPLOYMENT.md](file:///Users/pritishdash/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/3ABDA648-2049-4A24-A008-5681AE7A8018/DEPLOYMENT.md) and [deploy_cloud_run.sh](file:///Users/pritishdash/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/3ABDA648-2049-4A24-A008-5681AE7A8018/deploy_cloud_run.sh) for future use.
