# bibtexpy

A simple library with full support for bibtex.

## Grammar

We support the following grammar for bibtex:

```
quoted-string ::= "\"" non-quote "\""
curly-string ::= "{" non-quote "}"
expression ::= (quoted-string | ident) [ "#" (quoted-string | ident ]...
tag ::= ident "=" expression | curly-string
key ::= ident
type ::= ident
string ::= "@string" "{" tag, [tag "," ]... tag ,?
comment ::= "@comment" curly-string
entry ::= "@" type "{" key "," tag "," [tag "," ]... tag ","? "}"
bibtex ::= string? comment? entry...
```

