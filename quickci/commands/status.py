#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, Buddy


@click.group(invoke_without_command=True)
@click.pass_context
def status(ctx):
    """Return the status of the master branch of each project in each CI."""
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
    """Return the status of the master branch of each project in Travis CI."""
    ci = TravisCI(token=token) if token else TravisCI(token=obj["TRAVISCI_TOKEN"])
    click.secho("Travis CI", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of CircleCI projects.")
@click.option("--token", "-t", help="CircleCI auth token", default=None)
@click.pass_obj
def circle(obj, token):
    """Return the status of the master branch of each project in CircleCI."""
    ci = CircleCI(token=token) if token else CircleCI(token=obj["CIRCLECI_TOKEN"])
    click.secho("CircleCI", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of AppVeyor projects.")
@click.option("--token", "-t", help="AppVeyor auth token", default=None)
@click.pass_obj
def appveyor(obj, token):
    """Return the status of the master branch of each project in AppVeyor."""
    ci = AppVeyor(token=token) if token else AppVeyor(token=obj["APPVEYOR_TOKEN"])
    click.secho("AppVeyor", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of Buddy projects.")
@click.option("--token", "-t", help="Buddy auth token", default=None)
@click.pass_obj
def buddy(obj, token):
    """Return the status of the master branch of each project in Buddy."""
    ci = Buddy(token=token) if token else Buddy(token=obj["BUDDY_TOKEN"])
    click.secho("Buddy", bold=True, fg="blue")
    ci.status()
    return 0
