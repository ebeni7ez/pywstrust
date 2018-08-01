# -*- coding: utf-8 -*-

"""Console script for pywstrust."""
import sys
import click

from pywstrust.pywstrust import get_token


def get_saml_token(username, password, base_url, realm):
    return get_token(username, password, base_url, realm)


@click.command()
def main(args=None):
    """Console script for pywstrust."""
    click.echo("Replace this message by putting your code into "
               "pywstrust.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
