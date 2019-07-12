#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import pytest
from quickci.classes import Config
from quickci.classes import TravisCI, CircleCI, AppVeyor, Buddy, DroneCI


def test_config_temporary():
    """Test the Config class with temporary tokens."""
    config = Config()
    if config.check_file():
        assert not config.temporary
    else:
        assert config.temporary
        expect = {"TRAVISCI_TOKEN": "replace_me", "CIRCLECI_TOKEN": "replace_me",
                  "APPVEYOR_TOKEN": "replace_me", "BUDDY_TOKEN": "replace_me",
                  "DRONE_TOKEN": "replace_me"}
        result = config.content
        assert result == expect


def test_status_travis(capsys):
    """Test the Travis.status() function with temporary token."""
    t = TravisCI()
    expect = ("Please replace the default token with a valid one using " 
              "`quickci config update`, or provide one directly "
              "using `--token`.")
    t.status()
    result = capsys.readouterr()
    assert result.out.strip() == expect


def test_status_circle(capsys):
    """Test the Travis.status() function with temporary token."""
    c = CircleCI()
    expect = ("Please replace the default token with a valid one using " 
              "`quickci config update`, or provide one directly "
              "using `--token`.")
    c.status()
    result = capsys.readouterr()
    assert result.out.strip() == expect


def test_status_appveyor(capsys):
    """Test the Travis.status() function with temporary token."""
    a = AppVeyor()
    expect = ("Please replace the default token with a valid one using " 
              "`quickci config update`, or provide one directly "
              "using `--token`.")
    a.status()
    result = capsys.readouterr()
    assert result.out.strip() == expect


def test_status_buddy(capsys):
    """Test the Travis.status() function with temporary token."""
    b = Buddy()
    expect = ("Please replace the default token with a valid one using " 
              "`quickci config update`, or provide one directly "
              "using `--token`.")
    b.status()
    result = capsys.readouterr()
    assert result.out.strip() == expect


def test_status_drone(capsys):
    """Test the Drone.status() function with temporary token."""
    d = DroneCI()
    expect = ("Please replace the default token with a valid one using " 
              "`quickci config update`, or provide one directly "
              "using `--token`.")
    d.status()
    result = capsys.readouterr()
    assert result.out.strip() == expect
