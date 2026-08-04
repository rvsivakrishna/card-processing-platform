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
