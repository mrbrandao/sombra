# Sombra

**Sombra** (Portuguese for "shadow") is a local PII anonymization proxy for
agent and LLM CLIs. It intercepts traffic and masks sensitive Brazilian data —
CPF, CEP, CNPJ, street addresses, e-mails and names — in real time before it
reaches a remote LLM provider.

```
OpenCode CLI → LiteLLM Proxy (:4000) → Presidio Analyzer (:5002) + Anonymizer (:5001) → remote LLM
```

## Architecture

| Component | Role |
|-----------|------|
| `presidio-analyzer` | spaCy `pt_core_news_lg` NER + Sombra regex recognizers; detects PII in the prompt |
| `presidio-anonymizer` | Replaces the detected tokens with masks |
| `litellm` | OpenAI-compatible proxy; runs the Presidio guardrail in `pre_call` mode |

All services run as rootless Podman containers via `docker-compose.yml`.
Secrets are read only from the environment — never hardcoded in configuration.

## What Sombra detects

Sombra **extends** Presidio's default recognizers. Everything Presidio already
detects keeps working (names via spaCy NER, e-mails, phone numbers, URLs,
locations); Sombra adds the Brazilian patterns that are missing:

| Entity           | Example                  | Confidence |
|------------------|--------------------------|------------|
| `SOMBRA_CPF`     | `123.456.789-00`         | 0.95 (1.00 with context) |
| `SOMBRA_CEP`     | `80000-000`              | 0.95       |
| `SOMBRA_CNPJ`    | `12.345.678/0001-90`     | 0.95       |
| `SOMBRA_ADDRESS` | `Rua das Flores, 123`    | 0.75       |
| `PERSON`         | `João` (spaCy NER)       | 0.85       |
| `LOCATION`       | `Curitiba` (spaCy NER)   | 0.85       |

## Recognizer development

This section synthesizes the official Presidio guides — [Adding
recognizers](https://presidio.dataprivacystack.org/analyzer/adding_recognizers/)
and [Recognizer development best
practices](https://presidio.dataprivacystack.org/analyzer/developing_recognizers/) —
and shows how they apply to Sombra.

### Recognizer types

Presidio has three families of recognizers:

1. **Deny lists** — a fixed list of words to flag (e.g. titles like `Dr.`).
2. **Pattern-based** — regular expressions, optionally with *context* words
   that raise confidence when a keyword appears nearby. This is what Sombra
   uses.
3. **ML / rule-based** — spaCy, Stanza or Transformers NER models, or custom
   logic over NLP features. Sombra uses spaCy's `pt_core_news_lg` for
   `PERSON` and `LOCATION`.

### Best practices (from the Presidio guide)

- **Accuracy**: balance false positives and false negatives. A recognizer
  with many false positives hurts usability. Prefer *context* words to boost
  confidence instead of lowering scores.
- **Performance**: keep recognition under ~100 ms per 100 tokens. Pure regex
  recognizers (like Sombra's) easily satisfy this, which keeps the overall
  <150 ms latency budget.
- **Environment**: don't let third-party dependencies interfere with
  Presidio's. Sombra only depends on the `regex` module.
- **Extend, don't replace**: register Sombra recognizers on top of the default
  set. The default recognizers and spaCy NER keep working unchanged.

### How Sombra's recognizers are defined

Recognizers can be defined in code (`PatternRecognizer` subclasses in
`src/sombra/sombra_recog.py`) or declaratively in YAML
(`containers/sombra_recognizers.yaml`). Both describe the same thing and the
tests in `src/sombra/tests/` cover both.

A pattern-based recognizer pairs a regular expression with a confidence score
and a list of context words:

```python
from presidio_analyzer import Pattern, PatternRecognizer


class CpfRecognizer(PatternRecognizer):
    ENTITY = "SOMBRA_CPF"

    PATTERNS = [
        Pattern("CPF formatted", r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", 0.95),
        Pattern("CPF unformatted", r"\b\d{11}\b", 0.50),
    ]

    CONTEXT = ["cpf", "documento", "inscrição", "cadastro de pessoa física"]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="CpfRecognizer",
            supported_language="pt",
        )
```

The same recognizer in the container's registry YAML (which the analyzer loads
via the `RECOGNIZER_REGISTRY_CONF_FILE` environment variable):

```yaml
  - name: "Sombra CPF recognizer"
    supported_language: "pt"
    patterns:
      - name: "CPF formatted"
        regex: "\\b\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}\\b"
        score: 0.95
    context: [cpf, documento, inscrição]
    supported_entity: "SOMBRA_CPF"
```

!!! tip "Adding a new entity"
    To add a new Brazilian entity: (1) add a `PatternRecognizer` subclass in
    `src/sombra/sombra_recog.py`, (2) add a matching YAML block in
    `containers/sombra_recognizers.yaml`, (3) write tests in
    `src/sombra/tests/`, and (4) add the entity to the guardrail's
    `pii_entities_config` in `config.yaml`.

## Getting started

### Requirements

- [uv](https://docs.astral.sh/uv/) (recommended installer)
- Rootless [Podman](https://podman.io/) with `podman-compose`

### Install

```bash
uv sync            # installs the sombra package + dev tooling (mkdocs, pytest)
uv run pytest      # run the recognizer tests
```

Prefer pip? See the `README.md` for the pip-equivalent commands.

### Run the stack

```bash
set -a; source .env; set +a
podman-compose up -d --build
```

Services: analyzer on `:5002`, anonymizer on `:5001`, LiteLLM on `:4000`.

### Verify masking

1. **Analyzer** — detect PII directly:

```bash
curl -s http://localhost:5002/analyze -H "Content-Type: application/json" \
  -d '{"text":"Meu CPF é 123.456.789-00, CEP 80000-000, CNPJ 12.345.678/0001-90, Rua das Flores, 123.","language":"pt"}'
```

2. **Full proxy path** — send a chat request with PII through LiteLLM. The
   Presidio guardrail masks the prompt before it reaches the remote provider:

```bash
curl -s http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "opencode-zen/deepseek-v4-flash",
    "messages": [{
      "role": "user",
      "content": "Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000."
    }]
  }'
```

With `LITELLM_LOG=DEBUG` you can confirm in the LiteLLM logs that the prompt
reaches the provider already masked, e.g. `"content": "Consult my order in
the name of João, CPF <SOMBRA_CPF>, living in Curitiba, CEP <SOMBRA_CEP>."`.

### Documentation site

```bash
uv run mkdocs serve
```

## Related resources

- [Presidio — adding recognizers](https://presidio.dataprivacystack.org/analyzer/adding_recognizers/)
- [Presidio — recognizer best practices](https://presidio.dataprivacystack.org/analyzer/developing_recognizers/)
- [Presidio — PII masking LLM calls with LiteLLM](https://github.com/data-privacy-stack/presidio/tree/main/docs/samples/docker/litellm)
- [LiteLLM — guardrails](https://docs.litellm.ai/docs/proxy/guardrails)