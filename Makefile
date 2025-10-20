# AI Agent System Makefile

.PHONY: help install test run build clean docker-build docker-run docker-stop lint format

# Default target
help:
	@echo "AI Agent System - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests"
	@echo "  run         - Run the application locally"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build    - Build Docker image"
	@echo "  docker-run      - Run with Docker Compose"
	@echo "  docker-dev      - Run development environment"
	@echo "  docker-stop     - Stop Docker containers"
	@echo "  docker-clean    - Clean Docker resources"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       - Clean temporary files"
	@echo "  setup       - Initial project setup"

# Development commands
install:
	pip install -r requirements.txt

test:
	pytest -v --tb=short

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term

run:
	python app.py

lint:
	flake8 . --max-line-length=100 --ignore=E203,W503,E501 --exclude=Lib,Scripts,build,dist,.venv,venv
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=Lib,Scripts,build,dist,.venv,venv

format:
	black . --line-length=100 --exclude="/(Lib|Scripts|build|dist|\.venv|venv)/"
	isort . --profile=black --line-length=100 --skip-glob="Lib/*" --skip-glob="Scripts/*"

type-check:
	mypy analyzers agents generators llm orchestrator routes services --config-file=mypy.ini

test-with-coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

quality: format lint type-check test-with-coverage
	@echo "✅ All quality checks passed!"

# Docker commands
docker-build:
	docker build -t ai-agent-system .

docker-run:
	docker-compose up -d

docker-dev:
	docker-compose -f docker-compose.dev.yml up -d

docker-stop:
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

docker-clean:
	docker-compose down -v --rmi all
	docker-compose -f docker-compose.dev.yml down -v --rmi all
	docker system prune -f

# Setup commands
setup: install
	@echo "Setting up AI Agent System..."
	@mkdir -p data logs exports settings
	@cp config.env .env
	@echo "Setup complete! Please edit .env with your API keys."

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Production commands
deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.yml up -d --build

logs:
	docker-compose logs -f

status:
	docker-compose ps

# Health check
health:
	curl -f http://localhost:8000/test || echo "Service is not healthy"

# Database commands
db-migrate:
	@echo "Running database migrations..."
	# Add migration commands here

db-reset:
	@echo "Resetting database..."
	rm -f data/*.db
	@echo "Database reset complete"

# API testing
test-api:
	@echo "Testing API endpoints..."
	curl -s http://localhost:8000/ | jq .
	curl -s http://localhost:8000/status | jq .
	curl -s http://localhost:8000/test | jq .

# Development workflow
dev-setup: setup
	@echo "Setting up development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development environment ready!"

dev-test:
	docker-compose -f docker-compose.dev.yml exec ai-agent-system-dev pytest

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f ai-agent-system-dev
