# What Sombra detects

Sombra **extends** Presidio's default recognizers. Everything Presidio already
detects keeps working — names via spaCy NER, e-mails, phone numbers, URLs,
locations — and Sombra adds the Brazilian patterns that are missing:

| Entity           | Example                  | Confidence |
|------------------|--------------------------|------------|
| `SOMBRA_CPF`     | `123.456.789-00`         | 0.95 (1.00 with context) |
| `SOMBRA_CEP`     | `80000-000`              | 0.95       |
| `SOMBRA_CNPJ`    | `12.345.678/0001-90`     | 0.95       |
| `SOMBRA_ADDRESS` | `Rua das Flores, 123`    | 0.75       |
| `PERSON`         | `João` (spaCy NER)       | 0.85       |
| `LOCATION`       | `Curitiba` (spaCy NER)   | 0.85       |

`PERSON` and `LOCATION` come from Presidio's built-in spaCy NER. The
`SOMBRA_*` entities are Sombra's own pattern-based recognizers.

## How masking looks

Detected tokens are replaced by masks in the anonymizer, e.g.:

```
Consult my order in the name of João, CPF <SOMBRA_CPF>, living in Curitiba, CEP <SOMBRA_CEP>.
```

## Next

Building on this stack? Head to [Make targets](../reference/make-targets) or
the [Development](../development/recognizers) section to add your own
entities.