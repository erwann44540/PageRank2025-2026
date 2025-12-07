#!/usr/bin/env bash
# Crée un cluster Dataproc minimal. Personnalisez les variables ci-dessous.
set -euo pipefail

# Optional .env support
if [ -f "../.env" ]; then
  # shellcheck disable=SC1091
  source ../.env
fi

PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
CLUSTER_NAME="${CLUSTER_NAME:-dataproc-diagramme}"
REGION="${REGION:-europe-west1}"
# Leave ZONE empty to let Dataproc choose an auto-zone for the region (recommended)
ZONE="${ZONE:-}" # e.g. europe-west1-b or empty for auto-zone
SINGLE_NODE="${SINGLE_NODE:-false}" # true pour un cluster single-node (moins cher pour tests)
IMAGE_VERSION="${IMAGE_VERSION:-2.1-debian11}" # Dataproc image (ajustez si besoin)

# Security options: disable external IPs or specify a subnet
NO_EXTERNAL_IP="${NO_EXTERNAL_IP:-false}" # true to add --no-address
SUBNET="${SUBNET:-}" # e.g. projects/PROJECT/regions/REGION/subnetworks/SUBNET

MACHINE_TYPE="${MACHINE_TYPE:-n1-standard-4}"
NUM_WORKERS="${NUM_WORKERS:-2}"

if [ "$PROJECT_ID" = "YOUR_PROJECT_ID" ]; then
  echo "Veuillez éditer ${BASH_SOURCE[0]} ou le fichier .env et renseigner PROJECT_ID avant d'exécuter."
  exit 1
fi

ZONE_ARG=""
if [ -n "$ZONE" ]; then
  ZONE_ARG="--zone=$ZONE"
fi

SUBNET_ARG=""
if [ -n "$SUBNET" ]; then
  SUBNET_ARG="--subnet=$SUBNET"
fi

NO_ADDRESS_ARG=""
if [ "$NO_EXTERNAL_IP" = true ]; then
  NO_ADDRESS_ARG="--no-address"
fi

if [ "$SINGLE_NODE" = true ]; then
  echo "Création d'un cluster single-node ${CLUSTER_NAME} dans ${REGION}..."
  gcloud dataproc clusters create "$CLUSTER_NAME" \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    $ZONE_ARG \
    $SUBNET_ARG \
    --single-node $NO_ADDRESS_ARG \
    --image-version="$IMAGE_VERSION" \
    --master-machine-type="$MACHINE_TYPE"
else
  echo "Création d'un cluster standard ${CLUSTER_NAME} dans ${REGION}..."
  echo "Master et workers: ${MACHINE_TYPE}, nombre de workers: ${NUM_WORKERS}"
  gcloud dataproc clusters create "$CLUSTER_NAME" \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    $ZONE_ARG \
    $SUBNET_ARG \
    --master-machine-type="$MACHINE_TYPE" \
    --worker-machine-type="$MACHINE_TYPE" \
    --num-workers="$NUM_WORKERS" \
    $NO_ADDRESS_ARG \
    --image-version="$IMAGE_VERSION"
fi

echo "Cluster créé."
