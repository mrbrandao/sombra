"""Tests for the Sombra Brazilian recognizers."""

import pytest

from sombra.sombra_recog import (
    AddressRecognizer,
    CepRecognizer,
    CnpjRecognizer,
    CpfRecognizer,
)


@pytest.fixture
def cpf():
    return CpfRecognizer()


@pytest.fixture
def cep():
    return CepRecognizer()


@pytest.fixture
def cnpj():
    return CnpjRecognizer()


@pytest.fixture
def address():
    return AddressRecognizer()


def _first_match(recognizer, text, entity):
    results = recognizer.analyze(text=text, entities=[entity])
    assert len(results) == 1, f"expected one match, got {len(results)}: {results}"
    return results[0]


def _best_match(recognizer, text, entity):
    """Return the highest-confidence match among overlapping candidates."""
    results = recognizer.analyze(text=text, entities=[entity])
    assert results, f"expected at least one match for {text!r}"
    return max(results, key=lambda r: r.score)


def _assert_span(result, text, expected):
    start = text.find(expected)
    assert start != -1, f"substring {expected!r} not found in {text!r}"
    assert result.start == start, f"start {result.start} != {start}"
    assert result.end == start + len(expected), f"end {result.end} != {start + len(expected)}"


class TestCpf:
    def test_formatted(self, cpf):
        text = "Meu CPF é 123.456.789-00."
        result = _first_match(cpf, text, CpfRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CPF"
        assert result.score == 0.95
        _assert_span(result, text, "123.456.789-00")

    def test_unformatted(self, cpf):
        text = "CPF 12345678900"
        result = _first_match(cpf, text, CpfRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CPF"
        assert result.score == 0.50
        _assert_span(result, text, "12345678900")

    def test_no_match_on_plain_text(self, cpf):
        assert cpf.analyze(text="Bom dia, tudo bem?", entities=[CpfRecognizer.ENTITY]) == []


class TestCep:
    def test_formatted(self, cep):
        text = "Meu CEP é 80000-000."
        result = _first_match(cep, text, CepRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CEP"
        assert result.score == 0.95
        _assert_span(result, text, "80000-000")

    def test_unformatted(self, cep):
        text = "CEP 80000000"
        result = _first_match(cep, text, CepRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CEP"
        assert result.score == 0.50
        _assert_span(result, text, "80000000")

    def test_no_match_on_plain_text(self, cep):
        assert cep.analyze(text="Qualquer coisa.", entities=[CepRecognizer.ENTITY]) == []


class TestCnpj:
    def test_formatted(self, cnpj):
        text = "O CNPJ da empresa é 12.345.678/0001-90."
        result = _first_match(cnpj, text, CnpjRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CNPJ"
        assert result.score == 0.95
        _assert_span(result, text, "12.345.678/0001-90")

    def test_unformatted(self, cnpj):
        text = "CNPJ 12345678000190"
        result = _first_match(cnpj, text, CnpjRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_CNPJ"
        assert result.score == 0.50
        _assert_span(result, text, "12345678000190")

    def test_no_match_on_plain_text(self, cnpj):
        assert cnpj.analyze(text="Texto qualquer.", entities=[CnpjRecognizer.ENTITY]) == []


class TestAddress:
    def test_street_with_number(self, address):
        text = "Moro na Rua das Flores, 123."
        result = _best_match(address, text, AddressRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_ADDRESS"
        assert result.score == 0.75
        _assert_span(result, text, "Rua das Flores, 123")

    def test_avenue_abbreviated_with_property(self, address):
        text = "Av. Brasil 1000, casa 2"
        result = _best_match(address, text, AddressRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_ADDRESS"
        assert result.score == 0.75
        _assert_span(result, text, "Av. Brasil 1000")

    def test_property_unit_without_street_type(self, address):
        text = "o complemento é casa 12"
        result = _best_match(address, text, AddressRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_ADDRESS"
        assert result.score == 0.60
        _assert_span(result, text, "casa 12")

    def test_street_name_without_number(self, address):
        text = "moro na Rua dos Pinheiros"
        result = _best_match(address, text, AddressRecognizer.ENTITY)
        assert result.entity_type == "SOMBRA_ADDRESS"
        assert result.score == 0.40
        _assert_span(result, text, "Rua dos Pinheiros")

    def test_no_match_on_plain_text(self, address):
        assert address.analyze(text="Hoje está chovendo muito.", entities=[AddressRecognizer.ENTITY]) == []