"""Brazilian PII recognizers for the Presidio Analyzer.

Sombra is an extension for Presidio: it adds pattern-based recognizers for
Brazilian entities that the default recognizer set does not cover — CPF, CEP,
CNPJ and street addresses. Presidio's default recognizers, including PERSON
names detected by the spaCy NER model, keep working unchanged; Sombra only
adds what is missing for Brazilian data.

The recognizers follow Presidio's best practices (see
https://presidio.dataprivacystack.org/analyzer/developing_recognizers/): each
one is a :class:`PatternRecognizer` subclass that pairs regular expressions
with *context* words, which raise the final confidence when a relevant keyword
appears near the match. Performance stays within Presidio's ~100 ms per
100 tokens guidance since these are pure regex recognizers.
"""

from presidio_analyzer import Pattern, PatternRecognizer

#: Street type markers commonly found in Brazilian addresses.
STREET_TYPES = (
    r"(?:avenida|av\.|rua|alameda|travessa|estrada|rodovia|praça|praca|"
    r"beco|viela|ladeira|vila|passagem|acesso|servidão|servidao)"
)

#: Property unit markers commonly found in Brazilian addresses.
PROPERTY_MARKERS = (
    r"(?:casa|sobrado|apartamento|apto\.?|lote|quadra|bloco|complemento|"
    r"fundos|andar|galpão|galpao|kitnet|cobertura|salão|salao)"
)

#: Characters allowed inside a street name.
_STREET_NAME_CHARS = r"[A-Za-zÀ-ÿ0-9''.,\/ºª\- ]"


def _build_pattern(name: str, regex: str, score: float) -> Pattern:
    """Build a named Presidio pattern."""
    return Pattern(name=name, regex=regex, score=score)


class CpfRecognizer(PatternRecognizer):
    """Detect Brazilian CPF numbers.

    A CPF (Cadastro de Pessoas Físicas) is the individual taxpayer
    identifier: an 11-digit number usually formatted as ``xxx.xxx.xxx-xx``.
    """

    ENTITY = "SOMBRA_CPF"

    PATTERNS = [
        _build_pattern("CPF formatted", r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", 0.95),
        _build_pattern("CPF unformatted", r"\b\d{11}\b", 0.50),
    ]

    CONTEXT = [
        "cpf",
        "documento",
        "inscrição",
        "inscricao",
        "cadastro de pessoa física",
        "registro",
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="CpfRecognizer",
            supported_language="pt",
        )


class CepRecognizer(PatternRecognizer):
    """Detect Brazilian postal codes (CEP).

    A CEP (Código de Endereçamento Postal) is an 8-digit postal code usually
    formatted as ``xxxxx-xxx``.
    """

    ENTITY = "SOMBRA_CEP"

    PATTERNS = [
        _build_pattern("CEP formatted", r"\b\d{5}-\d{3}\b", 0.95),
        _build_pattern("CEP unformatted", r"\b\d{8}\b", 0.50),
    ]

    CONTEXT = ["cep", "código postal", "codigo postal", "endereço", "endereco"]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="CepRecognizer",
            supported_language="pt",
        )


class CnpjRecognizer(PatternRecognizer):
    """Detect Brazilian company registry numbers (CNPJ).

    A CNPJ (Cadastro Nacional da Pessoa Jurídica) is a 14-digit number usually
    formatted as ``xx.xxx.xxx/xxxx-xx``.
    """

    ENTITY = "SOMBRA_CNPJ"

    PATTERNS = [
        _build_pattern("CNPJ formatted", r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", 0.95),
        _build_pattern("CNPJ unformatted", r"\b\d{14}\b", 0.50),
    ]

    CONTEXT = [
        "cnpj",
        "empresa",
        "inscrição estadual",
        "inscricao estadual",
        "cadastro nacional da pessoa jurídica",
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="CnpjRecognizer",
            supported_language="pt",
        )


class AddressRecognizer(PatternRecognizer):
    """Detect Brazilian street addresses.

    Covers street type + name + number (``Rua das Flores, 123``), property
    units (``casa 12``, ``apartamento 42``) and street type + name alone.
    Broad locations remain covered by spaCy's LOCATION entity; this recognizer
    fills the gap for formatted street addresses.
    """

    ENTITY = "SOMBRA_ADDRESS"

    PATTERNS = [
        _build_pattern(
            "Address with street type and number",
            (
                rf"\b{STREET_TYPES}\s+{_STREET_NAME_CHARS}+?"
                rf"\s*(?:n[º°]?\.?|número|numero|num\.?|n\.?)?\s*\d{{1,5}}\b"
            ),
            0.75,
        ),
        _build_pattern(
            "Property unit with number",
            rf"\b{PROPERTY_MARKERS}\s*(?:n[º°]?\.?|n\.?)?\s*\d{{1,5}}\b",
            0.60,
        ),
        _build_pattern(
            "Street type with name",
            rf"\b{STREET_TYPES}\s+{_STREET_NAME_CHARS}{{2,60}}\b",
            0.40,
        ),
    ]

    CONTEXT = [
        "endereço",
        "endereco",
        "rua",
        "avenida",
        "alameda",
        "travessa",
        "bairro",
        "cidade",
        "cep",
        "casa",
        "lote",
        "quadra",
        "apartamento",
        "condomínio",
        "condominio",
        "residência",
        "residencia",
        "complemento",
        "número",
        "numero",
        "address",
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity=self.ENTITY,
            patterns=self.PATTERNS,
            context=self.CONTEXT,
            name="AddressRecognizer",
            supported_language="pt",
        )


def build_recognizers():
    """Return a list of all Sombra recognizers ready to register."""
    return [
        CpfRecognizer(),
        CepRecognizer(),
        CnpjRecognizer(),
        AddressRecognizer(),
    ]