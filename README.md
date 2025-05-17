# Tote Backend

[![codecov](https://codecov.io/gh/tadeodonegana/devops-up/graph/badge.svg?token=HXSTTPC2P6)](https://codecov.io/gh/tadeodonegana/devops-up)

## Features

- **Product Recommendations**: Get personalized product recommendations based on your shopping list.
- **Dish Ingredients**: Get a list of ingredients needed for specific dishes.
- **Product Categorization**: Categorize products into appropriate supermarket categories.
- **Health Check**: Check the health of the API.

## Prerequisites

- Python 3.8+
- [Groq API Key](https://console.groq.com/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tote-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   # On Windows
   set GROQ_API_KEY=your-api-key-here
   # On macOS/Linux
   export GROQ_API_KEY=your-api-key-here
   ```

## Running the Application Locally

Start the application with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

### 1. Product Recommendations

**Endpoint**: `POST /recommendations`

**Request Body**:
```json
{
  "products": ["tomate", "lechuga", "cebolla", "papa"]
}
```

**Response**:
```json
{
  "recommended_items": [
    "aceite de oliva",
    "sal",
    "pimienta",
    "ajo",
    "limón",
    "vinagre"
  ]
}
```

### 2. Dish Ingredients

**Endpoint**: `GET /dishes/ingredients?dish_name=milanesa`

**Query Parameters**:
- `dish_name`: Name of the dish to get ingredients for

**Response**:
```json
{
  "ingredients": [
    "carne (bife de nalga o peceto)",
    "huevos",
    "pan rallado",
    "sal",
    "pimienta",
    "ajo en polvo",
    "perejil",
    "aceite para freír"
  ]
}
```

### 3. Product Categorization

**Endpoint**: `POST /categorize-products`

**Request Body**:
```json
{
  "categorized_products": {
    "Frutas y Verduras": ["manzana", "banana", "lechuga", "tomate"],
    "Carnes": ["pollo", "carne picada"],
    "Lácteos": ["leche", "queso", "yogur"]
  },
  "uncategorized_products": ["harina", "arroz", "atún", "papel higiénico", "detergente"]
}
```

**Response**:
```json
{
  "categories": {
    "Frutas y Verduras": ["manzana", "banana", "lechuga", "tomate"],
    "Carnes": ["pollo", "carne picada"],
    "Lácteos": ["leche", "queso", "yogur"],
    "Abarrotes": ["harina", "arroz"],
    "Conservas": ["atún"],
    "Limpieza": ["papel higiénico", "detergente"]
  }
}
```

## AWS Lambda Deployment

The application includes Mangum for AWS Lambda compatibility. To deploy:

1. Create a deployment package:
   ```bash
   pip install -r requirements.txt --target ./dependencies
   cd dependencies
   zip -r ../aws_lambda_artifact.zip .
   cd ..
   zip -g aws_lambda_artifact.zip main.py services.py schemas.py
   ```

2. Upload the `aws_lambda_artifact.zip` file to your AWS Lambda function.

3. Set the Lambda handler to `main.handler`.

4. Configure environment variables in the Lambda console:
   - `GROQ_API_KEY`: Your Groq API key

## Development

### Testing

The application includes a comprehensive test suite with unit tests and integration tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=. tests/

# Run specific test files
pytest tests/test_app.py -v
pytest tests/test_services.py -v
pytest tests/test_schemas.py -v
```

The tests are structured as follows:
- `test_app.py`: Tests the API endpoints with mocked service functions
- `test_services.py`: Tests service functions with mocked Groq API
- `test_schemas.py`: Tests Pydantic schema validation
- `test_integration.py`: Integration tests for the API with mocked Groq client

All tests are designed to run without a real Groq API key. The test suite uses mocks to simulate API responses, making it easy to run in CI environments.

### GitHub CI/CD Workflow

The project includes GitHub Actions workflows for:

1. **PR Tests**: Runs whenever a PR is opened, synchronized, or reopened
   - Runs all tests with coverage reporting
   - Uploads coverage reports to Codecov
   - Comments on the PR with test results

2. **Deploy Workflow**: Runs on pushes to the main branch and PRs
   - Runs all tests with coverage reporting
   - For main branch only: Builds and pushes Docker image
   - For main branch only: Deploys to Render

### Testing with a Real API Key

If you want to run tests against the actual Groq API (not recommended for regular development), you can set the GROQ_API_KEY environment variable before running the tests:

```bash
# On Windows
set GROQ_API_KEY=your-api-key-here && pytest

# On macOS/Linux
GROQ_API_KEY=your-api-key-here pytest
```

## Notes

- The application uses Groq's LLaMa 3.3 70B model for all AI functionalities.
- All responses are provided in Spanish, tailored for users in Argentina.
- The Instructor library is used to format LLM responses according to Pydantic models.