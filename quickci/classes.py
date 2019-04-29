#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import asyncio
import aiohttp
import pprint
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

    :param str token: authentication token provided by Travis CI
    """

    def __init__(self, token: str):
        self.token = token
        self._url = "https://api.travis-ci.com"

    @property
    def colours(self) -> Dict[str, str]:
        """Return colours indicating build status.

        :return: Dict[str,str]
        """
        return {"passed": "green", "failed": "red", "errored": "red"}

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        :return: Dict[str,str]
        """
        return {"Travis-API-Version": "3",
                "User-Agent": "CI-Board",
                "Authorization": "token {}".format(self.token)}

    def user_info(self) -> Dict[str, Any]:
        """Return user information from the API.

        :return: Dict[str,Any]
        """
        q = requests.get(self._url + "/user", headers=self.headers)
        return q.json()

    def builds(self) -> Dict[str, Any]:
        """Return builds information from the API.

        :return: Dict[str,Any]
        """
        q = requests.get(self._url + "/builds", headers=self.headers)
        return q.json()

    def repos_ids(self) -> List[Tuple[str, str]]:
        """Return name and id for each repo available.

        :return: List[Tuple[str,str]]
        """
        login = self.user_info().get("login")
        q = requests.get(self._url + "/owner/{}/repos?repository.active=True".format(login),
                         headers=self.headers)
        return [(el["name"], el["id"]) for el in q.json().get("repositories")]

    def status(self) -> List[Tuple[str, str]]:
        """Return name and build status for each repo available (master
        branch only).

        :return: List[Tuple[str,str]]
        """
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

    :param str token: authentication token provided by CircleCI
    """

    def __init__(self, token: str):
        self.token = token
        self._url = "https://circleci.com/api/v1.1"

    @property
    def colours(self) -> Dict[str, str]:
        """Return colours indicating build status.

        :return: Dict[str,str]
        """
        return {"success": "green", "running": "yellow", "failed": "red"}

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        :return: Dict[str,str]
        """
        return {"circle-token": self.token}

    def user_info(self) -> Dict[str, Any]:
        """Return user information from the API.

        :return: Dict[str,Any]
        """
        q = requests.get(self._url + "/me?", headers=self.headers)
        return q.json()

    def projects(self) -> List[Dict[str, Any]]:
        """Return projects information from the API.

        :return: List[Dict[str,Any]]
        """
        q = requests.get(self._url + "/projects?", headers=self.headers)
        return q.json()

    def status(self) -> List[Tuple[str, str]]:
        """Return name and build status for each project available
        (master branch only).

        :return: List[Tuple[str,str]]
        """
        resp = self.projects()
        return [(repo.get("reponame"),
                 (repo.get("branches").get("master").get("latest_workflows")
                  .get("workflow").get("status")))
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
    DEFAULT_CONFIG = """
{
    "TRAVISCI_TOKEN": "replace_me", 
    "CIRCLECI_TOKEN": "replace_me", 
    "APPVEYOR_TOKEN": "replace_me", 
    "CODESHIP_TOKEN": "replace_me", 
    "RTD_TOKEN": "replace_me"
}
"""

    def __init__(self):
        self._config_dir = os.path.expanduser("~/.config/quickci")
        self._config_file = "tokens.json"
        self._content = self.parse()

    @property
    def config_path(self):
        return os.path.join(self._config_dir, self._config_file)

    def parse(self):
        try:
            with open(self.config_path) as f:
                res = json.loads(f.read())
        except FileNotFoundError:
            res = json.loads(self.DEFAULT_CONFIG)
        return res

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def check_dir(self) -> bool:
        """
        Check whether the config dir exists or not.

        :return: bool
        """
        return os.path.isdir(self._config_dir)

    def check_file(self) -> bool:
        """
        Check whether the config file exists or not.

        :return: bool
        """
        return os.path.isfile(self.config_path)

    def create(self) -> bool:
        """Create the config file in the default config dir.

        :return: bool
        """
        if not self.check_dir():
            os.makedirs(self._config_dir)
        with open(self.config_path, "w") as f:
            f.write(self.DEFAULT_CONFIG)

        return True

    def update(self, service: str, token: str):
        """Update a given service token with a new one.

        :param str service: service name

        :param str token: new token

        :return:
        """
        self.content[service] = token

    def save(self) -> bool:
        """Write the updated config to the default path.

        :return: bool
        """
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.content))

        return True

    def show(self):
        """Return a screen-friendly representation of the config.

        :return:
        """
        return pprint.pprint(self.content)

    def __getitem__(self, item):
        return self.content[item]
