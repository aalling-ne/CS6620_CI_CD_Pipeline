#!/bin/bash

set -e

#create network
docker network create flask-test-net || true

# build Dockerfile for app.py
docker build -t flask-api .

# run Dockerfile
docker run -d --rm --name flask-api --network flask-test-net -p 5000:5000 flask-api

# wait for API to be up
for i in {1..30}; do
  if curl -s http://localhost:5000/health >/dev/null; then
    echo "API is up!"
    break
  fi
  echo "Retrying in 1s..."
  sleep 1
done

# build Dockerfile.test for test_app.py
docker build -f Dockerfile.test -t flask-api-test .

# run test Dockerfile
docker run --rm --network flask-test-net flask-api-test

#cleanup
docker stop flask-api || true
docker network rm flask-test-net || true
