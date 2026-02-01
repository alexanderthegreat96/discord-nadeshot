.PHONY: help dev-build dev-up dev-down dev-logs dev-restart prod-build prod-up prod-down prod-logs prod-restart venv-create venv-clean test test-cov test-watch test-unit clean

help:
	@echo "Discord Nadeshot Bot - Make Commands"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev-build    - Build development Docker image"
	@echo "  make dev-up       - Start development container with docker-compose"
	@echo "  make dev-down     - Stop development container"
	@echo "  make dev-logs     - View development container logs"
	@echo "  make dev-restart  - Restart development container"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod-build   - Build production Docker image"
	@echo "  make prod-up      - Start production container with docker-compose"
	@echo "  make prod-down    - Stop production container"
	@echo "  make prod-logs    - View production container logs"
	@echo "  make prod-restart - Restart production container"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make venv-create  - Create Python virtual environment and install dependencies"
	@echo "  make venv-clean   - Remove virtual environment"
	@echo "  make test         - Run all tests with pytest"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make test-unit    - Run only unit tests"
	@echo "  make test-watch   - Run tests in watch mode (auto-rerun on changes)"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean        - Remove all containers, images, and virtual environment"
	@echo "  make help         - Show this help message"

# Development targets
dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-up:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-restart: dev-down dev-up

# Production targets
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-restart: prod-down prod-up

# Utility targets
venv-create:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

venv-clean:
	rm -rf venv

test: venv-create
	. venv/bin/activate && pytest

test-cov: venv-create
	. venv/bin/activate && pytest --cov=. --cov-report=html --cov-report=term

test-unit: venv-create
	. venv/bin/activate && pytest -m unit

test-watch: venv-create
	. venv/bin/activate && pytest-watch

clean: venv-clean
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker rmi discord-nadeshot-bot-dev discord-nadeshot-bot-prod 2>/dev/null || true
