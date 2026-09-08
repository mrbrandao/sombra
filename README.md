<p align="center">
  <img src="docs/public/img/sombra.png" alt="Sombra" width="200"/>
</p>

# Sombra

**Sombra** (Portuguese for "shadow") is a local PII anonymization proxy for
agent and LLM CLIs. It intercepts traffic and masks sensitive Brazilian data —
CPF, CEP, CNPJ, street addresses, e-mails and names — in real time before it
reaches a remote LLM provider.

Zero sensitive data is persisted remotely.

## Quickstart

```bash
cp .env.example .env    # set your OPENCODE_ZEN_API_KEY
make up                 # start the stack (analyzer, anonymizer, litellm)
make call-analyzer      # verify PII detection
```

## Documentation

Full docs — install, configure OpenCode, architecture, and development —
live in the [docs site](docs/index.md). Run it locally with:

```bash
make docs-serve
```

## License

Apache-2.0 — see [LICENSE](LICENSE).