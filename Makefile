# ==========================================
# Docker Compose Command Detection
# ==========================================
# This detects if the system uses 'docker compose' (V2) or 'docker-compose' (V1)
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

# ==========================================
# Variables
# ==========================================
DEV_FILE  = docker-compose.dev.yml
PROD_FILE = docker-compose.prod.yml
VENV      = venv
BIN       = $(VENV)/bin

.PHONY: help dev-build dev-up dev-down dev-logs dev-restart prod-build prod-up prod-down prod-logs prod-restart venv-create venv-clean test test-cov test-watch test-unit clean

# ==========================================
# Help / Information
# ==========================================
help:
	@echo "Discord Nadeshot Bot - Make Commands (Detected: $(DOCKER_COMPOSE))"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev-build    - Build development Docker image"
	@echo "  make dev-up       - Start development container"
	@echo "  make dev-down     - Stop development container"
	@echo "  make dev-logs     - View development container logs"
	@echo "  make dev-restart  - Restart development container"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod-build   - Build production Docker image"
	@echo "  make prod-up      - Start production container"
	@echo "  make prod-down    - Stop production container"
	@echo "  make prod-logs    - View production container logs"
	@echo "  make prod-restart - Restart production container"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make venv-create  - Create virtual environment and install dependencies"
	@echo "  make venv-clean   - Remove virtual environment"
	@echo "  make test         - Run all tests with pytest"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make test-unit    - Run only unit tests"
	@echo "  make test-watch   - Run tests in watch mode (auto-rerun)"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean        - Remove containers, images, and virtual environment"

# ==========================================
# Development Targets
# ==========================================
dev-build:
	$(DOCKER_COMPOSE) -f $(DEV_FILE) build

dev-up:
	$(DOCKER_COMPOSE) -f $(DEV_FILE) up -d

dev-down:
	$(DOCKER_COMPOSE) -f $(DEV_FILE) down

dev-logs:
	$(DOCKER_COMPOSE) -f $(DEV_FILE) logs -f

dev-restart: dev-down dev-up

# ==========================================
# Production Targets
# ==========================================
prod-build:
	$(DOCKER_COMPOSE) -f $(PROD_FILE) build

prod-up:
	$(DOCKER_COMPOSE) -f $(PROD_FILE) up -d

prod-down:
	$(DOCKER_COMPOSE) -f $(PROD_FILE) down

prod-logs:
	$(DOCKER_COMPOSE) -f $(PROD_FILE) logs -f

prod-restart: prod-down prod-up

# ==========================================
# Virtual Environment & Testing
# ==========================================
venv-create:
	python3 -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

venv-clean:
	rm -rf $(VENV)

test: venv-create
	$(BIN)/pytest

test-cov: venv-create
	$(BIN)/pytest --cov=. --cov-report=html --cov-report=term

test-unit: venv-create
	$(BIN)/pytest -m unit

test-watch: venv-create
	$(BIN)/pytest-watch

# ==========================================
# Cleanup
# ==========================================
clean: venv-clean
	$(DOCKER_COMPOSE) -f $(DEV_FILE) down -v
	$(DOCKER_COMPOSE) -f $(PROD_FILE) down -v
	docker rmi discord-nadeshot-bot-dev discord-nadeshot-bot-prod 2>/dev/null || true