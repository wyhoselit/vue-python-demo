## ADDED Requirements

### Requirement: GCP Container Registry Integration
The system SHALL automate the building of Docker images for the backend and frontend, pushing them to Google Container Registry (GCR), and ensuring they are pullable by the GKE cluster.

#### Scenario: Backend Image Build and Push Success
- **WHEN** the `deploy-k8s.sh` script is executed
- **THEN** a Docker image for the backend is built from `./backend/Dockerfile`
- **THEN** the backend image is tagged as `gcr.io/<PROJECT_ID>/vue-python-demo-backend:latest`
- **THEN** the backend image is successfully pushed to GCR

#### Scenario: Frontend Image Build and Push Success
- **WHEN** the `deploy-k8s.sh` script is executed
- **THEN** a Docker image for the frontend is built from `./frontend/Dockerfile`
- **THEN** the frontend image is tagged as `gcr.io/<PROJECT_ID>/vue-python-demo-frontend:latest`
- **THEN** the frontend image is successfully pushed to GCR

#### Scenario: GKE Image Pull Success
- **WHEN** Kubernetes manifests are applied to the GKE cluster
- **THEN** the GKE cluster successfully pulls the backend and frontend images from GCR
- **THEN** the pods start without image pull errors