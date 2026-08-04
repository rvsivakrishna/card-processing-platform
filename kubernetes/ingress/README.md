# NGINX Ingress

## Objective

Expose internal services through a single HTTP entry point.

## Components

- NGINX Ingress Controller
- Ingress Resource
- Host-based Routing

## Flow

Client
   │
   ▼
Ingress Controller
   │
   ▼
Ingress Resource
   │
   ▼
Payment API Service
   │
   ▼
Payment API Pods
