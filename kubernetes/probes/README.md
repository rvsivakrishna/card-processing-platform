# Platform Availability

## Objective

Improve application availability by using Kubernetes health probes.

## Implemented

- Startup Probe
- Readiness Probe
- Liveness Probe

## Validation

### Readiness
Pods removed from Service when unhealthy.

### Liveness
Pods automatically restarted.

### Startup
Prevents restarts during slow application initialization.
