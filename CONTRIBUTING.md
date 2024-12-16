# Contributing Guide

Thank you for your interest in contributing to Anubis! This guide will help you get started and contribute effectively to the project.

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Adding CLI Parameters](#adding-cli-parameters)
3. [Adding New Sources](#adding-new-sources)
4. [Coding Guidelines](#coding-guidelines)
5. [Testing Your Changes](#testing-your-changes)
6. [Submitting Changes](#submitting-changes)
7. [Questions and Support](#questions-and-support)

---

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jonluca/anubis.git
   cd anubis
   ```
2. **Create a Virtual Environment**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
3. **Install Dependencies**:
  ```bash
  pip install -r requirements.txt
  pip install -e .
  ```
4. **Run the CLI: Test the CLI to ensure everything is set up correctly:**
  ```bash
  anubis -h
  ```

## Adding CLI Parameters
Anubis uses docopt to parse CLI parameters. To add a new parameter:

1. **Modify the Header: Update the command definition in anubis/cli.py**:
  ```bash
  anubis -t TARGET [-o FILENAME] [-noispbdvx] [-w SCAN]
  ```
2. **Add your parameter, such as**:

  ```bash
  anubis -t TARGET [-o FILENAME] [-noispbdvx] [-x] [-w SCAN]
  ```
3. **Add a Description: Provide an explanation for the parameter**:

  ```text
  -x                 Sample new command
  ```
4. **Use the Parameter in Code: Reference the parameter using the options dictionary. For example**:

  ```python
  if options["--example"]:
      print("Example flag is enabled!")
  ```
## Adding New Sources
The core functionality for adding sources resides in anubis/commands/target.py, starting with the run() method.

Access Target URL: Use self.options["TARGET"] to get the target URL.

Write Your Function: Add your source-fetching logic in a new function. Ensure:

Add discovered subdomains to self.domains.
Validate subdomains for uniqueness and correctness.
Handle exceptions with:
```python
self.handle_exception(e, "Error message")
```
Integrate Into Thread Pool: Add your function to the thread pool in the run() method.

Output Results: Use ColorPrint.color("message") or print() for stdout messages.

## Coding Guidelines
**Indentation**: Use 2 spaces.
**Style**: Follow PEP 8 and Google style guidelines.
**Consistency**: Maintain consistency with existing project conventions.
## Testing Your Changes
Ensure your changes don't introduce regressions by running tests:

1. **Install Test Dependencies**:

  ```bash
  pip install coverage pytest pytest-cov
  ```
2. **Run Tests**:

  ```bash
  python setup.py test
  ```
3. **Test Coverage: Review the coverage report to ensure your changes are covered**:

  ```bash
  pytest --cov=anubis --cov-report=term-missing
  ```
## Submitting Changes
1. **Fork the Repository: Create your own copy of the repository.**

2. **Create a Feature Branch**:

  ```bash
  git checkout -b feature/your-feature-name
  ```
2. **Commit Your Changes**:
Write clear, concise commit messages.
Format your code to meet project guidelines.
3.**Push Your Branch**:

  ```bash
  git push origin feature/your-feature-name
  ```
4. **Open a Pull Request**:

Describe your changes and reference any related issues.
Ensure your PR passes CI checks.
## Questions and Support
If you have any questions, feel free to:

1. **Open an issue on GitHub.**
2. **Contact @RikDan-CyberSecurity-Research.**

We look forward to your contributions!

```yaml



### **Key Changes:**
- Clearer structure and logical sections.
- Added setup instructions and testing guidelines.
- Expanded the section on contributing workflow.
- Enhanced examples with specific file paths.


```


