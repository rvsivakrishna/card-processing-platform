for p in \
default-deny \
allow-payment-to-cardprocessor \
allow-payment-to-fraud \
allow-payment-to-audit \
allow-db-access
do
  echo "===== $p ====="
  kubectl get networkpolicy "$p" \
    -n card-processing \
    -o yaml
done
