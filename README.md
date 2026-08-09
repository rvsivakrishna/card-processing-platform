# Card Processing Platform
 
Production-style Kubernetes platform for a card payment processing system, demonstrating containerized microservices, secure service communication, persistent audit storage, Helm-based deployment, container security, autoscaling, and observability.
 
---
 
## Architecture
 
```text
                          Internet / User
                                |
                                v
                         NGINX Ingress
                                |
                                v
                         Payment API
                  /-------------|-------------\
                 /              |              \
                v               v               v
        Fraud Service     Card Processor    Audit Service
                                                   |
                                                   v
                                             MySQL Service
                                                   |
                                                   v
                                            MySQL StatefulSet
                                                   |
                                                   v
                                                 PVC/PV
```
 
## Platform Capabilities
 
### Application
 
- Payment API
- Card Processor
- Fraud Service
- Audit Service
- MySQL
 
### Kubernetes
 
- Namespace
- Deployments
- ReplicaSets
- Services
- Ingress
- ConfigMaps
- Secrets
- Health Probes
- HPA
- RBAC
- NetworkPolicies
- Persistent Storage
- StatefulSets
- Jobs
 
### Security
 
- Non-root containers
- Trivy vulnerability scanning
- Cosign image signing
- Immutable image digest
- Kubernetes Secrets
- Zero-trust NetworkPolicies
 
### Deployment
 
- Rolling Updates
- Rollbacks
- Helm
- Versioned Helm packages
- Helm repository
 
### Observability
 
- Metrics Server
- Prometheus
- Node Exporter
- kube-state-metrics
- Grafana
- Payment API `/metrics`
- PromQL
 
---
 
# Sprint Roadmap
 
| Sprint | Topic | Status |
|---|---|---|
| Sprint 1 | Basic Kubernetes Platform | Completed |
| Sprint 2 | NGINX Ingress | Completed |
| Sprint 3 | Health Probes | Completed |
| Sprint 4 | Rolling Updates & Rollbacks | Completed |
| Sprint 5 | Horizontal Pod Autoscaler | Completed |
| Sprint 6 | Kubernetes RBAC | Completed |
| Sprint 7 | Network Policies & Fraud Detection | Completed |
| Sprint 8 | Audit Service & Persistent Storage | Completed |
| Sprint 9 | MySQL Persistence, Secrets & Container Security | Completed |
| Sprint 10 | Production Deployment with Helm | Completed |
| Sprint 11 | Monitoring & Observability | Completed |
| Sprint 12 | Canary / Blue-Green Deployment | Planned |
| Sprint 13 | CI/CD Automation | Planned |
| Sprint 14 | AWS / EKS Production Deployment | Planned |
| Sprint 15 | Final Architecture & Interview Documentation | Planned |
 
---
 
# Sprint 1 – Basic Kubernetes Platform
 
## Objective
 
Deploy the initial Card Processing Platform on Kubernetes using production-style Kubernetes objects and internal service communication.
 
## Implemented
 
- Kubernetes Namespace
- ConfigMaps
- Secrets
- Deployments
- ReplicaSets
- ClusterIP Services
- Internal Kubernetes DNS
- Resource Requests
- Resource Limits
- Production-style repository structure
 
## Initial Microservices
 
- Payment API
- Card Processor
 
## Architecture
 
```text
User
 |
 v
Payment API
 |
 v
Card Processor
```
 
## Validation
 
The Payment API successfully communicated with the Card Processor using Kubernetes service discovery.
 
---
 
# Sprint 2 – NGINX Ingress
 
## Objective
 
Expose the Payment API through an NGINX Ingress Controller using host-based routing.
 
## Implemented
 
- NGINX Ingress Controller
- Host-based routing
- Payment API Ingress
- Kubernetes DNS service discovery
- Internal service communication
 
## Request Flow
 
```text
Client
   |
   v
NGINX Ingress
   |
   v
payment-api-service
   |
   v
Payment API
```
 
## Test
 
```bash
curl -H "Host: payment.bank.local" \
http://localhost:32047/payment
```
 
Example response:
 
```json
{
  "payment": "received",
  "processor_response": {
    "authorization": "SUCCESS",
    "transaction": "APPROVED"
  }
}
```
 
