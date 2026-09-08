# Quick tests

Smoke-test the Sombra stack with ready-made curl examples.

## Prerequisites

- Stack running: `make up`
- `jq` installed (output is piped through it for pretty printing)

## Run the examples

```bash
make call-analyzer   # hit the Presidio analyzer directly (:5002)
make call-litellm    # hit the full proxy masking path (:4000), needs .env sourced
make test-call       # run both sequentially
```

`make test-call` is the fastest way to verify the whole chain in one shot.

## Expected analyzer output

`make call-analyzer` detects entities in the sample text:

| Entity           | Confidence |
|------------------|------------|
| `SOMBRA_CPF`     | 0.95 (1.00 with context) |
| `SOMBRA_CEP`     | 0.95       |
| `SOMBRA_CNPJ`    | 0.95       |
| `SOMBRA_ADDRESS` | 0.75       |
| `PERSON` / `LOCATION` | 0.85 (spaCy NER) |

## Expected masked prompt

`make call-litellm` sends a chat request through the full masking path. The
LiteLLM logs show the prompt reaching the provider already masked:

```
"content": "Consult my order in the name of João, CPF <SOMBRA_CPF>, living in Curitiba, CEP <SOMBRA_CEP>."
```

## Run them by hand

```bash
curl -s http://localhost:5002/analyze -H "Content-Type: application/json" \
  -d '{"text":"Meu CPF é 123.456.789-00, CEP 80000-000, CNPJ 12.345.678/0001-90, Rua das Flores, 123.","language":"pt"}' | jq .

curl -s http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"opencode-zen/deepseek-v4-flash","messages":[{"role":"user","content":"Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000."}]}' | jq .
```

## Next

These are smoke tests. For the real test suite, see [Testing](./testing).