# Testing

The recognizer test suite.

## Run the tests

```bash
make test
```

Runs `uv run pytest` against the tests in `src/sombra/tests/`.

## What the tests cover

- **Pattern matching** — each `SOMBRA_*` entity is matched against valid and
  invalid samples.
- **Context boosting** — confidence rises when a context word appears nearby.
- **Parity between code and YAML** — the same recognizer defined both ways
  behaves identically.

## Writing a new test

Follow the existing structure in `src/sombra/tests/`: build a recognizer, run
it over a sample text with `analyzer.analyze()`, and assert the expected
entity type and score threshold.

```python
def test_cpf_recognizer(analyzer):
    results = analyzer.analyze(
        text="Meu CPF é 123.456.789-00.",
        language="pt",
    )
    assert any(r.entity_type == "SOMBRA_CPF" for r in results)
    assert any(r.score >= 0.9 for r in results)
```

## Next

Ready to smoke-test the stack end to end? See [Quick tests](./quick-tests).