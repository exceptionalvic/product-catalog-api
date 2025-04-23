# Product Catalog API - README

## Overview

This is a RESTful API for managing a product catalog, built with Django and Django REST framework. The API provides CRUD operations for products and includes search/filter functionality.

## Features

- Create, read, update, and delete products
- Search products by name
- Filter products by price range
- Automated API documentation with Swagger
- Unit tests for core functionality using Pytest
- GitHub Actions CI/CD pipeline

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL (for production/testing)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/exceptionalvic/product-catalog-api.git
cd product-catalog-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following content:
```
SECRET_KEY='django-insecure-ngmomncy9yz9&lxc!!%+ocmytn&@0r3&#$pemep=a!@qw%f5_'

# Local project used SQLite3 but for production, PostgreSQL is recommended:
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

### Running the Application

Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

## API Documentation

Swagger documentation is available at:
`http://localhost:8000/api/v1/docs/`

## Testing

Run the test suite with:
```bash
python manage.py test
```

Or with pytest:
```bash
pytest
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/main.yml`) will automatically:
- Set up Python 3.10 and webserver on Docker Containers
- Install dependencies
- Use Flake8 for Python syntax linting to avoid detect syntax errors and other suggestions
- Build the images and deploy to Github Container Registry
- Pull images from container registry and deploy to server

This runs on every successfully merged pull request on develop branch (base branch).

## API Endpoints

### Products

- `GET /api/v1/products/` - List all products (filterable by date added and search term. Can be extended to filter by stock, price etc)
- `POST /api/v1/products/` - Create a new product
- `GET /api/v1/products/<id>/` - Retrieve a product
- `PUT /api/v1/products/<id>/` - Update a product
- `DELETE /api/v1/products/<id>/` - Delete a product

## Example Requests

Create a product:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Keyboard","price":49.99,"stock":30}' http://localhost:8000/api/v1/products/
```

Search products:
```bash
curl "http://localhost:8000/api/v1/products/?search=Maltina"
```

## Project Assumptions

1. Development uses SQLite by default for simplicity
2. Production would use PostgreSQL
3. No authentication is implemented (would be added in production)
4. Price is stored with 2 decimal places (standard currency format)
5. Stock cannot be negative (enforced by model validation)
6. Service/Controller style used in design pattern
7. Project structured for seperation of concerns
8. Docker used as standard for effective deployment and possible container orchestration using Kubernetes


## Future Improvements

1. Add user authentication (JWT or OAuth2)
2. Implement rate limiting
3. Add more advanced search (full-text) as well as other filter params
4. Add pagination to list endpoints
6. Extend from just basic catalog