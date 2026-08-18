---
type: Kubernetes Deployment
title: Kubernetes Deployment Overview
description: Overview of deploying the application to Kubernetes, including backend, frontend, and ingress configurations.
tags: [kubernetes, deployment, gcp, cloud]
---
# Kubernetes Deployment Overview

This section describes the deployment of the application to a Kubernetes cluster, focusing on the configuration files and the deployment script provided. The deployment is designed for Google Kubernetes Engine (GKE) but can be adapted for other Kubernetes environments.

## Deployment Components

The Kubernetes deployment consists of the following main components:

1.  **Backend Deployment**: Configures the FastAPI backend service.
    *   **Source File**: `kubernetes/backend-deployment.yaml`
    *   **Details**: Defines the Docker image, container ports, resource requests/limits, and environment variables for the backend.

2.  **Frontend Deployment**: Configures the Vue.js + Vuetify frontend application.
    *   **Source File**: `kubernetes/frontend-deployment.yaml`
    *   **Details**: Defines the Docker image, container ports, and resource requests/limits for the frontend.

3.  **Ingress**: Manages external access to the services in the cluster.
    *   **Source File**: `kubernetes/ingress.yaml`
    *   **Details**: Routes external HTTP/HTTPS traffic to the appropriate backend and frontend services based on host and path rules.

## Deployment Script

The `deploy-k8s.sh` script automates the deployment process to Kubernetes. It handles tasks such as:

*   Building Docker images
*   Pushing images to a container registry (e.g., Google Container Registry)
*   Applying Kubernetes manifest files (`.yaml`) to the cluster

**Source File**: `deploy-k8s.sh`

## Related OpenSpec Changes

This Kubernetes deployment was introduced through the following OpenSpec change:

*   **Design**: `openspec/changes/archive/2026-08-18-kubernetes-deployment/design.md`
*   **Proposal**: `openspec/changes/archive/2026-08-18-kubernetes-deployment/proposal.md`
*   **GCP Kubernetes Deployment Spec**: `openspec/changes/archive/2026-08-18-kubernetes-deployment/specs/gcp-kubernetes-deployment/spec.md`
*   **GCP Container Registry Integration Spec**: `openspec/changes/archive/2026-08-18-kubernetes-deployment/specs/gcp-container-registry-integration/spec.md`
