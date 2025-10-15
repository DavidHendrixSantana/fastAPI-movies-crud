# Movies CRUD API

A comprehensive FastAPI application for managing movies with full CRUD operations, comprehensive testing, containerization, and CI/CD pipeline.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, Delete movies
- **Advanced Filtering**: Search by title, director, year range
- **Data Validation**: Comprehensive Pydantic models with validation
- **Database Support**: SQLite (default) and PostgreSQL
- **Interactive Documentation**: Automatic OpenAPI/Swagger UI
- **High Test Coverage**: >80% test coverage with pytest
- **Containerized**: Docker and docker-compose support
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Code Quality**: Linting, formatting, and type checking
- **Security**: Built-in security checks and best practices

## 🏗️ Architecture

The application follows a clean architecture pattern:

```
fastAPI_movies_crud/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI app creation and configuration
│   ├── database.py        # Database models and configuration
│   ├── schemas.py         # Pydantic schemas for validation
│   ├── services.py        # Business logic layer
│   └── routers.py         # API route definitions
├── tests/                 # Comprehensive test suite
│   ├── conftest.py        # Test configuration and fixtures
│   ├── test_routers.py    # API endpoint tests
│   ├── test_services.py   # Service layer tests
│   └── test_schemas.py    # Schema validation tests
├── .github/workflows/     # CI/CD pipeline configuration
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container orchestration
├── pyproject.toml        # Project configuration
└── requirements.txt      # Python dependencies
```

## 📋 Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- Git (for version control)

## 🛠️ Installation & Setup

### Quick Setup (Development Script)

```bash
# Make the development script executable
chmod +x dev.sh

# Setup development environment
./dev.sh setup

# Run the application
./dev.sh dev
```

### Manual Setup

1. **Clone the repository**:
```bash
git clone https://github.com/DavidHendrixSantana/fastAPI-movies-crud.git
cd fastAPI-movies-crud
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv

# On Windows
source venv/Scripts/activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Running the Application

### Development Mode

```bash
# Using the development script
./dev.sh dev

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t movies-crud-api .
docker run -p 8000:8000 movies-crud-api
```

### With PostgreSQL

```bash
# Start with PostgreSQL support
docker-compose --profile postgres up --build
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

### Run All Tests

```bash
# Using development script
./dev.sh test

# Or manually
pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80 -v
