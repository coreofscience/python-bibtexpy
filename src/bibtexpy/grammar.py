import pyparsing as pp
from bibtexpy.models import BibContext, Macro, Concat, String, Entry

LCURLY, RCURLY, LPAREN, RPAREN, HASH, QUOTE, EQ, AT, COMMA = map(
    pp.Suppress, '{}()#"=@,'
)


def join(tokens):
    return "".join(tokens)


def bracketed(expr):
    return (LCURLY + expr + RCURLY) | (LPAREN + expr + RPAREN)


# These symbols are allowed in bibtex keys
_name_symbols = "!$&*+-./:;<>?[]^_`|"

_esc_curly = pp.Literal(r"\{") | pp.Literal(r"\}")
_esc_quote = pp.Suppress("\\") + '"'
_no_curly = pp.Regex(r"[^{}]")
_no_quote_curly = pp.Regex(r'[^"{}]')

# Curly string can be something like {bib{Tex}}
keep_curly_string = pp.Forward()
curly_item = (keep_curly_string | _esc_curly | _no_curly).leaveWhitespace()
keep_curly_string << "{" + pp.ZeroOrMore(curly_item).setParseAction(join) + "}"
# Remove external curlies, leave inner ones for latex just in case
curly_string = keep_curly_string.copy().setParseAction(lambda t: t[1:-1])


# Quoted string shoulde be something like "hello {world}"
quoted_string = pp.Forward()
quoted_item = (
    keep_curly_string | _esc_quote | _esc_curly | _no_quote_curly
).leaveWhitespace()
quoted_string << QUOTE + pp.ZeroOrMore(quoted_item).setParseAction(join) + QUOTE

# Numbers can stand alone
number = pp.Word(pp.nums)

# Macros are case insensitive, they are wrapped so we can reslove them later
macro = pp.Word(pp.alphas, pp.alphanums + _name_symbols).setParseAction(
    lambda t: Macro(t[0].lower())
)

# String concatenation is available for quoted strings and macros
concat_operand = number | macro | quoted_string | curly_string
concat_string = (concat_operand + pp.ZeroOrMore(HASH + concat_operand)).setParseAction(
    lambda t: Concat(t.asList())
)

# Field value can be a concat (including number) or quoted string
field_name = pp.Word(pp.alphas, pp.alphanums + _name_symbols)
field_value = concat_string.copy()
field = (
    field_name.setResultsName("name") + EQ + field_value.setResultsName("value")
).setParseAction(lambda t: String(*t.asList()))


# Comment
comment = AT + pp.CaselessLiteral("comment") + pp.restOfLine

# Preamble
preamble = AT + pp.CaselessLiteral("preamble") + bracketed(concat_string)

# String
string = AT + pp.Suppress(pp.CaselessLiteral("string")) + bracketed(field)

# Entry
entry_type = field_name.copy()
entry_key = pp.Word(pp.alphanums + _name_symbols)
entry_content = pp.Group(pp.ZeroOrMore(field + COMMA) + pp.Optional(field))
entry = (
    AT
    + entry_type("type")
    + bracketed(entry_key("key") + COMMA + entry_content("content"))
).setParseAction(lambda t: Entry(*t.asList()))

# Bib file
bib = pp.ZeroOrMore(
    pp.Suppress(comment) | pp.Suppress(preamble) | string | entry
).setParseAction(BibContext)


if __name__ == "__main__":
    with open("./scratch/sample.bib") as bibfile:
        data = bibfile.read()
        (result,) = bib.parseString(data, parseAll=True)
        print(result.__repr__())