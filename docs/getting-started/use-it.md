# Use it

Try Sombra for real inside OpenCode.

## Prerequisites

- Stack running: `make up`
- `.env` sourced in your shell

```bash
set -a; source .env; set +a
```

## 1. Start OpenCode

Launch OpenCode in interactive mode:

```bash
opencode
```

## 2. Confirm the Sombra model

In the OpenCode TUI, open the model selector (usually via the model menu /
`/models`). You should see **Sombra - DeepSeek v4 Flash (PII Protected)** —
the local proxy model configured in `opencode.json`. Select it.

From the CLI you can verify the model is registered too:

```bash
opencode models
```

Look for `litellm-proxy/opencode-zen/deepseek-v4-flash`.

## 3. Try these prompts

Each prompt below is deliberately seeded with Brazilian PII. Paste one and
send it — the prompt travels OpenCode → LiteLLM → Presidio → masked remote
provider:

| Prompt |
|--------|
| `Consult my order in the name of João, CPF 123.456.789-00, living in Curitiba, CEP 80000-000.` |
| `Meu CPF é 123.456.789-00. Qual o status do meu pedido?` |
| `A empresa CNPJ 12.345.678/0001-90, na Rua das Flores, 123, precisa de uma nota fiscal.` |
| `E-mail para contato: joao.silva@example.com, telefone (41) 99999-0000.` |

The answers come back normal — the masking happens silently, before the
request leaves your machine.

## 4. Watch the masking happen in real time

Open a **second terminal** and follow the stack logs:

```bash
make logs
```

Now go back to OpenCode and send another prompt from the table above. Watch
the LiteLLM log lines stream by. You'll see the guardrail fire in `pre_call`
mode and the prompt reach the provider **already masked**:

```
"content": "Consult my order in the name of João, CPF <SOMBRA_CPF>, living in Curitiba, CEP <SOMBRA_CEP>."
```

The raw values (`123.456.789-00`, `80000-000`) never appear in the outgoing
request.

## 5. Where to see your messages

`make logs` shows the captured, masked version of every message your client
sends — this is the exact payload that hits the remote provider. If you ever
want to confirm what's being sent and what's been masked, this log stream is
the single source of truth.

For deeper per-request detail, restart the stack with `LITELLM_LOG=DEBUG`:

```bash
LITELLM_LOG=DEBUG make up
make logs
```

## Next

Want to know how it all fits together? See the [Architecture](../concepts/architecture).