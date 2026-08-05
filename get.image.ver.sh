kubectl get deployment payment-api \
-n card-processing \
-o=jsonpath='{.spec.template.spec.containers[0].image}'
echo
