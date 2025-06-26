#!/bin/bash
docker build -f Dockerfile.test -t flask-api-test .
docker run --rm flask-api-test
