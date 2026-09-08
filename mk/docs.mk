# VitePress targets for documentation management
# The docs site runs on VitePress (see package.json), so dependency setup is
# a single `npm install` shared by every target that needs it.

.PHONY: docs-deps docs-build docs-serve docs-preview docs-clean docs-check

docs-deps: ## - install docs tooling (VitePress via npm)
	@npm install

docs-build: docs-deps ## - build static documentation site
	@echo "Building documentation site..."
	@npm run docs:build

docs-serve: docs-deps ## - start VitePress development server
	@echo "Starting VitePress development server..."
	@npm run docs:dev

docs-preview: docs-build ## - preview the built documentation site
	@echo "Previewing documentation site..."
	@npm run docs:preview

docs-clean: ## - clean built documentation files
	@echo "Cleaning documentation build files..."
	@rm -rf docs/.vitepress/dist docs/.vitepress/cache
	@echo "Documentation build files cleaned."

docs-check: docs-deps ## - check documentation for issues
	@echo "Checking documentation configuration..."
	@if [ ! -f "docs/.vitepress/config.mts" ]; then \
		echo "Error: docs/.vitepress/config.mts not found in current directory"; \
		exit 1; \
	fi
	@npm run docs:build