# Sprint 12 - AWS EKS Platform Migration

## Objective

Migrate the Card Processing Platform from the local Kubernetes environment to AWS EKS using Terraform and Helm.

## Infrastructure

- Terraform remote state in Amazon S3
- State locking enabled
- Multi-AZ VPC
- 2 public subnets
- 2 private subnets
- Internet Gateway
- NAT Gateway
- Public and private route tables
- EKS Kubernetes 1.34
- Managed node group using t3.small instances
- Worker nodes deployed in private subnets
- Restricted EKS public API endpoint
- IAM roles for EKS cluster and worker nodes

## EBS CSI Integration

PersistentVolumeClaims initially remained Pending because the EBS CSI provisioner was unavailable.

Implemented:

- EKS OIDC provider
- IAM role for EBS CSI
- AmazonEBSCSIDriverPolicyV2
- aws-ebs-csi-driver EKS add-on

Validated:

- EBS CSI controller pods Running
- EBS CSI node pods Running
- MySQL PVC Bound
- Audit Service PVC Bound

## Helm Migration

Existing Card Processing Helm chart was adapted for EKS.

Changes:

- Added values-eks.yaml
- Changed local-path storage to AWS EBS-backed storage
- Temporarily disabled Ingress
- Temporarily disabled NetworkPolicy
- Kubernetes Secrets created outside Git
- Fixed Audit Service PVC claim reference
- Fixed Payment API Service selector

## Application Components

Deployed:

- payment-api
- card-processor
- fraud-service
- audit-service
- MySQL StatefulSet
- MySQL database initialization Job
- HorizontalPodAutoscaler

## Troubleshooting

### PVC Pending

Problem:

PVCs stayed in Pending state.

Root cause:

EBS CSI provisioner was not installed.

Fix:

Installed the Amazon EBS CSI driver using Terraform, OIDC and IAM.

### Payment API Service Had No Endpoints

Problem:

payment-api-service had no endpoints and port-forward timed out.

Root cause:

Service selector did not match Payment API pod labels.

Fix:

Aligned the Helm Service selector with the Deployment labels.

### Audit Database Schema Failure

Problem:

Audit API returned HTTP 500.

Error:

Table 'carddb.transactions' doesn't exist.

Root cause:

Database initialization Job created the transactions table in auditdb while the application used carddb.

Fix:

Updated the MySQL initialization ConfigMap to create and use carddb.

## Validation

Validated:

- EKS worker nodes Ready
- kube-system components Running
- EBS CSI components Running
- All Card Processing pods Running
- MySQL initialization Job Completed
- Payment API health endpoint working
- Payment transaction flow working
- Fraud Service returned business decision
- Audit Service health working
- Audit transaction stored successfully
- Audit history retrieved successfully
- Audit Service pod restarted
- Audit record remained available after restart

## Persistence Flow

Audit Service
→ MySQL Service
→ MySQL StatefulSet
→ PVC
→ AWS EBS CSI Driver
→ Amazon EBS

Persistence was verified after restarting the Audit Service pod.

## Deferred to Sprint 13

- AWS Load Balancer Controller
- ALB Ingress
- External application access
- EKS NetworkPolicy enablement
- Monitoring and observability integration