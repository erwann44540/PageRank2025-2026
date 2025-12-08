#!/usr/bin/env bash
# Upload du job PySpark vers GCS et soumission Dataproc
set -euo pipefail

# Optional .env support
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
fi


PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
BUCKET="${BUCKET:-YOUR_BUCKET_NAME}"
CLUSTER_NAME="${CLUSTER_NAME:-dataproc-diagramme}"
REGION="${REGION:-europe-west1}"

JOB_LOCAL_PATH="${JOB_LOCAL_PATH:-diagramme.py}"
GCS_JOB_PATH="gs://${BUCKET}/jobs/diagramme.py"

GCS_INPUT="${GCS_INPUT:-gs://${BUCKET}/data/wikilinks_lang=en.ttl}"

# On encode dans le nom de sortie le nombre de nœuds si possible
NUM_WORKERS="${NUM_WORKERS:-2}"
NODES=$((NUM_WORKERS + 1))
GCS_OUTPUT="gs://${BUCKET}/outputs/diagramme-${NODES}nodes-$(date +%s)"

if [ "$PROJECT_ID" = "YOUR_PROJECT_ID" ] || [ "$BUCKET" = "YOUR_BUCKET_NAME" ]; then
  echo "Veuillez mettre à jour PROJECT_ID et BUCKET dans le .env avant exécution."
  exit 1
fi

# Uploader le job
echo "Upload du job vers ${GCS_JOB_PATH}..."
gsutil cp "$JOB_LOCAL_PATH" "$GCS_JOB_PATH"


if ! gsutil -q stat "$GCS_INPUT"; then
  echo "Le fichier d'entrée ${GCS_INPUT} est introuvable sur GCS."
  echo "Assure-toi d'avoir uploadé ton TTL décompressé vers ce chemin."
  exit 1
fi

# Soumettre le job
echo "Soumission du job pyspark diagramme.py vers le cluster ${CLUSTER_NAME} (region ${REGION})..."
echo "Input:  ${GCS_INPUT}"
echo "Output: ${GCS_OUTPUT}"

gcloud dataproc jobs submit pyspark "gs://${BUCKET}/jobs/diagramme.py" \
  --cluster="$CLUSTER_NAME" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --py-files="gs://${BUCKET}/jobs/rdd.py,gs://${BUCKET}/jobs/dataframe.py" \
  -- \
  --input "$GCS_INPUT" --output "$GCS_OUTPUT"

echo "Job soumis. Résultats attendus dans ${GCS_OUTPUT}."
