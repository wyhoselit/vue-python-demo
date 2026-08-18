## 1. Kubernetes Manifests Creation

- [x] 1.1 Create `kubernetes/backend-deployment.yaml` with Deployment and Service for backend
- [x] 1.2 Create `kubernetes/frontend-deployment.yaml` with Deployment and Service for frontend
- [x] 1.3 Create `kubernetes/ingress.yaml` with Ingress resource for routing

## 2. Deployment Automation Script

- [x] 2.1 Create `deploy-k8s.sh` script with variables for GCP project ID, GKE cluster name, zone
- [x] 2.2 Implement `gcloud auth` and `gcloud config set project` steps in script
- [x] 2.3 Implement `gcloud container clusters get-credentials` step in script
- [x] 2.4 Implement Docker build and push commands for backend image to GCR
- [x] 2.5 Implement Docker build and push commands for frontend image to GCR
- [x] 2.6 Implement `kubectl apply` commands for all Kubernetes manifests
- [x] 2.7 Add verification steps to check pod status after deployment

## 3. Configuration & Validation

- [x] 3.1 Update placeholder values in all Kubernetes manifests (project ID, domain, etc.)
- [x] 3.2 Update placeholder values in `deploy-k8s.sh` (project ID, cluster name, zone)
- [x] 3.3 Make `deploy-k8s.sh` executable (`chmod +x`)
- [x] 3.4 Validate Dockerfiles in `./backend` and `./frontend` are compatible with GKE
- [s] 3.5 Test deployment script execution in a non-production GKE environment
- [s] 3.6 Verify frontend accessibility via Ingress domain
- [s] 3.7 Verify backend API accessibility via Ingress domain (/api prefix)
- [s] 3.8 Document required IAM roles for GCP service account used by CI/CD or manual deployment

## 4. CI/CD Integration (Future / Optional)

- [s] 4.1 Update GitHub Actions workflows to trigger `deploy-k8s.sh` on merge to main
- [s] 4.2 Configure GitHub Actions secrets for GCP credentials and project details
- [s] 4.3 Add steps for automated testing before deployment in CI/CD pipeline