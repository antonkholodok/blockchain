#!/bin/bash

curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"sender": "address-a", "recipient": "address-b", "amount": 5}' \
    http://127.0.0.1:5000/transactions/new