---
 
# Sprint 3 – Health Probes
 
## Objective
 
Improve application availability and automatic recovery.
 
## Implemented
 
- Startup Probe
- Liveness Probe
- Readiness Probe
 
## Benefits
 
- Prevents traffic from reaching unready Pods
- Detects failed application processes
- Automatically restarts unhealthy containers
- Supports safer rolling deployments
 
## Flow
 
```text
Pod Starts
   |
   v
Startup Probe
   |
   v
Readiness Probe
   |
   v
Service Traffic
   |
   v
Liveness Probe continuously checks health
```
 
---
 
# Sprint 4 – Rolling Updates & Rollbacks
 
## Objective
 
Implement zero-downtime deployment and rollback capability.
 
## Implemented
 
- RollingUpdate deployment strategy
- Controlled replacement of Pods
- Deployment revision history
- Rollback testing
 
## Commands
 
```bash
kubectl rollout history deployment/payment-api \
  -n card-processing
 
kubectl rollout status deployment/payment-api \
  -n card-processing
 
kubectl rollout undo deployment/payment-api \
  -n card-processing
```
 
## Outcome
 
New application versions could be rolled out without replacing every Pod simultaneously, and previous revisions could be restored when required.
 
---
 
# Sprint 5 – Horizontal Pod Autoscaler
 
## Objective
 
Automatically scale Payment API replicas according to CPU utilization.
 
## Implemented
 
- Metrics Server
- CPU-based HPA
- Resource Requests
- Resource Limits
- Load testing
 
## Result
 
```text
Normal Load
    |
    v
2 Payment API Pods
    |
CPU increases
    |
    v
HPA
    |
    v
3 Payment API Pods
```
 
When load decreased, the replica count automatically returned to the configured minimum.
 
## Validation
 
```bash
kubectl get hpa -n card-processing
kubectl top pods -n card-processing
```
 
---
 
# Sprint 6 – Kubernetes RBAC
 
## Objective
 
Implement Role Based Access Control following the Principle of Least Privilege.
 
## Components
 
- ServiceAccount
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding
 
## Service Accounts
 
- developer-sa
- devops-sa
- auditor-sa
 
## Developer Role
 
Allowed:
 
- View Pods
- View Logs
- Create Deployments
- Update Deployments
 
Restricted:
 
- Delete Namespace
- Delete cluster resources
- View/modify Nodes
 
## DevOps ClusterRole
 
Allowed:
 
- View Pods
- View Services
- View Ingress
- View ConfigMaps
- View HPA
- Update Deployments
 
Restricted:
 
- Delete Nodes
- Delete Namespace
- Modify RBAC
 
## Auditor ClusterRole
 
Allowed:
 
- View Nodes
- View Namespaces
- View PersistentVolumes
 
Restricted:
 
- Modify cluster resources
 
## Validation
 
```bash
kubectl auth can-i
```
 
---
 
# Sprint 7 – Fraud Detection & Network Security
 
## Objective
 
Introduce Fraud Detection and implement zero-trust service communication using Kubernetes NetworkPolicies.
 
## Application Changes
 
Added:
 
- Fraud Service
- Payment API → Fraud Service integration
- Fraud risk evaluation
- Payment decision workflow
 
## Fraud Decisions
 
```text
LOW
 |
 v
CLEAR
 |
 v
Card Processing
 |
 v
APPROVED
 
MEDIUM
 |
 v
REVIEW
 |
 v
Additional Verification / OTP
 |
 v
PENDING_VERIFICATION
 
HIGH
 |
 v
BLOCK
 |
 v
DECLINED
```
 
## NetworkPolicies
 
Implemented:
 
- Default deny
- Ingress → Payment API
- Payment API → Card Processor
- Payment API → Fraud Service
- Payment API → Audit Service
- Audit Service / DB Init → MySQL
 
## Security Model
 
```text
Default Deny
    |
    +---- Explicit allow: Ingress → Payment API
    |
    +---- Explicit allow: Payment API → Fraud
    |
    +---- Explicit allow: Payment API → Card Processor
    |
    +---- Explicit allow: Payment API → Audit
    |
    +---- Explicit allow: Audit / DB Init → MySQL
```
 
