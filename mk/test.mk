# Test targets for the Sombra package

.PHONY: test

test: ## - run the recognizer test suite
	@echo "Running tests..."
	@uv run pytest
