#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, Buddy


@click.group(invoke_without_command=True)
@click.pass_context
def status(ctx):
    """
    Return the status of the master branch of each project in each CI.
    """
    ctx.obj = Config().parse()
    if ctx.invoked_subcommand is None:
        ctx.invoke(travis)
        ctx.invoke(circle)
        ctx.invoke(appveyor)
        ctx.invoke(buddy)
    pass


@status.command(short_help="Show status of Travis CI projects.")
@click.option("--token", "-t", help="Travis CI auth token", default=None)
@click.pass_obj
def travis(obj, token):
    """
    Return the status of the master branch of each project in Travis CI.
    """
    if token:
        res = TravisCI(token=token)
    else:
        res = TravisCI(token=obj["TRAVISCI_TOKEN"])
    click.secho("Travis CI", bold=True, fg="blue")
    for el in res.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=res.colours[el[1]])
    return 0


@status.command(short_help="Show status of CircleCI projects.")
@click.option("--token", "-t", help="CircleCI auth token", default=None)
@click.pass_obj
def circle(obj, token):
    """
    Return the status of the master branch of each project in CircleCI.
    """
    if token:
        res = CircleCI(token=token)
    else:
        res = CircleCI(token=obj["CIRCLECI_TOKEN"])
    click.secho("CircleCI", bold=True, fg="blue")
    for el in res.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=res.colours[el[1]])
    return 0


@status.command(short_help="Show status of AppVeyor projects.")
@click.option("--token", "-t", help="AppVeyor auth token", default=None)
@click.pass_obj
def appveyor(obj, token):
    """
    Return the status of the master branch of each project in AppVeyor.
    """
    if token:
        res = AppVeyor(token=token)
    else:
        res = AppVeyor(token=obj["APPVEYOR_TOKEN"])
    click.secho("AppVeyor", bold=True, fg="blue")
    for el in res.status():
        click.secho(f"\t{el[0]} -> {el[1]}", fg=res.colours[el[1]])
    return 0


@status.command(short_help="Show status of Buddy projects.")
@click.option("--token", "-t", help="Buddy auth token", default=None)
@click.pass_obj
def buddy(obj, token):
    """
    Return the status of the master branch of each project in Buddy.
    """
    if token:
        res = Buddy(token=token)
    else:
        res = Buddy(token=obj["BUDDY_TOKEN"])
    click.secho("Buddy", bold=True, fg="blue")
    for el in res.status():
        click.secho(f"\t{el[0]} ({el[1]} pipeline) -> {el[2].casefold()}",
                    fg=res.colours[el[2]])
    return 0
