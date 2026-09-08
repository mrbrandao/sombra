# Make targets

Every operation you need, in one table.

| Target | What it does |
|--------|--------------|
| `make help` | Print the full list of targets |
| `make up` | Load `.env`, then `podman-compose up -d --build` (start the stack) |
| `make down` | Stop the stack |
| `make build` | Build the analyzer image only (no run) |
| `make logs` | Follow the stack logs |
| `make test` | Run the recognizer test suite (`uv run pytest`) |
| `make call-analyzer` | Call the Presidio analyzer directly (`:5002`) |
| `make call-litellm` | Call the LiteLLM proxy (`:4000`) — full masking path |
| `make test-call` | Run both curl examples sequentially |
| `make docs-deps` | Install the docs tooling (`npm install`) |
| `make docs-build` | Build the static documentation site |
| `make docs-serve` | Start the VitePress dev server (`:5173`) |
| `make docs-preview` | Preview the built docs site |
| `make docs-clean` | Remove build artifacts |
| `make docs-check` | Strict docs build — fails on warnings |

## Notes

- `make up` and `make build` print help and exit if `.env` is missing or
  unsourced.
- `make call-litellm` needs `.env` sourced so `LITELLM_MASTER_KEY` is in your
  shell.

## Next

Ready to extend Sombra? See [Recognizers](../development/recognizers).