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
        return {"passed": "green", "failed": "red", "errored": "red",
                "started": "yellow"}

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        :return: Dict[str,str]
        """
        return {"Travis-API-Version": "3",
                "User-Agent": "CI-Board",
                "Authorization": f"token {self.token}"}

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
        q = requests.get(self._url +
                         f"/owner/{login}/repos?repository.active=True",
                         headers=self.headers)
        return [(el["name"], el["id"]) for el in q.json().get("repositories")]

    def status(self) -> List[Tuple[str, str]]:
        """Return name and build status for each repo available (master
        branch only).

        :return: List[Tuple[str,str]]
        """
        loop = asyncio.get_event_loop()
        tasks = [get_async(self._url +
                           f"/repo/{el[1]}/builds?branch.name=master&sort_by=id:desc",
                           headers=self.headers, reponame=el[0])
                 for el in self.repos_ids()]
        res = loop.run_until_complete(asyncio.gather(*tasks))

        return [(el[0], el[1].get("builds")[0].get("state")) for el in res]


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
    Class used to get and manipulate data from the AppVeyor platform.

    :param str token: authentication token provided by AppVeyor
    """

    def __init__(self, token: str):
        self.token = token
        self._url = "https://ci.appveyor.com/api"

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
        return {"Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"}

    def projects(self) -> List[Dict[str, Any]]:
        """Return projects information from the API.

        :return: List[Dict[str,Any]]
        """
        q = requests.get(self._url + "/projects", headers=self.headers)
        return q.json()

    def status(self) -> List[Tuple[str, str]]:
        """Return name and build status for each project available
        (master branch only).

        :return: List[Tuple[str,str]]
        """
        resp = self.projects()
        account = resp[0].get("accountName")
        loop = asyncio.get_event_loop()
        tasks = [get_async(self._url +
                           f"/projects/{account}/{el.get('slug')}/branch/master",
                           headers=self.headers, reponame=el.get("slug"))
                 for el in resp]
        res = loop.run_until_complete(asyncio.gather(*tasks))

        return [(el[0], el[1].get("build").get("status")) for el in res]


class Buddy:
    """
    Class used to get and manipulate data from the Buddy platform.

    :param token: authentication token provided by Buddy
    """

    def __init__(self, token: str):
        self.token = token
        self._url = "https://api.buddy.works"

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        :return: Dict[str,str]
        """
        return {"Authorization": f"Bearer {self.token}"}

    @property
    def colours(self) -> Dict[str, str]:
        """Return colours indicating build status.

        :return: Dict[str,str]
        """
        return {"SUCCESSFUL": "green", "INPROGRESS": "yellow", "FAILED": "red"}

    def workspaces(self) -> List[Tuple[str, str]]:
        """Return user's workspaces from the API.

        :return: List[Tuple[str,str]]
        """
        q = requests.get(self._url + "/workspaces", headers=self.headers)
        wspaces = q.json()

        return [(el["domain"], el["url"]) for el in wspaces["workspaces"]]

    def projects(self) -> List[Tuple[str, str]]:
        """Return user's projects for each workspace from the API.

        :return: List[Tuple[str,str]]
        """
        projs = []
        wspaces = self.workspaces()
        for tup in wspaces:
            r = requests.get(tup[1] + "/projects", headers=self.headers)
            for el in r.json()["projects"]:
                projs.append((el["name"], el["url"]))

        return projs

    def status(self) -> List[Tuple[str, str, str]]:
        """Return project name, pipeline name and status from the API.

        :return: List[Tuple[str,str,str]]
        """
        projs = self.projects()
        st = []
        for el in projs:
            r = requests.get(el[1] + "/pipelines", headers=self.headers)
            for pip in r.json()["pipelines"]:
                st.append((el[0], pip["name"], pip["last_execution_status"]))

        return st


class GitLab:
    """
    TODO: Class used to get and manipulate data from the GitLab platform.

    :param str token: authentication token provided by GitLab
    :param str username: username of the GitLab user
    """

    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        self._url = "https://gitlab.com/api/v4"

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        :return: Dict[str,str]
        """
        return {"Private-Token": self.token}

    def projects(self) -> List[Dict[str, Any]]:
        """Return projects information from the API.

        :return: List[Dict[str,Any]]
        """
        q = requests.get(self._url + f"/users/{self.username}/projects",
                         headers=self.headers)
        return q.json()

    def repos_ids(self) -> List[Tuple[str, str]]:
        """Return name and id for each repo available.

        :return: List[Tuple[str,str]]
        """
        projs = self.projects()
        return [(el["name"], el["id"]) for el in projs]

    def status(self) -> List[Tuple[str, str]]:
        """Return name and build status for each project available
        (master branch only).

        :return: List[Tuple[str,str]]
        """
        pass


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
        return {"Authorization": f"Bearer {self.token}"}


class Config:
    """
    Class that controls the config file used to store and retrieve tokens.
    """
    DEFAULT_CONFIG = """
{
    "TRAVISCI_TOKEN": "replace_me", 
    "CIRCLECI_TOKEN": "replace_me", 
    "APPVEYOR_TOKEN": "replace_me", 
    "BUDDY_TOKEN": "replace_me",
    "CODESHIP_TOKEN": "replace_me", 
    "GITLABCI_TOKEN": "replace_me",
    "GITLABCI_USER": "replace_me"
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
