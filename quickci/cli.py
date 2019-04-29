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
@click.option("--show", "-s", is_flag=True, default=False,
              help="""Show current tokens""")
@click.option("--update", "-u", nargs=2, type=str,
              help="""Update existing tokens""")
@click.option("--create", "-c", is_flag=True, default=False,
              help="""Create empty config file""")
def config(show, update, create):
    """
    Create an empty configuration file, or retrieve and update tokens
    from an existing one.
    """
    conf = Config()
    if show:
        click.echo(conf.show())
    if create:
        if conf.check_file():
            click.echo("Configuration file already present in {}".format(conf.config_path))
            if not click.confirm("Do you really want to overwrite it?",
                                 prompt_suffix=" "):
                return 0
        click.echo("Creating empty config file in {}... ".format(conf.config_path), nl=False)
        conf.create()
        click.echo("Done.")
        click.echo("Please replace temporary tokens as needed.")
    if update:
        conf.update(update[0], update[1])
        conf.save()
        click.echo("Updated token for {}.".format(update[0]))

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
    conf = Config().parse()
    if travis:
        t = TravisCI(token=travis)
    else:
        t = TravisCI(token=conf["TRAVISCI_TOKEN"])
    if circle:
        c = CircleCI(token=circle)
    else:
        c = CircleCI(token=conf["CIRCLECI_TOKEN"])
    if appveyor:
        a = AppVeyor(token=appveyor)
    else:
        a = AppVeyor(token=conf["APPVEYOR_TOKEN"])
    if codeship:
        s = Codeship(token=codeship)
    else:
        s = Codeship(token=conf["CODESHIP_TOKEN"])
    if readthedocs:
        r = ReadTheDocs(token=readthedocs)
    else:
        r = ReadTheDocs(token=conf["RTD_TOKEN"])

    click.secho("CircleCI", bold=True, fg="blue")
    for el in c.status():
        click.secho("\t{} -> {}".format(el[0], el[1]), fg=c.colours[el[1]])
    click.secho("Travis CI", bold=True, fg="blue")
    for el in t.status():
        click.secho("\t{} -> {}".format(el[0], el[1]), fg=t.colours[el[1]])

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
