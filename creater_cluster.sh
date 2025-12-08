#!/usr/bin/env bash
# Crée un cluster Dataproc. S'appuie sur .env pour la config.
set -euo pipefail

# Optional .env support
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
fi

PROJECT_ID="${PROJECT_ID:-YOUR_PROJECT_ID}"
CLUSTER_NAME="${CLUSTER_NAME:-dataproc-diagramme}"
REGION="${REGION:-europe-west1}"

ZONE="${ZONE:-}"

# true => cluster single-node, false => master + workers
SINGLE_NODE="${SINGLE_NODE:-false}"

# Version Dataproc
IMAGE_VERSION="${IMAGE_VERSION:-2.1-debian11}"

# Réseau / IP
NO_EXTERNAL_IP="${NO_EXTERNAL_IP:-false}"
SUBNET="${SUBNET:-}"  

MACHINE_TYPE="${MACHINE_TYPE:-n1-standard-2}"

NUM_WORKERS="${NUM_WORKERS:-2}"

MASTER_BOOT_DISK_SIZE="${MASTER_BOOT_DISK_SIZE:-200}"
WORKER_BOOT_DISK_SIZE="${WORKER_BOOT_DISK_SIZE:-200}"

if [ "$PROJECT_ID" = "YOUR_PROJECT_ID" ]; then
  echo "Veuillez éditer .env et renseigner PROJECT_ID avant d'exécuter."
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
  echo "Création d'un cluster *single-node* ${CLUSTER_NAME} dans ${REGION}..."
  gcloud dataproc clusters create "$CLUSTER_NAME" \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    $ZONE_ARG \
    $SUBNET_ARG \
    --single-node $NO_ADDRESS_ARG \
    --image-version="$IMAGE_VERSION" \
    --master-machine-type="$MACHINE_TYPE" \
    --master-boot-disk-size="$MASTER_BOOT_DISK_SIZE"
else
  echo "Création d'un cluster standard ${CLUSTER_NAME} dans ${REGION}..."
  echo "Master et workers: ${MACHINE_TYPE}, nombre de workers: ${NUM_WORKERS}"

  gcloud dataproc clusters create "$CLUSTER_NAME" \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    $ZONE_ARG \
    $SUBNET_ARG \
    --master-machine-type="$MACHINE_TYPE" \
    --master-boot-disk-size="$MASTER_BOOT_DISK_SIZE" \
    --worker-machine-type="$MACHINE_TYPE" \
    --worker-boot-disk-size="$WORKER_BOOT_DISK_SIZE" \
    --num-workers="$NUM_WORKERS" \
    $NO_ADDRESS_ARG \
    --image-version="$IMAGE_VERSION"
fi

echo "Cluster créé."