## Validation
 
Verified:
 
- Payment transaction workflow
- Fraud decision response
- NetworkPolicy enforcement
- Unauthorized communication blocking
 
## Key Learning
 
Kubernetes Service existence alone does not mean communication is permitted when default-deny NetworkPolicies are enabled.
 
---
 
# Sprint 8 – Audit Service & Persistent Storage
 
## Objective
 
Introduce transaction auditing and persist audit records independently of the application Pod lifecycle.
 
## Implemented
 
- Audit Service microservice
- ClusterIP Service
- Payment → Audit integration
- PersistentVolume
- PersistentVolumeClaim
- Transaction audit history
 
## Architecture
 
```text
Internet
   |
   v
NGINX Ingress
   |
   v
Payment API
   |
   +----> Fraud Service
   |
   +----> Card Processor
   |
   +----> Audit Service
                |
                v
          Persistent Storage
```
 
## Validation
 
Audit records remained available after Audit Service Pod recreation.
 
---
 
# Sprint 9 – MySQL Persistence, Secrets & Container Security
 
## Objective
 
Replace file-based audit storage with persistent MySQL-backed audit storage and strengthen container security.
 
## Architecture
 
```text
Payment Event
     |
     v
Audit Service :8082
     |
     | Credentials from Kubernetes Secret
     v
mysql-service :3306
     |
     v
MySQL StatefulSet
     |
     v
auditdb
     |
     v
transactions table
     |
     v
PersistentVolume
```
 
## Audit Service Endpoints
 
- `GET /health`
- `POST /audit`
- `GET /history`
 
## Implemented
 
- MySQL StatefulSet
- MySQL ClusterIP Service
- MySQL Headless Service
- Persistent storage
- Database initialization Job
- Kubernetes Secret
- Environment injection using `secretKeyRef`
- Audit Service → MySQL integration
- Non-root container execution
- Immutable SHA256 image deployment
 
## Test Transaction
 
```text
Transaction: TXN-SPRINT9-001
Status: SUCCESS
Risk: LOW
Amount: 1500.75
```
 
Example response:
 
```json
{
  "message": "Audit record stored",
  "transaction": "TXN-SPRINT9-001"
}
```
 
The transaction remained available through `/history` after Pod recreation.
 
## Container Security
 
The Audit Service image was:
 
- Built using a hardened Dockerfile
- Executed as a non-root user
- Scanned using Trivy
- Signed using Cosign
- Verified using the Cosign public key
- Deployed using an immutable SHA256 digest
 
## Security Principle
 
Database credentials were not hard-coded into:
 
- Source code
- Container image
- Kubernetes Deployment
 
Credentials were injected through Kubernetes Secrets.
 
---
 
# Sprint 10 – Production Deployment with Helm
 
## Objective
 
Convert individually managed Kubernetes manifests into a reusable and version-controlled Helm deployment model.
 
## Implemented
 
The Helm chart was expanded to deploy platform components including:
 
- Payment API
- Card Processor
- Fraud Service
- Audit Service
- MySQL StatefulSet
- MySQL Services
- ConfigMap
- PersistentVolumeClaim
- Database initialization Job
- Ingress
- HPA
- NetworkPolicies
- Resource Requests & Limits
- Health Probes
 
## Helm Structure
 
```text
helm/payment-api/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── networkpolicy.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── configmap.yaml
    ├── audit-deployment.yaml
    ├── fraud-deployment.yaml
    ├── card-processor-deployment.yaml
    ├── mysql-statefulset.yaml
    ├── mysql-services.yaml
    ├── mysql-init-configmap.yaml
    ├── db-init-job.yaml
    └── ...
```
 
## Helm Release Flow
 
```text
Application Configuration
          |
          v
      values.yaml
          |
          v
    Helm Templates
          |
          v
      helm lint
          |
          v
    helm template
          |
          v
     helm package
          |
          v
Versioned Helm Package
          |
          v
helm upgrade --install
          |
          v
Kubernetes Platform
```
 
## Validation
 
```bash
helm lint .
```
 
Result:
 
```text
1 chart(s) linted, 0 chart(s) failed
```
 
Rendered resources included:
 
