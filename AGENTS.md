# AGENTS.md

## Project Overview

**Sombra** is a local PII anonymization proxy + CLI pipeline. It intercepts traffic from agent/LLM CLIs (OpenCode, etc.) and masks sensitive data — especially Brazilian PII (CPF, CEP, names, e-mails, addresses) — in real time before it reaches a remote LLM provider (e.g., OpenCode Zen / DeepSeek v4 Flash). No sensitive data is persisted remotely.

## Source of Truth

- `spec.md` is the authoritative design document. It was originally written in Portuguese and has been translated to English; the user plans to extend it with more instructions. **Always read `spec.md` first** and keep changes aligned with it.
- Treat the spec's architecture as the target: the repo currently contains only `spec.md` and `LICENSE` — no code, config, or CI exists yet.

## Architecture (from spec)

```
OpenCode CLI → LiteLLM Proxy (:4000) → Presidio Analyzer (:5002) + Anonymizer (:5001) → remote LLM
```

- Components: LiteLLM proxy (OpenAI API-compatible, `master_key`, pre-call guardrails), custom Presidio Analyzer (spaCy `pt_core_news_lg` + PT-BR regex recognizers `BR_CPF`/`BR_CEP`), Presidio Anonymizer, rootless Podman containers.
- Key files planned: `docker-compose.yml`, `config.yaml` (LiteLLM), `opencode.json`, `presidio/Dockerfile`, `presidio/custom_br_recognizers.py`.

## Roadmap / Current Work

1. Bootstrap the system with organized settings (first deliverable in progress).
2. A **simple Go script** to deploy the environment as **quadlet containers under systemd** — this supersedes the `docker-compose.yml`/`podman-compose` approach described in the spec.

## Constraints

- Rootless Podman (no root privileges).
- Real-time masking with <150ms added latency per request; 100% masking of formatted e-mails/CPFs/CEPs in synthetic tests; zero unmasked PII may reach the remote provider.
- Do not commit unless explicitly asked.