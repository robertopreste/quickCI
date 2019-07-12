#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, Buddy, DroneCI


@click.group(invoke_without_command=True)
@click.pass_context
def status(ctx):
    """Return the status of the master branch of each project in each CI."""
    ctx.obj = Config()

    if ctx.invoked_subcommand is None:
        ctx.invoke(travis)
        ctx.invoke(circle)
        ctx.invoke(appveyor)
        ctx.invoke(buddy)
        ctx.invoke(drone)
    pass


@status.command(short_help="Show status of Travis CI projects.")
@click.option("--token", "-t", help="Travis CI auth token", default=None)
@click.pass_obj
def travis(obj, token):
    """Return the status of the master branch of each project in Travis CI."""
    # if not token and obj["travis"] == "replace_me":
    #     click.secho("Please replace the default token with a valid one "
    #                 "using `quickci config update`, or provide one "
    #                 "directly using `--token`.", fg="red")
    #     return 1
    ci = TravisCI(token=token) if token else TravisCI(token=obj["travis"])
    click.secho("Travis CI", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of CircleCI projects.")
@click.option("--token", "-t", help="CircleCI auth token", default=None)
@click.pass_obj
def circle(obj, token):
    """Return the status of the master branch of each project in CircleCI."""
    # if not token and obj["circle"] == "replace_me":
    #     click.secho("Please replace the default token with a valid one "
    #                 "using `quickci config update`, or provide one "
    #                 "directly using `--token`.", fg="red")
    #     return 1
    ci = CircleCI(token=token) if token else CircleCI(token=obj["circle"])
    click.secho("CircleCI", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of AppVeyor projects.")
@click.option("--token", "-t", help="AppVeyor auth token", default=None)
@click.pass_obj
def appveyor(obj, token):
    """Return the status of the master branch of each project in AppVeyor."""
    # if not token and obj["appveyor"] == "replace_me":
    #     click.secho("Please replace the default token with a valid one "
    #                 "using `quickci config update`, or provide one "
    #                 "directly using `--token`.", fg="red")
    #     return 1
    ci = AppVeyor(token=token) if token else AppVeyor(token=obj["appveyor"])
    click.secho("AppVeyor", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of Buddy projects.")
@click.option("--token", "-t", help="Buddy auth token", default=None)
@click.pass_obj
def buddy(obj, token):
    """Return the status of the master branch of each project in Buddy."""
    # if not token and obj["buddy"] == "replace_me":
    #     click.secho("Please replace the default token with a valid one "
    #                 "using `quickci config update`, or provide one "
    #                 "directly using `--token`.", fg="red")
    #     return 1
    ci = Buddy(token=token) if token else Buddy(token=obj["buddy"])
    click.secho("Buddy", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of Drone CI projects.")
@click.option("--token", "-t", help="Drone CI auth token", default=None)
@click.pass_obj
def drone(obj, token):
    """Return the status of the latest build of each project in Drone CI."""
    ci = DroneCI(token=token) if token else DroneCI(token=obj["drone"])
    click.secho("Drone CI", bold=True, fg="blue")
    ci.status()
    return 0