```text
NetworkPolicy
ConfigMap
PersistentVolumeClaim
Service
Deployment
HorizontalPodAutoscaler
StatefulSet
Job
Ingress
```
 
## Helm Upgrade & Rollback
 
```bash
helm history payment-api -n card-processing
```
 
Example:
 
```text
REVISION   STATUS
1          superseded
2          superseded
3          deployed
```
 
Rollback was tested successfully.
 
## Helm Repository
 
Versioned chart artifacts:
 
```text
helm-repo/
├── index.yaml
├── card-processing-platform-1.0.0.tgz
└── card-processing-platform-1.0.1.tgz
```
 
Example consumer flow:
 
```bash
helm repo add card-processing <helm-repository-url>
helm repo update
helm search repo card-processing
helm pull card-processing/card-processing-platform
```
 
## Troubleshooting – Helm Ownership Conflict
 
### Symptom
 
```text
invalid ownership metadata
missing app.kubernetes.io/managed-by
missing meta.helm.sh/release-name
missing meta.helm.sh/release-namespace
```
 
### Root Cause
 
Resources already existed because they had previously been deployed using `kubectl`.
 
Helm therefore could not automatically assume ownership.
 
### Key Learning
 
When migrating existing Kubernetes objects to Helm, resource ownership and migration strategy must be explicitly planned.
 
---
 
# Sprint 11 – Monitoring & Observability
 
## Objective
 
Introduce infrastructure-level and application-level observability using Prometheus and Grafana.
 
## Monitoring Stack
 
Implemented:
 
- Prometheus Server
- Node Exporter
- kube-state-metrics
- Grafana
- Kubernetes infrastructure metrics
- Prometheus target validation
- Grafana Prometheus data source
- Payment API instrumentation
- `/metrics` endpoint
- PromQL validation
 
## Architecture
 
```text
Node Exporter -----------\
                          \
kube-state-metrics --------> Prometheus --------> Grafana
                          /
Payment API /metrics ----/
```
 
## Infrastructure Metrics
 
Prometheus collects metrics for:
 
- Node CPU
- Node memory
- Kubernetes Pod state
- Container restart information
- Kubernetes API
- cAdvisor
- CoreDNS
- Prometheus itself
 
## Prometheus Target Validation
 
Target availability was validated using:
 
```promql
up
```
 
Meaning:
 
```text
up = 1
Target successfully scraped
 
up = 0
Target unavailable
```
 
Healthy targets validated included:
 
- Kubernetes API Server
- k8s-master Node Exporter
- k8s-worker Node Exporter
- CoreDNS
- kube-state-metrics
- cAdvisor
- Prometheus
 
## Grafana
 
Grafana was configured with Prometheus as its data source.
 
Internal Kubernetes Prometheus URL:
 
```text
http://prometheus-server.monitoring.svc.cluster.local
```
 
Grafana → Prometheus connectivity was successfully validated.
 
## Payment API Instrumentation
 
The Payment API was instrumented using the Python Prometheus client.
 
Metrics endpoint:
 
```text
/metrics
```
 
Custom metrics:
 
```text
payment_requests_total
payment_status_total
payment_risk_total
payment_errors_total
payment_request_duration_seconds
```
 
## Business Observability
 
Metrics provide visibility into:
 
- Total payment traffic
- Approved transactions
- Declined transactions
- Pending verification
- LOW fraud risk
- MEDIUM fraud risk
- HIGH fraud risk
- Dependency errors
- Application errors
- Payment processing latency
 
## Fraud Test Results
 
### LOW Risk
 
```json
{
  "status": "APPROVED",
  "fraud": {
    "decision": "CLEAR",
    "risk": "LOW"
  }
}
```
 
### MEDIUM Risk
 
```json
{
  "status": "PENDING_VERIFICATION",
  "otp_required": true,
  "fraud": {
    "decision": "REVIEW",
    "risk": "MEDIUM"
  }
}
```
 
### HIGH Risk
 
```json
{
  "status": "DECLINED",
  "reason": "Fraud detected",
  "fraud": {
    "decision": "BLOCK",
    "risk": "HIGH"
  }
}
```
 
## Payment Load Test
 
