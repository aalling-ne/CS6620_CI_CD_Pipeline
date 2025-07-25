#!/bin/bash
set -e

docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from flask-api-test
