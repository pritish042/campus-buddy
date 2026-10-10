#!/usr/bin/env bash
set -euo pipefail

# Deployment Script for Campus Buddy on Google Cloud Run
# Usage: ./deploy_cloud_run.sh <GCP_PROJECT_ID> [REGION]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <GCP_PROJECT_ID> [REGION]"
    echo "Example: $0 my-gcp-project-123 asia-south1"
    exit 1
fi

PROJECT_ID="$1"
REGION="${2:-asia-south1}"
SERVICE_NAME="campus-buddy"

echo "=== 🚀 Deploying Campus Buddy to Google Cloud Run ==="
echo "Project:  ${PROJECT_ID}"
echo "Region:   ${REGION}"
echo "Service:  ${SERVICE_NAME}"

# Configure gcloud
gcloud config set project "${PROJECT_ID}"

# Enable APIs
echo "Enabling necessary GCP APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com

# Deploy using ADK
echo "Launching ADK deployment..."
adk deploy cloud_run \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --service_name="${SERVICE_NAME}" \
  --with_ui \
  ./campus_buddy \
  -- \
  --set-secrets=GROQ_API_KEY=GROQ_API_KEY:latest \
  --set-env-vars=ADK_MODEL=groq/qwen/qwen3.8-27b \
  --allow-unauthenticated

echo "=== ✅ Deployment Complete ==="
