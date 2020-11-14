import click
from bibtexpy.grammar import bibtex


@click.group()
def main():
    """
    BibTex manipulation CLI.
    """


@main.command()
@click.option(
    "--input", "-i", "_input", help="input file", type=click.File(mode="r"), default="-"
)
@click.option(
    "--output", "-o", help="output file", type=click.File(mode="w"), default="-"
)
def parse(_input, output):
    """
    Build a syntax tree and print it back in latex form.
    """
    try:
        (tree,) = bibtex.parseFile(_input, parseAll=True)
        output.write(tree.latex())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()