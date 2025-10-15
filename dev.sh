#!/bin/bash

# Development script for Movies CRUD API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Setup development environment
setup_dev() {
    print_info "Setting up development environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    print_info "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_info "Development environment setup complete!"
}

# Run tests
run_tests() {
    print_info "Running tests..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80 -v
}

# Run linting
run_lint() {
    print_info "Running linting checks..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    print_info "Running flake8..."
    flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503
    
    print_info "Running black..."
    black --check app/ tests/
    
    print_info "Running isort..."
    isort --check-only app/ tests/
    
    print_info "All linting checks passed!"
}

# Format code
format_code() {
    print_info "Formatting code..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    print_info "Running black..."
    black app/ tests/
    
    print_info "Running isort..."
    isort app/ tests/
    
    print_info "Code formatting complete!"
}

# Run the application
run_dev() {
    print_info "Starting development server..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Run with Docker
run_docker() {
    print_info "Building and running with Docker..."
    
    # Build image
    docker build -t movies-crud-api .
    
    # Run container
    docker run --rm -p 8000:8000 movies-crud-api
}

# Clean up
clean() {
    print_info "Cleaning up..."
    
    # Remove cache files
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    find . -type f -name "*.coverage" -delete
    rm -rf .pytest_cache/
    rm -rf htmlcov/
    rm -rf .mypy_cache/
    rm -rf test_*.db
    
    print_info "Cleanup complete!"
}

# Show help
show_help() {
    echo "Movies CRUD API Development Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     Setup development environment"
    echo "  test      Run tests with coverage"
    echo "  lint      Run linting checks"
    echo "  format    Format code with black and isort"
    echo "  dev       Start development server"
    echo "  docker    Build and run with Docker"
    echo "  clean     Clean up cache files"
    echo "  help      Show this help message"
    echo ""
}

# Main script logic
case "${1:-help}" in
    setup)
        setup_dev
        ;;
    test)
        run_tests
        ;;
    lint)
        run_lint
        ;;
    format)
        format_code
        ;;
    dev)
        run_dev
        ;;
    docker)
        run_docker
        ;;
    clean)
        clean
        ;;
    help|*)
        show_help
        ;;
esac