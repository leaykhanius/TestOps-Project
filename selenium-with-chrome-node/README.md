# Selenium Test Execution System

## Overview

This system executes Selenium test cases in a Kubernetes environment, using two pods: one for managing test execution (Test Controller Pod) and another for running tests in a headless Chrome browser (Chrome Node Pod).

- **Test Controller Pod**: Collects and manages test cases, then sends them to the Chrome Node Pod for execution.
- **Chrome Node Pod**: Runs a headless Chrome browser where the tests are executed.

## How It Works

1. **Test Controller Pod**:
   - Contains the test cases (`run_tests.py`).
   - Uses **Remote WebDriver** to connect to the Chrome Node Pod.
   - Sends WebDriver commands (e.g., open a URL, click a button) to the Chrome Node Pod for execution.

2. **Chrome Node Pod**:
   - Runs a headless Chrome browser.
   - Receives WebDriver commands from the Test Controller Pod.
   - Executes the browser actions and sends results back to the Test Controller Pod.


## Architecture

### Test Case Controller Pod:
- Hosts the test cases (`run_tests.py`) written in Python and Selenium.
- Sends commands via **Remote WebDriver** to the Chrome Node Pod.
- Collects test results and logs after execution.

### Chrome Node Pod:
- Runs headless Chrome for executing WebDriver commands sent by the Test Case Controller Pod.
- Communicates with the Test Case Controller Pod using Kubernetes Services for streamlined inter-pod communication.

## Inter-Pod Communication

Inter-pod communication is established by Kubernetes Services:

- **Test Case Controller Pod** sends requests to the **Chrome Node Pod** using a service (`chrome-node-svc`) configured as `ClusterIP`, which allows internal Kubernetes communication.
- **DNS-based service discovery** is used to connect the Test Case Controller Pod to the Chrome Node Pod at `http://chrome-node-svc:3000/webdriver`.

## Components

### Kubernetes Deployment Files

- **chrome-node-deploy.yaml**:
  - Creates the Chrome Node Pod with the **browserless/chrome** image.
  - Configured with `containerPort` 3000, enabling the Chrome Node Pod to receive WebDriver commands.

- **test-case-controller-deploy.yaml**:
  - Deploys the Test Case Controller Pod with the custom Docker image specified in the `Dockerfile`.

### Python Automation Script for Kubernetes Deployment and Test Execution

The automation script (`deploy_job.py`) facilitates the deployment and execution of test cases by:

- **Deploying Kubernetes Resources**:
  - Applies Kubernetes YAML configurations for the Test Controller and Chrome Node pods.
  - Scales the Chrome Node deployment dynamically based on a specified node count.

- **Readiness Check**:
  - Verifies the readiness of Chrome Node Pods before initiating test cases.

- **Test Execution**:
  - Initiates the Selenium test suite on the Test Controller Pod once Chrome Node Pods are ready.

### Dockerfiles

- **Dockerfile**:
  - Installs Python dependencies, including Selenium, and adds the test suite to the container.
  - Configures the container to execute `run_tests.py` in a headless Chrome browser environment.

## Deployment Process

### Building Docker Images:

1. **Build the Docker image for the Test Controller Pod**:
   ```
   docker build -t your-repo/selenium-test-cases-chrome-node:v1 .
   docker push your-repo/selenium-test-cases-chrome-node:v1
   ```
   - *(Ensure Chrome Node Pod uses an existing image like `browserless/chrome:latest` or similar.)*

### Deploying Kubernetes Resources Using `deploy_job`

**Run `deploy_job.py` for Automated Deployment**:
   - The `deploy_job.py` script automates the deployment of all Kubernetes resources, including pods and services for the Test Case Controller and Chrome Node. Ensure `deploy_job.py` is configured to apply these resources with the necessary configurations for your environment.


### Running the Automation Script

- **Execute `deploy_job.py` to Automate Readiness Checks and Test Execution**:
   ```
   python deploy_job.py
   ```
   - This script verifies pod readiness, passes test cases to the Chrome Node Pod, and initiates test execution.

### Deploying on AWS EKS

1. **Set Up an EC2 Instance**:
   - Install `kubectl` and configure it to connect to the EKS cluster.

2. **Deploy Kubernetes Resources on EKS**:
   - Execute `deploy_job.py` to deploy the same Kubernetes resources on AWS EKS, enabling cloud-based test execution.

## How Tests Are Executed

1. **Test Case Controller Pod Initialization**:
   - Initializes and reads test cases from `run_tests.py`.
   - Establishes communication with the Chrome Node Pod using `http://chrome-node-svc:3000/webdriver`.

2. **Executing Tests**:
   - The Test Controller Pod sends WebDriver commands (like navigating to URLs, clicking buttons) to the Chrome Node Pod.
   - The Chrome Node Pod performs these actions in a headless Chrome environment and returns results.

3. **Retrieving Results**:
   - The Test Controller Pod collects output, logs, and screenshots to summarize test results.

## Deliverables
**GitHub Repository Structure**:
   - **Selenium Tests**: Python scripts implementing test cases.
   - **Dockerfile**: Instructions for building the image for the Test Controller Pod.
   - **Kubernetes YAML Files**: Configuration files (`chrome-node-deploy.yaml`, `chrome-node-svc.yaml`, `test-case-controller-deploy.yaml`, `test-case-controller-svc.yaml`) for deploying the resources.
   - **README.md**: Detailed system overview and setup guide.

