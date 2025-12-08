#!/usr/bin/env bash
set -euo pipefail

# Optional .env support
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
fi

PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
CLUSTER_NAME="${CLUSTER_NAME:-dataproc-diagramme}"
REGION="${REGION:-europe-west1}"

if [ "$PROJECT_ID" = "YOUR_PROJECT_ID" ]; then
  echo "Veuillez éditer le script ou le .env et renseigner PROJECT_ID." 
  exit 1
fi

echo "Suppression du cluster ${CLUSTER_NAME}..."
gcloud dataproc clusters delete "$CLUSTER_NAME" --region="$REGION" --project="$PROJECT_ID" --quiet

echo "Cluster supprimé."
