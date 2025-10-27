# Contributing to AWS Security Scanner

First off, thank you for considering contributing to AWS Security Scanner! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be respectful in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if relevant**
* **Include your environment details** (Python version, OS, AWS region)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the proposed enhancement**
* **Explain why this enhancement would be useful**
* **List any alternative solutions or features you've considered**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/aws-security-scanner.git
cd aws-security-scanner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install pytest pylint flake8  # Development dependencies
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

## Coding Standards

### Python Style Guide

* Follow PEP 8 style guidelines
* Use meaningful variable and function names
* Add docstrings to all functions and classes
* Keep functions focused and concise
* Maximum line length: 100 characters

### Example:

```python
def scan_resource(resource_type, resource_id):
    """
    Scan a specific AWS resource for vulnerabilities.
    
    Args:
        resource_type (str): Type of AWS resource (e.g., 's3', 'ec2')
        resource_id (str): Unique identifier for the resource
        
    Returns:
        list: List of vulnerability dictionaries
    """
    vulnerabilities = []
    # Implementation here
    return vulnerabilities
```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters
* Reference issues and pull requests after the first line

Example:
```
Add RDS encryption check

- Implement check for RDS storage encryption
- Add test cases for encrypted and unencrypted instances
- Update documentation with new check

Fixes #123
```

## Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Aim for good code coverage

Run tests:
```bash
pytest tests/
```

Run linting:
```bash
flake8 aws_security_scanner.py
pylint aws_security_scanner.py
```

## Adding New Security Checks

When adding a new security check:

1. Add the check method to the `AWSSecurityScanner` class
2. Call the method in `run_scan()`
3. Follow the existing pattern for vulnerability reporting
4. Update README.md with the new check
5. Add appropriate error handling
6. Include test cases

Example structure:
```python
def scan_new_resource(self):
    """Check new resource type for security issues"""
    print("\n[*] Scanning New Resource...")
    try:
        # Your scanning logic here
        if condition_is_vulnerable:
            self.vulnerabilities.append({
                'severity': 'HIGH',
                'resource': f'Resource: {resource_name}',
                'issue': 'Description of the issue',
                'recommendation': 'How to fix it'
            })
    except ClientError as e:
        print(f"  Error scanning new resource: {e}")
```

## Documentation

* Update README.md for user-facing changes
* Add docstrings to new functions/classes
* Update inline comments for complex logic
* Include examples where helpful

## Questions?

Feel free to open an issue with the `question` label if you have any questions about contributing!

## Recognition

Contributors will be recognized in the project README. Thank you for your contributions! 🎉
