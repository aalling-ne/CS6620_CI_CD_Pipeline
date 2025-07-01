# CS6620_CI_CD_Pipeline Assignment - Part 2
Alexander Alling
CS6620
Summer 2025

# Description
This repo demonstrates how to use Dockerfiles and shell scripts to run a simple Flask REST API in a platform independant way. It also shows using Docker in a CI/CD workflow in GitHub Actions by automatically running the shell script.

# Included Files
**app.py** - The Flask application that serves as our simple REST API  
**test_app.py** - Pytest unit tests configured for use with Docker  
> note: the base url "http://flask-api:5000" is appropriate when app.py is running in a Docker Image named "flask-api". If you are not running app.py and test_app.py with the provided Dockerfiles, you'll need to connect to the localhost instead "http://localhost:5000".

**requirements.txt** - lists the required files for running and testing the app. Currently - flask, pytest, requests  
**Dockerfile** - creates a docker image that runs app.py  
**run.sh** - builds the primary Dockerfile. This script is not used in the GitHub Actions workflow, and is provided for running app.py in a Docker container outside of testing.  
**Dockerfile.test** - creates a docker image that runs test_app.py  
**test.sh** - Creates a Docker network, builds the Dockerfile, confirms the API's health, then builds Dockerfile.test and runs the Pytest unit tests.  

**/.github/workflows/python-app.yml** - workflow file using GitHub Actions to run test.sh, which creates the Docker containers and runs the app and tests. 


# Usage
This CI/CD workflow runs automatically any time a Push or a Pull-Request is made to the repo.  
The results of the testing can be seen on the GitHub website at the GitHub Action - "Python application" Workflow.  

The workflow can be triggered manually with the **Run Workflow** button.  

# Running the Code Locally  
Instructions for testing the project locally:  
**1 - Have Docker Installed**  

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
