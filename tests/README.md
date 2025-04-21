# Tests for Tote Backend API

This directory contains unit tests and integration tests for the Tote Backend API.

## Test Structure

The tests are organized as follows:

- `test_app.py`: Unit tests for the API endpoints with mocked service layer
- `test_services.py`: Unit tests for the service functions with mocked Groq API
- `test_schemas.py`: Unit tests for Pydantic schema validation
- `test_integration.py`: Integration tests that test the full request flow (with mocked Groq API)

## Running Tests

### Prerequisites

- Python 3.8+
- All dependencies installed from `requirements.txt`

### Running All Tests

To run all tests, use the following command from the project root:

```bash
python -m pytest
```

### Running Specific Test Files

To run specific test files:

```bash
python -m pytest tests/test_app.py
python -m pytest tests/test_services.py
python -m pytest tests/test_schemas.py
python -m pytest tests/test_integration.py
```

### Running with Coverage

To run tests with coverage report:

```bash
python -m pytest --cov=. tests/
```

For HTML coverage report:

```bash
python -m pytest --cov=. --cov-report=html tests/
```

## Test Environment

The tests use environment variables for configuration. For testing purposes, 
the Groq API key is mocked, but for local testing, you may want to set:

```bash
export GROQ_API_KEY=your_test_api_key
```

## Adding New Tests

When adding new functionality, please add corresponding tests in the appropriate test file:

1. For new API endpoints: Add tests to `test_app.py`
2. For new service functions: Add tests to `test_services.py`
3. For new schemas: Add tests to `test_schemas.py`
4. For testing the integrated flow: Add tests to `test_integration.py` 