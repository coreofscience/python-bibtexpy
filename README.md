# bibtexpy

A simple library with full support for bibtex.

## Grammar

We support the following grammar for bibtex:

![Railroad](./docs/railroad.png)

In summary we support:

- enclosing blocks with curlies or brackets.
- quoted and curlied strings, inner curlies are left to be processed by LaTeX.
- concatenation between numbers, macros, and strings.
- quote scaping inside quoted strings.
- `comment`, `string` and `preamble` blocks.

We don't support savage things like:

- Implicit comments.
- Operations with undefined macros.
- Circular references on macros.

As a couple of notes:

- `comment` and `preamble` blocks are ignored from the get go.
- `preamble` blocks may only contain a valid string concatenation.

