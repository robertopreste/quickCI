#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import sys
import click
from quickci.commands.config import config
from quickci.commands.status import status


@click.group()
@click.version_option()
def main():
    """Have a quick look at the status of CI projects from the command line."""
    pass


main.add_command(config)
main.add_command(status)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
