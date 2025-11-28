# Contributing to dataDisk

Thank you for considering contributing to dataDisk! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/dataDisk.git
   cd dataDisk
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

These checks will run automatically when you commit code if you've installed the pre-commit hooks.

## Testing

We use pytest for testing. To run tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=dataDisk
```

## Pull Request Process

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive commit messages:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

3. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a pull request against the main repository's `main` branch

5. Ensure your PR description clearly describes the changes and the problem it solves

## Release Process

1. Update version number in:
   - `dataDisk/__init__.py`
   - `pyproject.toml`
   - `setup.py`

2. Update CHANGELOG.md with the new version and changes

3. Create a new GitHub release with appropriate tag

## Code of Conduct

Please be respectful and inclusive in your interactions with others in this project.