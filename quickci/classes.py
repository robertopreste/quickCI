#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import asyncio
import aiohttp
import json
import os
import requests
from typing import List, Tuple, Dict, Any


async def get_async(host: str,
                    headers: Dict[str, Any],
                    reponame: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(host, headers=headers) as resp:
            response = await resp.json()
            return reponame, response


class TravisCI:
    """
    Class used to get and manipulate data from the TravisCI platform.
    """

    def __init__(self, token: str):
        """

        :param str token: authentication token provided by Travis CI
        """
        self.token = token
        self._url = "https://api.travis-ci.com"

    @property
    def colours(self):
        return {"passed": "green", "failed": "red", "errored": "red"}

    @property
    def headers(self):
        return {"Travis-API-Version": "3",
                "User-Agent": "CI-Board",
                "Authorization": "token {}".format(self.token)}

    def user_info(self):
        q = requests.get(self._url + "/user", headers=self.headers)
        return q.json()

    def builds(self):
        q = requests.get(self._url + "/builds", headers=self.headers)
        return q.json()

    def repos_ids(self):
        login = self.user_info().get("login")
        q = requests.get(self._url + "/owner/{}/repos?repository.active=True".format(login),
                         headers=self.headers)
        return [(el["name"], el["id"]) for el in q.json().get("repositories")]

    def status(self):
        loop = asyncio.get_event_loop()
        tasks = [get_async(
            self._url + "/repo/{}/builds?branch.name=master&sort_by=id:desc".format(el[1]),
            headers=self.headers,
            reponame=el[0])
            for el in self.repos_ids()
        ]
        res = loop.run_until_complete(asyncio.gather(*tasks))

        return [(el[0], el[1].get("builds")[0].get("state")) for el in res]


        # res = []
        # for el in self.repos_ids():
        #     q = requests.get(self._url
        #                      + "/repo/{}/builds?branch.name=master&sort_by=id:desc".format(el[1]),
        #                      headers=self.headers)
        #     state = q.json().get("builds")[0].get("state")
        #     res.append((el[0], state))
        # return res


class CircleCI:
    """
    Class used to get and manipulate data from the CircleCI platform.
    """

    def __init__(self, token: str):
        """

        :param str token: authentication token provided by CircleCI
        """
        self.token = token
        self._url = "https://circleci.com/api/v1.1"

    @property
    def colours(self):
        return {"success": "green", "running": "yellow", "failed": "red"}

    @property
    def headers(self):
        return {"circle-token": self.token}

    def user_info(self):
        q = requests.get(self._url + "/me?", headers=self.headers)
        return q.json()

    def projects(self):
        q = requests.get(self._url + "/projects?", headers=self.headers)
        return q.json()

    def status(self) -> List[Tuple[str, str]]:
        """
        Return the status of each project present on CircleCI (master
        branch only).
        :return: List[Tuple[str, str]]
        """
        resp = self.projects()
        return [(repo["reponame"],
                repo["branches"]["master"]["latest_workflows"]["workflow"]["status"])
                for repo in resp]


class AppVeyor:
    """
    TODO: Class used to get and manipulate data from the AppVeyor platform.
    """

    def __init__(self, token: str):
        """

        :param str token: authentication token provided by AppVeyor
        """
        self.token = token
        self._url = "https://ci.appveyor.com/api"

    @property
    def headers(self):
        return {"Authentication": "Bearer {}".format(self.token)}


class Codeship:
    """
    TODO: Class used to get and manipulate data from the Codeship platform.
    Token expires after an hour. 
    """

    def __init__(self, token: str):
        """

        :param str token: authentication token provided by Codeship
        """
        self.token = token
        self._url = "https://api.codeship.com/v2"

    @property
    def headers(self):
        return {"Authentication": "Bearer {}".format(self.token)}


class ReadTheDocs:
    """
    TODO: Class used to get and manipulate data from the ReadTheDocs platform.
    Not possible to retrieve projects belonging to a specific user.
    """

    def __init__(self, token: str):
        """

        :param str token: authentication token provided by ReadTheDocs
        """
        self.token = token
        self._url = "https://readthedocs.org/api/v2"

    @property
    def headers(self):
        return {"Authentication": self.token}


class Config:
    """
    Class that controls the config file used to store and retrieve tokens.
    """

    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/quickci")
        self.config_file = "tokens.json"
        self.content = """{
    "TRAVISCI_TOKEN": "replace_me", 
    "CIRCLECI_TOKEN": "replace_me", 
    "APPVEYOR_TOKEN": "replace_me", 
    "CODESHIP_TOKEN": "replace_me", 
    "RTD_TOKEN": "replace_me"
}"""

    @property
    def config_path(self):
        return os.path.join(self.config_dir, self.config_file)

    @staticmethod
    def check_dir(config_dir: str) -> bool:
        """
        Check whether the config dir exists or not.
        :param str config_dir: config dir to check
        :return: bool
        """
        return os.path.isdir(config_dir)

    @staticmethod
    def check_file(config_file: str) -> bool:
        """
        Check whether the config file exists or not.
        :param str config_file: config file to check
        :return: bool
        """
        return os.path.isfile(config_file)

    def create_config(self):
        """
        Create the config file in the default config dir.
        :return:
        """
        # TODO: check existence of config dir and file first
        if not self.check_dir(self.config_dir):
            os.makedirs(self.config_dir)
        with open(self.config_path, "w") as f:
            f.write(self.content)

        return

    def parse_config(self):
        """
        Parse the config file, if present.
        :return:
        """
        if self.check_file(self.config_path):
            with open(self.config_path) as f:
                return json.loads(f.read())
