#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import pytest
from click.testing import CliRunner
from quickci import cli


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Have a quick look at the status of CI" in result.output
    assert "Show this message and exit." in result.output


def test_cli_help():
    """Test the CLI help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--help"])
    assert result.exit_code == 0
    assert "Have a quick look at the status of CI" in result.output
    assert "Show this message and exit." in result.output


def test_cli_config():
    """Test the config command group."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["config"])
    assert result.exit_code == 0
    assert "config [OPTIONS] COMMAND [ARGS]" in result.output
    assert "Show this message and exit." in result.output


def test_cli_config_help():
    """Test the config command group help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["config", "--help"])
    assert result.exit_code == 0
    assert "config [OPTIONS] COMMAND [ARGS]" in result.output
    assert "Show this message and exit." in result.output


def test_cli_config_show():
    """Test the config show command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["config", "show"])
    assert result.exit_code == 0
    assert "APPVEYOR_TOKEN" in result.output
    assert "BUDDY_TOKEN" in result.output
    assert "CIRCLECI_TOKEN" in result.output
    assert "TRAVISCI_TOKEN" in result.output
    assert "DRONE_TOKEN" in result.output


def test_cli_status():
    """Test the status command group."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status"])
    assert result.exit_code == 0
    assert "Travis CI" in result.output
    assert "CircleCI" in result.output
    assert "AppVeyor" in result.output
    assert "Buddy" in result.output
    assert "Drone" in result.output


def test_cli_status_help():
    """Test the status command group help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "--help"])
    assert result.exit_code == 0
    assert "appveyor" in result.output
    assert "buddy" in result.output
    assert "circle" in result.output
    assert "travis" in result.output
    assert "drone" in result.output
    assert "Show this message and exit." in result.output


def test_cli_status_travis():
    """Test the status travis command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "travis"])
    assert result.exit_code == 0
    assert "Travis CI" in result.output


def test_cli_status_circle():
    """Test the status circle command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "circle"])
    assert result.exit_code == 0
    assert "CircleCI" in result.output


def test_cli_status_appveyor():
    """Test the status appveyor command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "appveyor"])
    assert result.exit_code == 0
    assert "AppVeyor" in result.output


def test_cli_status_buddy():
    """Test the status buddy command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "buddy"])
    assert result.exit_code == 0
    assert "Buddy" in result.output


def test_cli_status_drone():
    """Test the status drone command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["status", "drone"])
    assert result.exit_code == 0
    assert "Drone CI" in result.output
