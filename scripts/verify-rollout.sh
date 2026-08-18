#!/bin/bash
# scripts/verify-rollout.sh - Verify a Kubernetes deployment rollout
# Usage: ./scripts/verify-rollout.sh <deployment_name>

set -euo pipefail

DEPLOYMENT_NAME="$1"

echo "Verifying rollout for deployment: ${DEPLOYMENT_NAME}"

# 1. Get the new replicaset (by creation timestamp)
REPLICASET=$(kubectl get rs -l app=${DEPLOYMENT_NAME} --sort-by=.metadata.creationTimestamp -o name | tail -1)
REPLICASET=${REPLICASET#replicaset/}
echo "New ReplicaSet: ${REPLICASET}"

# 2. Wait for the new replicaset to be ready
kubectl wait --for=condition=Ready "replicaset/${REPLICASET}" --timeout=120s
echo "New ReplicaSet is ready."

# 3. Check that old replicasets are scaled down to 0
OLD_REPLICASETS=$(kubectl get rs -l app=${DEPLOYMENT_NAME} --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[:-1][?(@.spec.replicas>0)].metadata.name}')

if [[ -n "${OLD_REPLICASETS}" ]]; then
    echo "ERROR: Old ReplicaSets still have replicas:"
    echo "${OLD_REPLICASETS}"
    exit 1
fi

echo "Old ReplicaSets scaled down successfully."
echo "Rollout for ${DEPLOYMENT_NAME} verified."