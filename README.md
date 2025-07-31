# CS6620_CI_CD_Pipeline Assignment - Part 3
Alexander Alling
CS6620
Summer 2025

# Description
This repo demonstrates how to use Docker Compose along with Dockerfiles and shell scripts to run a Flask REST API which stores data in an AWS S3 Bucket and DynamoDB Table (simulated using Localstack). The functionality of the REST API and AWS Storage is verified automatically with a CI/CD workflow in GitHub Actions.

# Included Files
**app.py** - The Flask application that serves as our simple REST API  
**test_app.py** - Pytest unit tests configured for use with Docker  
> note: the base url "http://flask-api:5000" is set automatically by an environment variable in docker-compose.test.yml. If you do not use the provided Compose files, no environment variables are set, and "http://localhost:5000" is used automatically instead.

**requirements.txt** - lists the required files for running and testing the app. Currently - flask, pytest, requests, boto3  
**Dockerfile** - creates a docker image that runs app.py  
**docker-compose.yml** - Docker Compose file that runs localstack and the REST API application (by using the Dockerfile).  
**run.sh** - runs docker-compose.yml. This script is not used in the GitHub Actions workflow, and is provided for running app.py and localstack in Docker containers outside of testing.  
**Dockerfile.test** - creates a docker image that runs test_app.py  
**docker-compose.test.yml** - Docker Compose file that runs localstack and the REST API application (by using the Dockerfile), then runs test_app.py (by using Dockerfile.test).  
**test.sh** - Creates a Docker network, builds the Dockerfile, confirms the API's health, then builds Dockerfile.test and runs the Pytest unit tests.  

**/.github/workflows/python-app.yml** - workflow file using GitHub Actions to run test.sh, which creates the Docker containers and runs the app and tests. 


# Usage
This CI/CD workflow runs automatically any time a Push or a Pull-Request is made to the repo.  
The results of the testing can be seen on the GitHub website at the GitHub Action - "Python application" Workflow.  

The workflow can be triggered manually with the **Run Workflow** button.  

# Running the Code Locally  
Instructions for testing the project locally:  
**1 - Have Docker Compose Installed**  

**2 - Clone the Repo**  

> git clone https://github.com/aalling-ne/CS6620_CI_CD_Pipeline/  
> cd CS6620_CI_CD_Pipeline
  
**3 - Give execution privledges to the test shell script**  

> chmod +x test.sh

**4 - Run the testing script**

> ./test.sh

**Extra - Run app.py in Docker container without running unit tests**

> chmod +x run.sh  
> ./run.sh

# Testing the API with curl  
The REST API can be tested with curl as follows:  
**1 - POST**  

> curl -X POST http://localhost:5000/api/items -H "Content-Type: application/json" -d '{"id": "1", "name": "Test Item"}'

Expected Status Code - 201

**2 - PUT**  

> curl -X PUT http://localhost:5000/api/items/1 -H "Content-Type: application/json" -d '{"id": "1", "favorite_color": "green"}'

Expected Status Code - 200

**3 - DELETE**

> curl -X DELETE http://localhost:5000/api/items/1

Expected Status Code - 204  

# Resources Utilized  

https://docs.docker.com/guides/localstack/  
https://docs.localstack.cloud/aws/services/s3/  
https://docs.localstack.cloud/aws/getting-started/installation/  
https://docs.localstack.cloud/aws/capabilities/config/credentials/  
https://ruan.dev/blog/2024/08/06/getting-started-with-localstack-overview-setup-and-practical-usage-guide  
https://last9.io/blog/docker-compose-health-checks/  
https://docs.python.org/3/library/json.html  

