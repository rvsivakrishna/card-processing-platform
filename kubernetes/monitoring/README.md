# Sprint 10 - Monitoring and Observability

## Objective

Introduce infrastructure and application observability for the Card Processing Platform using Prometheus and Grafana.

## Architecture

```text
Kubernetes Nodes
      |
      +---- Node Exporter
      |
Kubernetes Objects
      |
      +---- kube-state-metrics
      |
      v
   Prometheus
      |
      | PromQL
      v
    Grafana
      |
      v
Dashboards / Operational Visibility


Payment Requests
      |
      v
 Payment API
      |
      +---- /metrics
                |
                v
            Prometheus
                |
                v
             Grafana
