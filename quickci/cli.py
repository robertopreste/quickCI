#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import sys
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, GitLab, \
    Codeship, ReadTheDocs


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
    Create or update the configuration file.
    """
    conf = Config()
    if show:
        click.echo(conf.show())
    if create:
        if conf.check_file():
            click.echo(f"Configuration file already present in {conf.config_path}")
            if not click.confirm("Do you really want to overwrite it?",
                                 prompt_suffix=" "):
                return 0
        click.echo(f"Creating empty config file in {conf.config_path}... ",
                   nl=False)
        conf.create()
        click.echo("Done.")
        click.echo("Please replace temporary tokens as needed.")
    if update:
        conf.update(update[0], update[1])
        conf.save()
        click.echo(f"Updated token for {update[0]}.")

    return 0


@main.command()
@click.option("--travis", "-t", help="""TravisCI auth token""")
@click.option("--circle", "-c", help="""CircleCI auth token""")
@click.option("--appveyor", "-a", help="""AppVeyor auth token""")
@click.option("--gitlab", "-g", nargs=2, type=str,
              help="""GitLab auth token and username""")
@click.option("--codeship", "-s", help="""Codeship auth token""")
def status(travis, circle, appveyor, gitlab, codeship):
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
    if gitlab:
        g = GitLab(token=gitlab[0], username=gitlab[1])
    else:
        g = GitLab(token=conf["GITLABCI_TOKEN"],
                   username=conf["GITLABCI_USER"])
    if codeship:
        s = Codeship(token=codeship)
    else:
        s = Codeship(token=conf["CODESHIP_TOKEN"])

    click.secho("CircleCI", bold=True, fg="blue")
    for el in c.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=c.colours[el[1]])
    click.secho("Travis CI", bold=True, fg="blue")
    for el in t.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=t.colours[el[1]])
    click.secho("AppVeyor", bold=True, fg="blue")
    for el in a.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=a.colours[el[1]])

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
