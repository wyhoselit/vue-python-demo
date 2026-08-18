#!/bin/bash
# deploy-k8s.sh - Deploy Vue-Python Demo to GKE
# Usage: ./deploy-k8s.sh [PROJECT_ID] [CLUSTER_NAME] [ZONE] [DOMAIN]

set -euo pipefail

# Configuration - Update these values or pass as arguments
PROJECT_ID="${1:-your-gcp-project-id}"
CLUSTER_NAME="${2:-vue-python-demo-cluster}"
ZONE="${3:-us-central1-a}"
DOMAIN="${4:-your-domain.com}"

# Derived values
BACKEND_IMAGE="gcr.io/${PROJECT_ID}/vue-python-demo-backend:latest"
FRONTEND_IMAGE="gcr.io/${PROJECT_ID}/vue-python-demo-frontend:latest"
K8S_DIR="$(dirname "$0")/kubernetes"

echo "=== Vue-Python Demo GKE Deployment ==="
echo "Project ID: ${PROJECT_ID}"
echo "Cluster: ${CLUSTER_NAME}"
echo "Zone: ${ZONE}"
echo "Domain: ${DOMAIN}"
echo "Backend Image: ${BACKEND_IMAGE}"
echo "Frontend Image: ${FRONTEND_IMAGE}"
echo ""

# Validate required tools
for cmd in gcloud docker kubectl; do
    if ! command -v "${cmd}" &> /dev/null; then
        echo "ERROR: ${cmd} not found in PATH"
        exit 1
    fi
done

# 1. Authenticate with GCP
echo "=== Step 1: Authenticating with GCP ==="
gcloud auth configure-docker --quiet

# 2. Set GCP project
echo "=== Step 2: Setting GCP project ==="
gcloud config set project "${PROJECT_ID}"

# 3. Get GKE credentials
echo "=== Step 3: Getting GKE cluster credentials ==="
gcloud container clusters get-credentials "${CLUSTER_NAME}" --zone "${ZONE}" --project "${PROJECT_ID}"

# 4. Build and push backend image
echo "=== Step 4: Building and pushing backend image ==="
docker build -t "${BACKEND_IMAGE}" ./backend
docker push "${BACKEND_IMAGE}"

# 5. Build and push frontend image
echo "=== Step 5: Building and pushing frontend image ==="
docker build -t "${FRONTEND_IMAGE}" ./frontend
docker push "${FRONTEND_IMAGE}"

# 6. Update ingress domain placeholder
echo "=== Step 6: Updating Ingress domain ==="
sed -i "s/your-domain.com/${DOMAIN}/g" "${K8S_DIR}/ingress.yaml"

# 7. Apply Kubernetes manifests
echo "=== Step 7: Applying Kubernetes manifests ==="
kubectl apply -f "${K8S_DIR}/backend-deployment.yaml"
kubectl apply -f "${K8S_DIR}/frontend-deployment.yaml"
kubectl apply -f "${K8S_DIR}/ingress.yaml"

# 8. Verify deployment
echo "=== Step 8: Verifying deployment ==="
echo "Waiting for pods to be ready..."
./scripts/verify-rollout.sh backend
./scripts/verify-rollout.sh frontend

echo ""
echo "=== Deployment Status ==="
kubectl get pods -l app=backend
kubectl get pods -l app=frontend
kubectl get services
kubectl get ingress

echo ""
echo "=== Deployment Complete ==="
echo "Frontend: http://${DOMAIN}"
echo "Backend API: http://${DOMAIN}/api"