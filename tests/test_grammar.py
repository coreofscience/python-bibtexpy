from pyparsing import ParseException
import pytest
from bibtexpy.grammar import (
    curly_string,
    quoted_string,
    concat_string,
    entry_field,
    string,
    entry,
    bibtex,
)
from bibtexpy.models import Concat, MacroDefinition, Macro, Field, Entry, BibContext

SAMPLE_STRINGS = [
    ('"es"', Concat(["es"])),
    ('es # una # "kiralina"', Concat([Macro("es"), Macro("una"), "kiralina"])),
    ("es # una # {kiralina}", Concat([Macro("es"), Macro("una"), "kiralina"])),
    ("1100 # una # {kiralina}", Concat(["1100", Macro("una"), "kiralina"])),
    ('"es"', Concat(["es"])),
]


@pytest.mark.parametrize(
    "value",
    [
        "hola que hace",
        'hola "que hace" hace',
        "hola que \\} hace",
        "hola que \\{ hace",
        'hola que " hace',
        '{biber} que " hace',
    ],
)
def test_curly_parsing(value):
    result = curly_string.parseString(f"{{{value}}}", parseAll=True)
    assert result.asList() == [value]


@pytest.mark.parametrize(
    "value",
    [
        r"hola que } hace",
        r"hola que { hace",
    ],
)
def test_curly_failing(value):
    # Non escaped curlies are not allwed on curly strings
    with pytest.raises(ParseException):
        curly_string.parseString(f"{{{value}}}", parseAll=True)


@pytest.mark.parametrize(
    "value",
    [
        "hola {que} hace",
        "hola que \\{hace",
        'hola que \\"hace',
    ],
)
def test_quoted_parsing(value):
    # Non escaped curlies are not allwed on curly strings
    result = quoted_string.parseString(f'"{value}"', parseAll=True)
    assert result.asList() == [value.replace('\\"', '"')]


@pytest.mark.parametrize("value, expected", SAMPLE_STRINGS)
def test_concat_strings(value, expected):
    (result,) = concat_string.parseString(value, parseAll=True)
    assert result == expected


@pytest.mark.parametrize("value, expected", SAMPLE_STRINGS)
def test_fields(value, expected):
    (result,) = entry_field.parseString(f"key = {value}", parseAll=True)
    assert result == Field("key", expected)


@pytest.mark.parametrize("value, expected", SAMPLE_STRINGS)
def test_macro_definitions(value, expected):
    (result,) = string.parseString(f"@string {{key = {value}}}", parseAll=True)
    assert result == MacroDefinition("key", expected)


@pytest.mark.parametrize("value, expected", SAMPLE_STRINGS)
def test_entries(value, expected):
    (result,) = entry.parseString(f"@article {{cite, key = {value}}}", parseAll=True)
    assert result == Entry("article", "cite", [Field("key", expected)])


@pytest.mark.parametrize(
    "value, expected",
    SAMPLE_STRINGS,
)
def test_bibtex_entries(value, expected):
    (result,) = bibtex.parseString(f"@article {{cite, key = {value}}}", parseAll=True)
    assert result == BibContext([Entry("article", "cite", [Field("key", expected)])])


@pytest.mark.parametrize(
    "value, expected",
    SAMPLE_STRINGS,
)
def test_bibtex_macros(value, expected):
    (result,) = bibtex.parseString(f"@string {{ key = {value}}}", parseAll=True)
    assert result == BibContext([MacroDefinition("key", expected)])