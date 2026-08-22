# Sprint 13 - AWS ALB Ingress

## Objective

Expose the Card Processing Platform running on Amazon EKS through an AWS Application Load Balancer using the AWS Load Balancer Controller.

## Architecture

Internet
→ AWS Application Load Balancer
→ Kubernetes ALB Ingress
→ payment-api-service
→ Payment API Pods
→ Fraud Service / Card Processor / Audit Service
→ MySQL
→ Amazon EBS

## AWS Load Balancer Controller

Implemented:

- IAM policy for AWS Load Balancer Controller
- IAM role using the existing EKS OIDC provider
- IRSA service account
- AWS Load Balancer Controller installed using Helm

The controller initially failed because it could not discover the VPC through instance metadata.

Fix:

- Passed AWS region explicitly
- Passed VPC ID explicitly through Helm

## ALB Ingress

Configured:

- ingressClassName: alb
- internet-facing scheme
- target-type: ip
- HTTP listener on port 80
- payment-api-service as backend

Removed legacy NGINX-specific ingress annotations.

## Validation

Validated:

- AWS Load Balancer Controller pods Running
- ALB successfully provisioned
- Ingress SuccessfullyReconciled
- TargetGroupBinding created
- Target type: ip
- Payment API pods registered directly as ALB targets
- External /payment endpoint reachable through ALB DNS

## End-to-End Transaction Validation

External transaction request flowed through:

ALB
→ Payment API
→ Fraud Service
→ Card Processor
→ Audit Service
→ MySQL

Validated transaction outcomes:

- APPROVED / LOW risk
- PENDING_VERIFICATION / MEDIUM risk
- DECLINED / HIGH risk

Audit history confirmed transactions were persisted in MySQL backed by Amazon EBS.

## Troubleshooting

### Controller CrashLoop

Error:

failed to get VPC ID from instance metadata

Fix:

Provided region and vpcId explicitly during Helm installation.

### Legacy NGINX Annotation

The EKS values inherited:

nginx.ingress.kubernetes.io/rewrite-target

Fix:

Removed the NGINX annotation and retained only ALB annotations.

## Interview Summary

The Card Processing Platform was exposed externally through an AWS-native Application Load Balancer. The AWS Load Balancer Controller used IRSA for AWS permissions, and ALB target type ip allowed direct registration of Kubernetes pod IPs. End-to-end payment processing and audit persistence were validated through the external ALB endpoint.