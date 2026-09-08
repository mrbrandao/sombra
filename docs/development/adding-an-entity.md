# Adding an entity

How to add a new Brazilian entity to Sombra.

## The four steps

1. **Add a `PatternRecognizer` subclass** in `src/sombra/sombra_recog.py`.
2. **Add a matching YAML block** in `containers/sombra_recognizers.yaml`.
3. **Write tests** in `src/sombra/tests/`.
4. **Add the entity** to the guardrail's `pii_entities_config` in
   `config.yaml`.

## Example

Adding a recognizer for a fictitious `SOMBRA_EMAIL_BR` entity:

```python
from presidio_analyzer import Pattern, PatternRecognizer


class BrEmailRecognizer(PatternRecognizer):
    ENTITY = "SOMBRA_EMAIL_BR"

    PATTERNS = [
        Pattern("BR e-mail", r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", 0.90),
    ]

    CONTEXT = ["e-mail", "email", "correio eletrônico"]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="BrEmailRecognizer",
            supported_language="pt",
        )
```

```yaml
  - name: "Sombra BR e-mail recognizer"
    supported_language: "pt"
    patterns:
      - name: "BR e-mail"
        regex: "\\b[\\w.+-]+@[\\w-]+\\.[\\w.]+\\b"
        score: 0.90
    context: [e-mail, email, correio eletrônico]
    supported_entity: "SOMBRA_EMAIL_BR"
```

Then add the entity to `pii_entities_config` in `config.yaml`:

```yaml
pii_entities_config:
  SOMBRA_EMAIL_BR: "MASK"
```

## Verify

```bash
make test            # run the recognizer test suite
make test-call       # hit the analyzer with a sample prompt
```

## Next

Write tests following the patterns in [Testing](./testing).