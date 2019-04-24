#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import sys
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, Codeship, \
    ReadTheDocs


@click.group()
@click.version_option()
def main():
    pass


@main.command()
def config():
    """
    Create the config file.
    """
    c = Config()
    click.echo("Creating config file in {}...".format(c.config_path))
    c.create()
    click.echo("Done. Please replace temp tokens as needed.")

    return 0


@main.command()
@click.option("--travis", "-t", help="""TravisCI auth token""")
@click.option("--circle", "-c", help="""CircleCI auth token""")
@click.option("--appveyor", "-a", help="""AppVeyor auth token""")
@click.option("--codeship", "-s", help="""Codeship auth token""")
@click.option("--readthedocs", "-r", help="""ReadTheDocs auth token""")
def status(travis, circle, appveyor, codeship, readthedocs):
    """
    Return the status of the master branch of each project in each CI.
    """
    conf_tokens = Config().parse()
    if travis:
        t = TravisCI(token=travis)
    else:
        t = TravisCI(token=conf_tokens["TRAVISCI_TOKEN"])
    if circle:
        c = CircleCI(token=circle)
    else:
        c = CircleCI(token=conf_tokens["CIRCLECI_TOKEN"])
    if appveyor:
        a = AppVeyor(token=appveyor)
    else:
        a = AppVeyor(token=conf_tokens["APPVEYOR_TOKEN"])
    if codeship:
        s = Codeship(token=codeship)
    else:
        s = Codeship(token=conf_tokens["CODESHIP_TOKEN"])
    if readthedocs:
        r = ReadTheDocs(token=readthedocs)
    else:
        r = ReadTheDocs(token=conf_tokens["RTD_TOKEN"])
    # click.echo(t.get_user_info())
    # click.echo(t.get_builds())
    # click.echo(c.get_user_info())
    # click.echo(c.projects())
    click.secho("CircleCI", bold=True, fg="blue")
    for el in c.status():
        click.secho("\t{} -> {}".format(el[0], el[1]), fg=c.colours[el[1]])
    click.secho("Travis CI", bold=True, fg="blue")
    for el in t.status():
        click.secho("\t{} -> {}".format(el[0], el[1]), fg=t.colours[el[1]])

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
