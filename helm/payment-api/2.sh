for f in \
/tmp/card-processor-deploy.yaml \
/tmp/fraud-deploy.yaml \
/tmp/audit-deploy.yaml \
/tmp/mysql-sts.yaml
do
  echo "===== $f ====="
  grep -E 'image:|replicas:|containerPort:|claimName:|storageClassName:|storage:' "$f"
done


echo " Services=========== "

for f in \
/tmp/card-processor-svc.yaml \
/tmp/fraud-svc.yaml \
/tmp/audit-svc.yaml \
/tmp/mysql-svc.yaml \
/tmp/mysql-headless.yaml
do
  echo "===== $f ====="
  grep -E 'name:|type:|port:|targetPort:|clusterIP:' "$f"
done
