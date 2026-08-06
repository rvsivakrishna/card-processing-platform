#!/bin/bash

URL="http://localhost:32047/payment"
HOST="payment.bank.local"

echo "Starting load test with 30 workers..."

for i in {1..30}
do
(
    while true
    do
        curl -s \
          -H "Host: ${HOST}" \
          ${URL} >/dev/null
    done
) &
done

echo "Load test running..."
echo "Press Ctrl+C to stop."

wait
