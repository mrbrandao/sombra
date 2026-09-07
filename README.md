# Sombra

**Sombra** (Portuguese for "shadow") is a local PII anonymization proxy for
agent and LLM CLIs. It intercepts traffic and masks sensitive Brazilian data —
CPF, CEP, CNPJ, street addresses, e-mails and names — in real time before it
reaches a remote LLM provider.

This repository holds the **Sombra** Python package: a set of custom
[Presidio](https://presidio.dataprivacystack.org/) recognizers for Brazilian
PII, plus the container and proxy configuration that wires everything
together.

```
OpenCode CLI → LiteLLM Proxy (:4000) → Presidio Analyzer (:5002) + Anonymizer (:5001) → remote LLM
```

## What Sombra recognizes

Sombra **extends** Presidio's default recognizers with patterns for Brazilian
data. Everything Presidio already detects (names via spaCy NER, e-mails,
phone numbers, locations) keeps working; Sombra only adds what is missing:

| Entity          | Example              | Score |
|-----------------|----------------------|-------|
| `SOMBRA_CPF`    | `123.456.789-00`     | 0.95  |
| `SOMBRA_CEP`    | `80000-000`          | 0.95  |
| `SOMBRA_CNPJ`   | `12.345.678/0001-90` | 0.95  |
| `SOMBRA_ADDRESS`| `Rua das Flores, 123`| 0.75  |

## Installation

> uv is the recommended installer. pip works too — every command below has a
> pip equivalent.

### With uv (recommended)

```bash
git clone <your-repo-url> sombra
cd sombra

# Install the tool (recognizers library) + dev tooling, create the lockfile
uv sync

# Run the recognizer tests
uv run pytest

# Serve the documentation site
uv run mkdocs serve
```

- `uv sync` installs the Sombra tool **and** the dev tooling (mkdocs, pytest,
  which live in the `dev` dependency group).
- `uv sync --no-dev` installs only the Sombra tool itself.
- Once published, `uv tool install sombra` (or `uv pip install sombra` /
  `pip install sombra`) installs the package from PyPI.

### With pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Docs + tests
pip install -e ".[dev]"
```

### Installing from PyPI (future)

Once published, the package can be consumed exactly like any PyPI package:

```bash
uv tool install sombra        # or: uv pip install sombra / pip install sombra
```

## Usage

### 1. Start the local stack (Podman Compose)

```bash
cp .env.example .env        # fill in your real OPENCODE_ZEN_API_KEY
set -a; source .env; set +a
podman-compose up -d --build
```

This starts three services:

- `presidio-analyzer` on `:5002` — spaCy `pt_core_news_lg` + Sombra recognizers
- `presidio-anonymizer` on `:5001` — masks the detected tokens
- `litellm` on `:4000` — OpenAI-compatible proxy with the PII guardrail

### 2. Configure the OpenCode CLI

OpenCode does not auto-load `.env`, so the proxy's master key must be in your shell:

```bash
set -a; source .env; set +a
opencode run "Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000."
```

### 3. Verify masking directly

```bash
curl -s http://localhost:5002/analyze -H "Content-Type: application/json" \
  -d '{"text":"CPF 123.456.789-00, CEP 80000-000, CNPJ 12.345.678/0001-90, Rua das Flores, 123","language":"pt"}'
```

## Development

```bash
uv sync                    # install tool + dev group
uv run pytest              # run tests
uv run ruff check .        # lint (if installed)
uv run mkdocs serve        # preview docs
```

## Documentation

Full documentation is served via mkdocs (see `mkdocs.yml`). The docs include
a synthesis of Presidio's best practices for writing recognizers, so future
entities can be added consistently.

## License

Apache-2.0 — see [LICENSE](LICENSE).