# Architecture

How Sombra intercepts and masks your prompts.

## Data flow

```
        +------------------------------------------------------------------+
        |                              OpenCode CLI                         |
        |                    (agent / LLM CLI - your prompts)              |
        +----------------------------------+-------------------------------+
                                           |  HTTP (OpenAI-compatible)
                                           v
        +------------------------------------------------------------------+
        |                         LiteLLM Proxy  (:4000)                   |
        |                   OpenAI-compatible API surface                  |
        |      master_key auth  +  Presidio guardrail  (pre_call)         |
        +--------+-----------------------------+--------------------------+
                 | analyze (detect PII)         | anonymize (mask tokens)
                 v                              v
        +--------------------+          +---------------------+
        | Presidio Analyzer  |  :5002  | Presidio Anonymizer |  :5001
        | spaCy pt_core_news_lg        | replaces PII with   |
        | + SOMBRA_* regexes  |          | <SOMBRA_CPF> etc.  |
        +--------------------+          +---------------------+
                 |                          |
                 +------------+-------------+
                              v
        +------------------------------------------------------------------+
        |                        Remote LLM provider                       |
        |                  (OpenCode Zen / DeepSeek v4 Flash)              |
        |                    receives ONLY masked prompts                   |
        +------------------------------------------------------------------+
```

## Components

| Component | Role |
|-----------|------|
| `presidio-analyzer` | spaCy `pt_core_news_lg` NER + Sombra regex recognizers; detects PII in the prompt |
| `presidio-anonymizer` | Replaces the detected tokens with masks |
| `litellm` | OpenAI-compatible proxy; runs the Presidio guardrail in `pre_call` mode |

## Notes

- All services run as rootless Podman containers via `docker-compose.yml`.
- Secrets are read only from the environment — never hardcoded in
  configuration.
- The guardrail runs in `pre_call` mode, so masking happens **before** the
  request reaches the remote provider.

## Next

See [What Sombra detects](./what-sombra-detects) for the full list of
recognized entities.