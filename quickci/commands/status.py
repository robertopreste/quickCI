#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
from quickci.classes import Config, TravisCI, CircleCI, AppVeyor, Buddy, DroneCI


@click.group(invoke_without_command=True)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_context
def status(ctx, branch, repo):
    """Return the status of the given branch of each project in each CI."""
    ctx.obj = Config()

    if ctx.invoked_subcommand is None:
        ctx.invoke(travis, branch=branch, repo=repo)
        ctx.invoke(circle, branch=branch, repo=repo)
        ctx.invoke(appveyor, branch=branch, repo=repo)
        ctx.invoke(buddy, branch=branch, repo=repo)
        ctx.invoke(drone, branch=branch, repo=repo)
    pass


@status.command(short_help="Show status of Travis CI projects.")
@click.option("--token", "-t", help="Travis CI auth token", default=None)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_obj
def travis(obj, token, branch, repo):
    """Return the status of the given branch of each project in Travis CI."""
    ci = TravisCI(token=token, branch=branch, repo=repo) \
        if token else TravisCI(token=obj["travis"], branch=branch, repo=repo)
    click.secho(f"Travis CI ({branch} branch)", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of CircleCI projects.")
@click.option("--token", "-t", help="CircleCI auth token", default=None)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_obj
def circle(obj, token, branch, repo):
    """Return the status of the given branch of each project in CircleCI."""
    ci = CircleCI(token=token, branch=branch, repo=repo) \
        if token else CircleCI(token=obj["circle"], branch=branch, repo=repo)
    click.secho(f"CircleCI ({branch} branch)", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of AppVeyor projects.")
@click.option("--token", "-t", help="AppVeyor auth token", default=None)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_obj
def appveyor(obj, token, branch, repo):
    """Return the status of the given branch of each project in AppVeyor."""
    ci = AppVeyor(token=token, branch=branch, repo=repo) \
        if token else AppVeyor(token=obj["appveyor"], branch=branch, repo=repo)
    click.secho(f"AppVeyor ({branch} branch)", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of Buddy projects.")
@click.option("--token", "-t", help="Buddy auth token", default=None)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_obj
def buddy(obj, token, branch, repo):
    """Return the status of the given branch of each project in Buddy."""
    ci = Buddy(token=token, branch=branch, repo=repo) \
        if token else Buddy(token=obj["buddy"], branch=branch, repo=repo)
    click.secho(f"Buddy ({branch} branch)", bold=True, fg="blue")
    ci.status()
    return 0


@status.command(short_help="Show status of Drone CI projects.")
@click.option("--token", "-t", help="Drone CI auth token", default=None)
@click.option("--branch", "-b", help="Branch to check", default="master")
@click.option("--repo", "-r", help="Repo to check", default=None)
@click.pass_obj
def drone(obj, token, branch, repo):
    """Return the status of the given branch of each project in Drone CI."""
    ci = DroneCI(token=token, branch=branch, repo=repo) \
        if token else DroneCI(token=obj["drone"], branch=branch, repo=repo)
    click.secho(f"Drone CI ({branch} branch)", bold=True, fg="blue")
    ci.status()
    return 0
