# CS6620_CI_CD_Pipeline Assignment
Alexander Alling
CS6620
Summer 2025

# Description
This repo demonstrates a basic CI/CD workflow by automatically running pytest unit-testing when a push or pull-request is made.

# Usage
This CI/CD workflow runs automatically any time a Push or a Pull-Request is made to the repo.  
The results of the testing can be seen on the GitHub website at the GitHub Action - "Python application" Workflow.  

The workflow can be triggered manually with the Run Workflow button.  

# Files for Workflow
requirements.txt - list the installation requirments for the workflow (in this case, pytest)  
/.github/workflows/python-app.yml - workflow file using GitHub Actions to create a virtual machine and run pytest tests.  

# Running the Code Locally  
Instructions for testing the project locally:  
**1 - Have Python3 installed, and ideally create a new Virtual Environment**  

>python3 -m venv venv  
>source venv/bin/activate  

**2 - Clone the Repo**  

> git clone https://github.com/aalling-ne/CS6620_CI_CD_Pipeline/  
> cd CS6620_CI_CD_Pipeline
  
**3 - Install the Dependancies**  

> pip install -r requirements.txt

**4 - Run the testing file with pytest**

> pytest test_pipeline.py
