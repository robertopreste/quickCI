#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import click
from quickci.classes import Config


@click.group()
@click.pass_context
def config(ctx):
    """Create or update the configuration file."""
    ctx.obj = Config()
    pass


@config.command(short_help="Show the config file.")
@click.pass_obj
def show(obj):
    """Display the content of the configuration file."""
    if obj.temporary:
        click.secho("This is a temporary config file. Please create a "
                    "proper config file using `quickci config create`.",
                    fg="red")
    click.echo(obj.show())
    return 0


@config.command(short_help="Create a new config file.")
@click.pass_obj
def create(obj):
    """Create a new configuration file or overwrite an existing one."""
    if obj.check_file():
        click.echo(f"Configuration file already present in {obj.config_path}")
        if not click.confirm("Do you really want to overwrite it?",
                             prompt_suffix=" "):
            click.echo("Exiting.")
            return 0
    click.echo(f"Creating empty config file in {obj.config_path}... ", nl=False)
    obj.create()
    click.echo("Done.")
    click.echo("Please replace temporary tokens as needed.")
    return 0


@config.command(short_help="Update a specific token.")
@click.argument("service", type=click.Choice(["travis", "circle", "appveyor",
                                              "buddy"]))
@click.argument("token", type=str)
@click.pass_obj
def update(obj, service, token):
    """Update a specific service token in the configuration file."""
    obj.update(service, token)
    obj.save()
    click.echo(f"Updated token for {service}.")
    return 0



