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
