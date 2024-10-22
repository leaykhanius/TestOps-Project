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
