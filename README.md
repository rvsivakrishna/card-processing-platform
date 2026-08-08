
                    Internet
                        │
                        ▼
               NGINX Ingress
                        │
                        ▼
                 Payment API
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    Card Processor              ConfigMap
          │                           │
          └─────────────┬─────────────┘
                        ▼
                     Secret

──────────────────────────────────────────

Deployment
Rolling Updates
HPA
RBAC
Resource Limits

# Sprint Roadmap

| Sprint | Topic | Status |
|---------|-------|--------|
| Sprint 1 | Basic Kubernetes Platform | ✅ |
| Sprint 2 | NGINX Ingress | ✅ |
| Sprint 3 | Health Probes | ✅ |
| Sprint 4 | Rolling Updates & Rollbacks | ✅ |
| Sprint 5 | Horizontal Pod Autoscaler (HPA) | ✅ |
| Sprint 6 | Kubernetes RBAC | ✅ |
| Sprint 7 | Network Policies | 🚧 |
| Sprint 8 | Persistent Storage | ⏳ |
| Sprint 9 | Monitoring (Prometheus & Grafana) | ⏳ |
| Sprint 10 | Helm Chart | ⏳ |

# card-processing-platform
Production-ready Kubernetes platform demonstrating enterprise deployment patterns for a card processing system.

## Sprint 1 - Basic Kubernetes Platform

### Features
- Kubernetes Namespace
- ConfigMaps
- Secrets
- Deployments
- ReplicaSets
- ClusterIP Services
- Internal Service Communication
- Resource Requests & Limits
- Production-style Folder Structure

### Microservices
- Payment API
- Card Processor

### Architecture

User
   │
   ▼
Payment API
   │
   ▼
Card Processor


## Sprint 2 – NGINX Ingress

### Features

- Installed NGINX Ingress Controller
- Host-based routing
- Payment API exposed through Ingress
- Kubernetes DNS-based service discovery
- Internal microservice communication

### Test

```bash
curl -H "Host: payment.bank.local" \
http://localhost:32047/payment
```

Expected response:

```json
{
  "payment":"received",
  "processor_response":{
      "authorization":"SUCCESS",
      "transaction":"APPROVED"
  }
}
```


## Completed Features

- ✅ Kubernetes Namespaces
- ✅ ConfigMaps
- ✅ Secrets
- ✅ Services
- ✅ Deployments
- ✅ NGINX Ingress
- ✅ Health Probes
- ✅ Rolling Updates
- ✅ Rollbacks

## Sprint 3 – Health Probes

### Features

- Liveness Probe
- Readiness Probe
- Startup validation
- Zero-downtime deployments

### Benefits

- Automatic recovery from unhealthy containers
- Prevents traffic to unready Pods
- Improves application availability

  ## Sprint 4 – Rolling Updates & Rollbacks

### Features

- Rolling Update strategy
- Zero downtime deployment
- Deployment history
- Rollback to previous revision

### Commands

kubectl rollout history deployment payment-api

kubectl rollout undo deployment payment-api

## Sprint 5 – Horizontal Pod Autoscaler

### Features

- Metrics Server
- CPU-based Autoscaling
- Resource Requests & Limits
- Load Testing

### Result

- Scaled from 2 replicas to 3 replicas under load
- Automatically scaled back to 2 replicas after load decreased

# Sprint 6 - Kubernetes RBAC

## Objective

Implement Role Based Access Control (RBAC) for the Card Processing Platform following the Principle of Least Privilege.

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

## Roles

### developer-role

Namespace scoped permissions for application developers.

Allowed

- View Pods
- View Logs
- Create Deployments
- Update Deployments

Restricted

- Delete Deployments
- Delete Namespace
- View Nodes

---

### devops-cluster-role

Cluster-wide operational permissions.

Allowed

- View Pods
- View Services
- View Ingress
- View ConfigMaps
- View HPA
- Update Deployments

Restricted

- Delete Nodes
- Delete Namespace
- Modify RBAC

---

### auditor-cluster-role

Read-only cluster visibility.

Allowed

- View Nodes
- View Namespaces
- View PersistentVolumes

Restricted

- Modify Cluster Resources

---

## Validation

Permissions verified using:

kubectl auth can-i

## Sprint 7 Implementation

Implemented Fraud Detection microservice and Kubernetes network security.

### Application Changes

- Added Fraud Service application
- Integrated Payment API with Fraud Service
- Added fraud risk evaluation workflow

### Kubernetes Changes

Added:
- Fraud Deployment
- Fraud Service
- Default deny network policy
- Payment to Fraud communication policy
- Payment to Card Processor communication policy
- Ingress protection policy

### Security Improvements

- Microservice isolation
- Zero trust network approach
- Restricted pod-to-pod communication
- Explicit service communication rules

### Testing

Verified:
- Payment transaction workflow
- Fraud decision response
- NetworkPolicy enforcement

## Sprint 8 – Audit Service with Persistent Storage

### Features

- Audit Service microservice
- Internal ClusterIP communication
- Persistent Volume (PV)
- Persistent Volume Claim (PVC)
- Transaction audit logging
- Payment → Audit integration
- Persistent audit history across pod restarts

### Flow

Internet
   │
   ▼
NGINX Ingress
   │
   ▼
Payment API
   ├──► Fraud Service
   ├──► Card Processor
   └──► Audit Service
               │
               ▼
         Persistent Volume

## Sprint 9 — Audit Service: MySQL Persistence & Kubernetes Secrets

Sprint 9 replaces the file-based `audit.log` approach with persistent MySQL-backed audit storage.

### Architecture

```text
Payment / Application Event
          |
          v
    Audit Service :8082
          |
          | MySQL credentials
          | injected from Kubernetes Secret
          v
    mysql-service :3306
          |
          v
       auditdb
          |
          v
     transactions
```

### Implemented

* Replaced file-based audit persistence with MySQL.
* Added `Audit Service` endpoints:

  * `GET /health`
  * `POST /audit`
  * `GET /history`
* Added MySQL StatefulSet and Services.
* Added MySQL persistent storage.
* Added Kubernetes Secret for database credentials.
* Injected `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` using `secretKeyRef`.
* Configured Audit Service to connect through `mysql-service`.
* Deployed the Audit Service using an immutable SHA256 image digest.
* Verified the container runs as the non-root `audituser`.
* Scanned the container image with Trivy.
* Signed and verified the image using Cosign.
* Verified audit data survives Audit Service pod recreation.

### Validation

A test transaction was submitted:

```text
Transaction: TXN-SPRINT9-001
Status: SUCCESS
Risk: LOW
Amount: 1500.75
```

`POST /audit` returned:

```json
{
  "message": "Audit record stored",
  "transaction": "TXN-SPRINT9-001"
}
```

`GET /history` subsequently returned the persisted transaction from MySQL.

The Audit Service pod was then recreated and the same transaction remained available, confirming that audit records are persisted independently of the application pod.

### Security

Database credentials are not hard-coded into the application image or Deployment manifest. Kubernetes `Secret` references are used to inject the required database credentials into the Audit Service.

The container image is:

* Trivy scanned
* Signed with Cosign
* Verified against its immutable SHA256 digest
* Running as a non-root user