```bash
for i in {1..10}; do
  curl -s \
    -H "Host: payment.bank.local" \
    http://localhost:32047/payment
  echo
  sleep 1
done
```
 
## Prometheus Metric Validation
 
Payment API `/metrics` exposed metrics including:
 
```text
payment_requests_total
payment_request_duration_seconds_bucket
payment_request_duration_seconds_count
payment_request_duration_seconds_sum
```
 
## Network Security Consideration
 
The `card-processing` namespace uses default-deny NetworkPolicies.
 
Prometheus runs in the `monitoring` namespace.
 
Monitoring traffic therefore requires explicitly permitted communication:
 
```text
monitoring namespace
        |
        | TCP 8080
        | /metrics
        v
Payment API
card-processing namespace
```
 
Monitoring traffic must follow the same zero-trust security model as normal application traffic.
 
---
 
# Capacity Planning & Reliability Finding
 
## Scenario
 
During the observability rollout, additional monitoring workloads exposed insufficient cluster capacity headroom.
 
## Symptoms
 
Observed symptoms included:
 
- Kubernetes API latency
- TLS handshake timeouts
- etcd request timeouts
- kubelet communication delays
- failed health probes
- Pod restarts
- Metrics API unavailability
- delayed Helm operations
- unstable monitoring components
 
## Investigation
 
Because multiple unrelated platform components were affected simultaneously, the investigation moved from individual application troubleshooting toward infrastructure capacity analysis.
 
Reviewed areas included:
 
- Kubernetes control-plane components
- Worker workloads
- Application replicas
- MySQL
- Monitoring workloads
- Kubernetes system Pods
- Requests and limits
- Available capacity
 
## Root Cause
 
The observability rollout exposed insufficient capacity headroom for the combined application, database, Kubernetes platform, and monitoring workloads.
 
## Immediate Mitigation
 
- Reduced nonessential replica counts
- Prioritized critical workloads
- Reduced monitoring footprint
- Avoided additional workload expansion
- Stabilized the Kubernetes control plane before continuing
 
## Engineering Decision
 
The issue was not hidden by continuously increasing:
 
- Probe timeouts
- Helm timeouts
- API timeouts
 
Instead, it was treated as a capacity-planning and infrastructure-sizing issue.
 
## Production Recommendation
 
Capacity planning must account for:
 
```text
Operating System
      +
Container Runtime
      +
Kubernetes Components
      +
CNI
      +
Ingress
      +
Application Pods
      +
Databases
      +
Monitoring
      +
Logging
      +
Rolling Deployment Headroom
      +
Autoscaling Headroom
      +
Failure Recovery Capacity
```
 
Production architecture should implement:
 
- Right-sized nodes
- CPU/memory requests
- CPU/memory limits
- Operational capacity headroom
- HPA
- Node autoscaling
- Workload distribution
- Multi-node / multi-AZ resilience
- Monitoring capacity included in sizing
 
## Key SRE Learning
 
The observability rollout did not create the underlying capacity problem.
 
It exposed an existing lack of capacity headroom.
 
This distinction is important when troubleshooting production infrastructure.
 
---
 
# Major Troubleshooting Scenarios
 
## NGINX 504 Gateway Timeout
 
### Symptom
 
```text
HTTP/1.1 504 Gateway Time-out
```
 
### Investigation
 
Checked:
 
- Ingress
- Service selector
- Service endpoints
- Pod labels
- NetworkPolicies
- Downstream communication
 
### Root Cause
 
During Helm migration, Payment API labels changed while existing NetworkPolicies still referenced older labels.
 
### Resolution
 
Aligned Pod labels and NetworkPolicy selectors.
 
---
 
## Helm Ownership Conflict
 
### Symptom
 
```text
invalid ownership metadata
```
 
### Root Cause
 
Resources existed before the Helm release.
 
### Lesson
 
Define resource ownership and migration strategy before moving manually managed Kubernetes resources into Helm.
 
---
 
## ImagePullBackOff
 
### Investigation
 
Validated:
 
- Local Docker image
- Repository name
- Image tag
- Registry push
- Deployment image reference
 
### Resolution
 
Published the required image version to the registry and restarted the rollout.
 
---
 
## NetworkPolicy Timeouts
 
