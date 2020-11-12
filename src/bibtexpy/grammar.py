import pyparsing as pp
from bibtexpy.models import BibContext, Macro, Concat, MacroDefinition, Entry

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
keep_curly_string.setName("keep_curly_string")
# Remove external curlies, leave inner ones for latex just in case
curly_string = (
    keep_curly_string.copy().setParseAction(lambda t: t[1:-1]).setName("curly_string")
)


# Quoted string shoulde be something like "hello {world}"
quoted_string = pp.Forward()
quoted_item = (
    keep_curly_string | _esc_quote | _esc_curly | _no_quote_curly
).leaveWhitespace()
quoted_string << QUOTE + pp.ZeroOrMore(quoted_item).setParseAction(join) + QUOTE
quoted_string.setName("quote_string")

# Numbers can stand alone
number = pp.Word(pp.nums).setName("number")

# Macros are case insensitive, they are wrapped so we can reslove them later
macro = (
    pp.Word(pp.alphas, pp.alphanums + _name_symbols)
    .setParseAction(lambda t: Macro(t[0].lower()))
    .setName("macro")
)

# String concatenation is available for quoted strings and macros
concat_operand = number | macro | quoted_string | curly_string
concat_operand.setName("concat_operand")
concat_string = (
    (concat_operand + pp.ZeroOrMore((HASH + concat_operand).setName("concat")))
    .setParseAction(lambda t: Concat(t.asList()))
    .setName("concat_string")
)

# Field value can be a concat (including number) or quoted string
field_name = pp.Word(pp.alphas, pp.alphanums + _name_symbols).setName("name")
field_value = concat_string.copy().setName("value")
field = (
    (field_name.setResultsName("name") + EQ + field_value.setResultsName("value"))
    .setParseAction(lambda t: MacroDefinition(*t.asList()))
    .setName("macro_definition")
)


# Comment
comment = AT + pp.CaselessLiteral("comment") + pp.restOfLine
comment.setName("comment")

# Preamble
preamble = AT + pp.CaselessLiteral("preamble") + bracketed(concat_string)
preamble.setName("preamble")

# String
string = AT + pp.Suppress(pp.CaselessLiteral("string")) + bracketed(field)
string.setName("string")

# Entry
entry_type = field_name.copy()
entry_key = pp.Word(pp.alphanums + _name_symbols)
entry_fields = pp.Group(pp.ZeroOrMore(field + COMMA) + pp.Optional(field)).setName(
    "entry_fields"
)
entry_content = (entry_key("key") + COMMA + entry_fields).setName("entry_content")
entry = (
    (AT + entry_type("type") + bracketed(entry_content))
    .setParseAction(lambda t: Entry(*t.asList()))
    .setName("entry")
)

# Bib file
bibtex = (
    pp.ZeroOrMore(pp.Suppress(comment) | pp.Suppress(preamble) | string | entry)
    .setParseAction(lambda t: BibContext(t.asList()))
    .setName("bibtex")
)


if __name__ == "__main__":
    with open("./scratch/sample.bib") as bibfile:
        data = bibfile.read()
        (result,) = bibtex.parseString(data, parseAll=True)
        print(result.__repr__())