# Recognizers

How Sombra's recognizers are defined.

This section synthesizes the official Presidio guides — [Adding
recognizers](https://presidio.dataprivacystack.org/analyzer/adding_recognizers/)
and [Recognizer development best
practices](https://presidio.dataprivacystack.org/analyzer/developing_recognizers/)
— and shows how they apply to Sombra.

## Recognizer types

Presidio has three families of recognizers:

1. **Deny lists** — a fixed list of words to flag (e.g. titles like `Dr.`).
2. **Pattern-based** — regular expressions, optionally with *context* words
   that raise confidence when a keyword appears nearby. This is what Sombra
   uses.
3. **ML / rule-based** — spaCy, Stanza or Transformers NER models, or custom
   logic over NLP features. Sombra uses spaCy's `pt_core_news_lg` for
   `PERSON` and `LOCATION`.

## Best practices

- **Accuracy**: balance false positives and false negatives. Prefer *context*
  words to boost confidence instead of lowering scores.
- **Performance**: keep recognition under ~100 ms per 100 tokens. Pure regex
  recognizers easily satisfy this, keeping the overall <150 ms latency budget.
- **Environment**: don't let third-party dependencies interfere with
  Presidio's. Sombra only depends on the `regex` module.
- **Extend, don't replace**: register Sombra recognizers on top of the default
  set. The default recognizers and spaCy NER keep working unchanged.

## Two ways to define a recognizer

Recognizers can be defined in code (`PatternRecognizer` subclasses in
`src/sombra/sombra_recog.py`) or declaratively in YAML
(`containers/sombra_recognizers.yaml`). Both describe the same thing, and the
tests in `src/sombra/tests/` cover both.

### In code

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

### In YAML

The same recognizer in the container's registry YAML (loaded by the analyzer
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

## Next

Want to add a new Brazilian entity? See [Adding an entity](./adding-an-entity).