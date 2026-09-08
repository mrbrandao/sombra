# Install

Get Sombra running locally in three commands.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — recommended Python installer
- Rootless [Podman](https://podman.io/) with `podman-compose`
- [Node.js](https://nodejs.org/) 18+ and npm — for the docs site (optional)

## 1. Clone and install

```bash
git clone <your-repo-url> sombra
cd sombra
uv sync
```

This installs the Sombra recognizer library plus the test tooling.

## 2. Create your environment file

```bash
cp .env.example .env
```

Then open `.env` and set your real `OPENCODE_ZEN_API_KEY` — the key for the
remote LLM provider (OpenCode Zen). The default `LITELLM_MASTER_KEY` is fine
for local use.

## 3. Start the stack

```bash
make up
```

`make up` loads `.env` and runs `podman-compose up -d --build`, starting three
services:

| Service | Port | Role |
|---------|------|------|
| `presidio-analyzer` | `:5002` | Detects PII in prompts |
| `presidio-anonymizer` | `:5001` | Masks the detected tokens |
| `litellm` | `:4000` | OpenAI-compatible proxy with the PII guardrail |

Just want to build the analyzer image without starting the stack? Use
`make build`.

## Next

Your stack is running. Now [configure OpenCode](./configure-opencode).