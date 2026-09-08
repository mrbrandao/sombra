# Podman Compose lifecycle targets for the Sombra stack
# Rootless Podman only. Secrets come from `.env` (never hardcoded).
# Targets that need the environment first run `guard-env`.

.PHONY: guard-env up down build logs

guard-env: ## - ensure .env exists and is sourced
	@if [ ! -f ".env" ]; then \
		echo "Error: .env not found."; \
		echo "Run: cp .env.example .env"; \
		echo "Then fill in your OPENCODE_ZEN_API_KEY."; \
		exit 1; \
	fi
	@set -a; source .env; set +a

up: guard-env ## - start the full stack (analyzer, anonymizer, litellm)
	@set -a; source .env; set +a; \
	echo "Starting Sombra stack..."; \
	podman-compose up -d --build

down: ## - stop the stack
	@echo "Stopping Sombra stack..."
	@podman-compose down

build: guard-env ## - build the analyzer image only (no run)
	@set -a; source .env; set +a; \
	echo "Building Sombra analyzer image..."; \
	podman-compose build

logs: ## - follow the stack logs
	@podman-compose logs -f
