#!/bin/bash

NS=card-processing

echo "===== Developer ====="
kubectl auth can-i --as=system:serviceaccount:$NS:developer-sa get pods -n $NS
kubectl auth can-i --as=system:serviceaccount:$NS:developer-sa delete deployment -n $NS

echo
echo "===== DevOps ====="
kubectl auth can-i --as=system:serviceaccount:$NS:devops-sa get ingresses -n $NS
kubectl auth can-i --as=system:serviceaccount:$NS:devops-sa get horizontalpodautoscalers.autoscaling -n $NS
kubectl auth can-i --as=system:serviceaccount:$NS:devops-sa delete namespace

echo
echo "===== Auditor ====="
kubectl auth can-i --as=system:serviceaccount:$NS:auditor-sa get nodes
kubectl auth can-i --as=system:serviceaccount:$NS:auditor-sa delete node

echo
echo "===== Jenkins ====="
kubectl auth can-i --as=system:serviceaccount:$NS:jenkins-sa update deployment -n $NS
kubectl auth can-i --as=system:serviceaccount:$NS:jenkins-sa delete deployment -n $NS
