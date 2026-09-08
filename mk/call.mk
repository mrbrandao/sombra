# Curl example targets for exercising the Sombra stack
# Output is piped through `jq .` for pretty printing (jq must be installed).

.PHONY: call-analyzer call-litellm test-call

call-analyzer: ## - call the Presidio analyzer directly with sample PT PII
	@curl -s http://localhost:5002/analyze \
		-H "Content-Type: application/json" \
		-d '{"text":"Meu CPF é 123.456.789-00, CEP 80000-000, CNPJ 12.345.678/0001-90, Rua das Flores, 123.","language":"pt"}' \
		| jq .

call-litellm: ## - call the LiteLLM proxy (full masking path) - needs .env sourced
	@if [ -z "$$LITELLM_MASTER_KEY" ]; then \
		echo "Error: LITELLM_MASTER_KEY not set."; \
		echo "Run: set -a; source .env; set +a"; \
		exit 1; \
	fi
	@curl -s http://localhost:4000/v1/chat/completions \
		-H "Authorization: Bearer $$LITELLM_MASTER_KEY" \
		-H "Content-Type: application/json" \
		-d '{"model":"opencode-zen/deepseek-v4-flash","messages":[{"role":"user","content":"Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000."}]}' \
		| jq .

test-call: call-analyzer call-litellm ## - run both curl examples sequentially
	@echo "Done."