### Root Cause
 
Default-deny policies blocked communication that had not been explicitly permitted.
 
### Lesson
 
Application traffic and monitoring traffic must both be considered in NetworkPolicy design.
 
---
 
## Persistence Validation
 
Audit records were verified before and after Pod recreation.
 
Records remained available because transaction storage was moved to MySQL with persistent storage.
 
---
 
## Monitoring Capacity Incident
 
Cluster-wide symptoms were traced to insufficient capacity headroom rather than an individual application defect.
 
Long-term remediation is infrastructure right-sizing and autoscaling rather than increasing timeout values.
 
---
 
# End-to-End Payment Flow
 
```text
User
 |
 v
NGINX Ingress
 |
 v
Payment API
 |
 +------------------> Fraud Service
 |                         |
 |                         v
 |                 LOW / MEDIUM / HIGH
 |
 +------------------> Card Processor
 |
 +------------------> Audit Service
                          |
                          v
                     MySQL Service
                          |
                          v
                     MySQL StatefulSet
                          |
                          v
                        PVC/PV
```
 
---
 
# Security Flow
 
```text
Source Code
    |
    v
Docker Build
    |
    v
Minimal / Non-root Image
    |
    v
Trivy Scan
    |
    v
Container Registry
    |
    v
Cosign Signature
    |
    v
Immutable Image Digest
    |
    v
Kubernetes Deployment
```
 
---
 
# Deployment Flow
 
```text
Developer
   |
   v
Git
   |
   v
Application / Kubernetes Changes
   |
   v
Helm Chart
   |
   v
helm lint
   |
   v
helm template
   |
   v
helm package
   |
   v
Helm Repository
   |
   v
helm upgrade --install
   |
   v
Kubernetes
```
 
---
 
# Observability Flow
 
```text
Application / Kubernetes
         |
         +------ Node Exporter
         |
         +------ kube-state-metrics
         |
         +------ Payment API /metrics
         |
         v
      Prometheus
         |
         | PromQL
         v
       Grafana
         |
         v
Operational Visibility
```
 
---
 
# Key DevOps / SRE Concepts Demonstrated
 
- Kubernetes workload deployment
- Kubernetes service discovery
- Ingress routing
- Health checking
- Rolling deployments
- Rollbacks
- Horizontal autoscaling
- RBAC
- Principle of Least Privilege
- Zero-trust networking
- Stateful applications
- Persistent storage
- Secrets management
- Container hardening
- Vulnerability scanning
- Artifact signing
- Immutable deployments
- Helm packaging
- Helm release management
- Release versioning
- Prometheus
- Grafana
- Application instrumentation
- PromQL
- Capacity planning
- Production troubleshooting
- Reliability engineering decisions
 
---
 
# Upcoming Sprints
 
## Sprint 12 – Canary / Blue-Green Deployment
 
Implement controlled production traffic migration and safer release strategies.
 
## Sprint 13 – CI/CD Automation
 
Planned pipeline:
 
```text
Git Push
   |
   v
Build
   |
   v
Test
   |
   v
Trivy Scan
   |
   v
Push Image
   |
   v
Cosign Sign
   |
   v
Helm Package
   |
   v
Deploy
```
 
## Sprint 14 – AWS / EKS Production Deployment
 
Target architecture:
 
- Amazon EKS
- AWS Load Balancer
- Production worker-node sizing
- Autoscaling
- Cloud networking
- Persistent storage
- Production observability
 
## Sprint 15 – Final Architecture & Interview Documentation
 
Prepare:
 
- Architecture documentation
- Troubleshooting stories
- Production decision explanations
- DevOps/SRE interview questions
- Short and deep-dive project explanations
 
---
 
# Project Outcome
 
The Card Processing Platform evolved from a basic two-service Kubernetes deployment into a production-style platform implementing:
 
```text
Microservices
     +
Ingress
     +
Health Management
     +
Autoscaling
     +
RBAC
     +
Network Security
     +
Persistent Database
     +
Container Security
     +
Helm Release Management
     +
Observability
     +
Capacity Planning
```
 
The project captures both successful implementation and operational troubleshooting, including the engineering decisions required to improve reliability, security, scalability, and production readiness.
