# 🚀 Google Cloud Run Deployment Guide for Campus Buddy

This guide explains how to deploy **Campus Buddy** with its built-in browser UI to Google Cloud Run using Google Secret Manager for secure credentials.

---

## 🔒 Security Best Practices
- **Never embed API keys** in source code, Dockerfiles, or `.env` files committed to version control.
- All secrets are stored in **Google Secret Manager** and mounted as environment variables at runtime.
- The [.gcloudignore](file:///Users/pritishdash/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/3ABDA648-2049-4A24-A008-5681AE7A8018/.gcloudignore) file ensures `.env` files are never uploaded during container builds.

---

## 📋 Prerequisites
1. A Google Cloud project with billing enabled.
2. The Google Cloud SDK (`gcloud` CLI) installed locally, or use **[Google Cloud Shell](https://shell.cloud.google.com)** (recommended — `gcloud` is pre-installed).

---

## 🛠️ Step-by-Step Deployment

### Step 1: Login & Select Project
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable Required GCP APIs
```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com
```

### Step 3: Create the Secret in Secret Manager
Replace with your actual Groq API key (starts with `gsk_`):
```bash
echo -n "gsk_your_groq_api_key_here" | gcloud secrets create GROQ_API_KEY \
  --data-file=- \
  --replication-policy="automatic"
```

### Step 4: Grant Cloud Run Access to the Secret
Find the Compute Engine default service account (or Cloud Run service account) and grant `secretAccessor` permission:
```bash
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding GROQ_API_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Step 5: Deploy with Google ADK
Run this command from the project root folder:
```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=asia-south1 \
  --service_name=campus-buddy \
  --with_ui \
  ./campus_buddy \
  -- \
  --set-secrets=GROQ_API_KEY=GROQ_API_KEY:latest \
  --set-env-vars=ADK_MODEL=groq/qwen/qwen3.8-27b \
  --allow-unauthenticated
```

> ℹ️ **Port & UI Configuration:**
> - Cloud Run dynamically assigns a `PORT` (typically 8080). ADK automatically detects and binds to this port.
> - The `--with_ui` flag serves the ADK Dev UI web interface at `https://<service-url>/dev-ui/`.

---

## 💾 Session & Memory Persistence Details

- **Implemented Session Storage:** In-memory session service (`InMemorySessionService` / local in-memory storage).
- **Behavior:** Conversations and reminders are preserved during the active container session.
- **Container Restarts & Scale-to-Zero:** If Cloud Run scales to zero instances due to inactivity or a new revision is deployed, in-memory session state resets for new instances. For permanent multi-instance persistent memory across container lifecycles, configure `--session_service_uri` to point to a database or Cloud Storage bucket.

---

## 🧪 Verification & Live Testing

### 1. Web Browser Interface
Open the Service URL printed by the deployment:
👉 **`https://<SERVICE_URL>/dev-ui/`**

### 2. Direct REST API Test
```bash
SERVICE_URL="https://campus-buddy-xxxx.a.run.app"

# Test agent endpoint
curl -s -X POST "${SERVICE_URL}/run" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "campus_buddy",
    "user_id": "student_1",
    "session_id": "session_1",
    "new_message": {
      "role": "user",
      "parts": [{"text": "What classes and food do I have on Friday?"}]
    }
  }'
```

---

## 🧹 Cleanup (Avoid Unwanted Billing)

When finished with the demo, remove the Cloud Run service and secret:
```bash
# Delete Cloud Run Service
gcloud run services delete campus-buddy --region=asia-south1 --quiet

# Delete Secret
gcloud secrets delete GROQ_API_KEY --quiet
```
