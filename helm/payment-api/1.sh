kubectl get deployment card-processor -n card-processing -o yaml > /tmp/card-processor-deploy.yaml
kubectl get svc card-processor-service -n card-processing -o yaml > /tmp/card-processor-svc.yaml

kubectl get deployment fraud-service -n card-processing -o yaml > /tmp/fraud-deploy.yaml
kubectl get svc fraud-service -n card-processing -o yaml > /tmp/fraud-svc.yaml

kubectl get deployment audit-service -n card-processing -o yaml > /tmp/audit-deploy.yaml
kubectl get svc audit-service -n card-processing -o yaml > /tmp/audit-svc.yaml

kubectl get statefulset mysql -n card-processing -o yaml > /tmp/mysql-sts.yaml
kubectl get svc mysql-service -n card-processing -o yaml > /tmp/mysql-svc.yaml
kubectl get svc mysql-headless -n card-processing -o yaml > /tmp/mysql-headless.yaml
