#!/usr/bin/env bash
set -euo pipefail

# Optional .env support
if [ -f "../.env" ]; then
  # shellcheck disable=SC1091
  source ../.env
fi

PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
REGION="${REGION:-europe-west1}"
BASE_CLUSTER_NAME="${CLUSTER_NAME:-dataproc-diagramme}"

if [ "$PROJECT_ID" = "YOUR_PROJECT_ID" ]; then
  echo "Veuillez renseigner PROJECT_ID dans le .env avant d'exécuter ce script."
  exit 1
fi

NODE_COUNTS=(2 4 6)

for NODES in "${NODE_COUNTS[@]}"; do
  NUM_WORKERS=$((NODES - 1))
  export NUM_WORKERS
  export CLUSTER_NAME="${BASE_CLUSTER_NAME}-${NODES}nodes"

  ./create_cluster.sh
  ./submit_job.sh
  ./delete_cluster.sh

  echo "Expérience ${NODES} nœuds terminée."
  echo
done

echo "Toutes les expériences sont terminées."
