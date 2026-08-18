## Context

The current application deployment uses Docker Compose for local development and potentially for production, lacking the scalability, high availability, and advanced features required for a robust production environment. The goal is to transition to a Kubernetes-based deployment on Google Kubernetes Engine (GKE).

## Goals / Non-Goals

**Goals:**
- Deploy the Vue-Python demo application (backend and frontend) to GKE.
- Utilize Kubernetes Deployments, Services, and Ingress for managing the application.
- Automate image building and pushing to Google Container Registry (GCR).
- Provide a clear, executable script for deployment.

**Non-Goals:**
- Implementing a full CI/CD pipeline (though the script can be integrated later).
- Advanced Kubernetes features like Helm charts, Istio, or custom operators in this initial phase.
- Detailed observability setup (e.g., configuring Prometheus, Grafana, or a full OpenTelemetry collector in Kubernetes).
- Managing database persistence for the backend; the current SQLite setup is considered sufficient for this demo migration.

## Decisions

1.  **Containerization Strategy:** Both backend and frontend will be containerized. Backend will use a Python-based image, and frontend will use an Nginx-based image.
    *   **Rationale:** Existing Dockerfiles provide a clear path to containerization. GKE requires containerized applications.
    *   **Alternatives Considered:** None, as containerization is fundamental to Kubernetes.

2.  **Image Registry:** Google Container Registry (GCR) will be used for storing Docker images.
    *   **Rationale:** Native integration with GCP and GKE, simplifying authentication and image pulling.
    *   **Alternatives Considered:** Docker Hub, Artifact Registry (also GCP-native, but GCR is simpler for a demo).

3.  **Kubernetes Resource Types:**
    *   **Deployment:** For managing stateless application instances (backend and frontend).
        *   **Rationale:** Provides declarative updates, rollbacks, and replica management.
    *   **Service:** For exposing application components within the cluster.
        *   **Rationale:** Enables stable network endpoints for pods.
    *   **Ingress:** For external HTTP/HTTPS access and routing traffic to frontend/backend services.
        *   **Rationale:** Centralized entry point, host-based routing, and SSL termination capabilities (via annotations).
    *   **Alternatives Considered:** DaemonSets, StatefulSets (not applicable for stateless components), NodePort/LoadBalancer Services for internal components (less flexible than Ingress for external access).

4.  **Observability:** Initial Kubernetes manifests will *not* include detailed OpenTelemetry collector configurations. Environment variables for OpenTelemetry will be commented out.
    *   **Rationale:** Keep initial deployment simple. Advanced observability can be added in a separate phase, potentially leveraging GCP's native monitoring or a dedicated OpenTelemetry Operator for Kubernetes.
    *   **Alternatives Considered:** Including a basic OpenTelemetry collector sidecar (adds complexity to initial deployment).

5.  **Deployment Automation:** A shell script (`deploy-k8s.sh`) will handle image building, pushing, and manifest application.
    *   **Rationale:** Provides a simple, transparent, and reproducible way to deploy the application for demonstration purposes.
    *   **Alternatives Considered:** Terraform/Pulumi (more robust for IaC but adds a learning curve for a simple demo), Helm (standard for packaging K8s apps but overkill for this initial phase).

## Risks / Trade-offs

*   **[Risk] Unmanaged Database:** Backend uses SQLite which is not suitable for scalable, distributed Kubernetes environments → **Mitigation:** For production, integrate with a managed database service (e.g., Cloud SQL) or a persistent volume solution (e.g., GCE Persistent Disks) for stateful data.
*   **[Risk] Security Hardening:** Default GKE cluster and service account permissions may be overly permissive initially → **Mitigation:** Implement principle of least privilege, configure RBAC, network policies, and scanning for vulnerabilities in a dedicated security review phase.
*   **[Risk] Observability Gaps:** OpenTelemetry configuration is minimal, potentially leading to gaps in monitoring and tracing in a live GKE environment → **Mitigation:** Integrate with GCP Cloud Monitoring/Logging/Tracing or deploy a dedicated OpenTelemetry Collector within the cluster with appropriate configurations.
*   **[Trade-off] Manual Ingress Host Update:** `your-domain.com` needs manual update in `ingress.yaml` → **Mitigation:** For more dynamic environments, external-dns or a similar solution can automate DNS record management.

