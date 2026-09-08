# Configure OpenCode

Point the OpenCode CLI at your local Sombra proxy.

## 1. Add the provider

OpenCode is configured via `opencode.json` in the project root. This file is
already shipped in the repo — it registers the local LiteLLM proxy as a
provider and selects its PII-protected model by default:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "litellm-proxy": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Sombra LiteLLM Proxy",
      "options": {
        "baseURL": "http://localhost:4000/v1",
        "apiKey": "{env:LITELLM_MASTER_KEY}"
      },
      "models": {
        "opencode-zen/deepseek-v4-flash": {
          "name": "Sombra - DeepSeek v4 Flash (PII Protected)"
        }
      }
    }
  },
  "model": "litellm-proxy/opencode-zen/deepseek-v4-flash"
}
```

## 2. Export the master key

OpenCode does **not** auto-load `.env`, so the proxy's master key must be in
your shell before starting OpenCode:

```bash
set -a; source .env; set +a
```

## 3. Start OpenCode

```bash
opencode run "Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000."
```

Every request to the model now passes through Sombra's masking guardrail
before leaving your machine.

## Next

Your setup is complete. Verify it works with [Use it](./use-it).