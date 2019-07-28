#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import asyncio
import aiohttp
import click
from concurrent.futures import ThreadPoolExecutor
import pprint
import json
import os
import requests
from typing import List, Tuple, Dict, Any


class _CIService:
    """Base class for any CI service.

    Each specific class below will need to be instantiated with an
    authentication token (explicitly provided) and a base url for the
    given CI service (internally provided by that specific class).

    Attributes:
        _token: Authentication token.
        _url: Base url for API requests.
        _branch: Branch to check (default: master).
        _found: Whether the given branch has at least one build
            (default: False).
    """

    def __init__(self, token: str, url: str, branch: str):
        self._token = token
        self._url = url
        self._branch = branch
        self._found = False

    @property
    def colours(self) -> Dict[str, str]:
        """Return colours indicating build status.

        Returns:
            Dictionary of status -> colour.
        """
        return {"passed": "green", "success": "green", "SUCCESSFUL": "green",
                "failed": "red", "errored": "red", "FAILED": "red",
                "started": "yellow", "running": "yellow",
                "INPROGRESS": "yellow", "ENQUEUED": "yellow"}

    @staticmethod
    async def aget(host: str,
                   headers: Dict[str, Any]) -> Dict[str, Any]:
        """Generic asynchronous request call.

        Args:
            host: Url to request.
            headers: Request headers to use.

        Returns:
            Dictionary with async response.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(host, headers=headers) as response:
                data = await response.json()
                return data


class TravisCI(_CIService):
    """Class used to get and manipulate data from the TravisCI platform."""

    def __init__(self, token: str = "replace_me", branch: str = "master"):
        url = "https://api.travis-ci.com"
        super().__init__(token, url, branch)

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        Returns:
            Dictionary with API headers.
        """
        return {"Travis-API-Version": "3",
                "User-Agent": "quickCI",
                "Authorization": f"token {self._token}"}

    @property
    def login(self) -> str:
        """Get login information from the API.

        Returns:
            Login information from the API.
        """
        response = requests.get(f"{self._url}/user", headers=self.headers)
        data = response.json()
        return data.get("login", "")

    def projects(self) -> List[Tuple[str, str]]:
        """Find name and id of each repository.

        Returns:
            Name and id for each repo available.
        """
        url = f"{self._url}/owner/{self.login}/repos?repository.active=True"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return [(el["name"], el["id"]) for el in data.get("repositories")]

    async def astatus(self, repo: Tuple[str, str]):
        """Print name and build status for the given repo and branch.

        Args:
            repo: Repo tuple as returned by self.repositories().
        """
        url = f"{self._url}/repo/{repo[1]}/builds?branch.name={self._branch}&sort_by=id:desc"
        status = await self.aget(url, headers=self.headers)
        repo_name = repo[0]
        try:
            repo_stat = status.get("builds")[0].get("state")
            self._found = True
            click.secho(f"\t{repo_name} -> {repo_stat}", fg=self.colours[repo_stat])
        except IndexError:  # no builds within the given branch
            return

        return

    def status(self):
        """Perform the async call to retrieve repo status for each repo
        available in self.repos_ids().
        """
        if self._token == "replace_me":
            click.secho("Please replace the default token with a valid one "
                        "using `quickci config update`, or provide one "
                        "directly using `--token`.", fg="red")
            return
        projs = self.projects()
        loop = asyncio.get_event_loop()
        tasks = [self.astatus(el) for el in projs]
        loop.run_until_complete(asyncio.gather(*tasks))
        if self._found is False:
            click.secho("\tNo build found.", fg="magenta")
        return


class CircleCI(_CIService):
    """Class used to get and manipulate data from the CircleCI platform."""

    def __init__(self, token: str = "replace_me", branch: str = "master"):
        url = "https://circleci.com/api/v1.1"
        super().__init__(token, url, branch)

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        Returns:
            Dictionary with API headers.
        """
        return {"circle-token": self._token}

    def projects(self) -> List[Dict[str, Any]]:
        """Return projects information from the API.

        Returns:
            Json dictionary with API response.
        """
        response = requests.get(f"{self._url}/projects?", headers=self.headers)
        return response.json()

    def astatus(self, repo: Dict[str, Any]):
        """Print name and build status for the given repo and branch.

        Args:
            repo: Repo dict as returned by self.projects().
        """
        repo_name = repo.get("reponame")
        try:
            repo_stat = (repo.get("branches").get(self._branch).get("latest_workflows")
                         .get("workflow").get("status"))
            self._found = True
            click.secho(f"\t{repo_name} -> {repo_stat}", fg=self.colours[repo_stat])
        except AttributeError:  # no builds within the given branch
            return
        return

    def status(self):
        """Return name and build status for each project available.
        """
        if self._token == "replace_me":
            click.secho("Please replace the default token with a valid one "
                        "using `quickci config update`, or provide one "
                        "directly using `--token`.", fg="red")
            return
        projs = self.projects()
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor()
        tasks = [loop.run_in_executor(executor, self.astatus, repo)
                 for repo in projs]
        asyncio.gather(*tasks)
        if self._found is False:
            click.secho("\tNo build found.", fg="magenta")
        return


class AppVeyor(_CIService):
    """Class used to get and manipulate data from the AppVeyor platform."""

    def __init__(self, token: str = "replace_me", branch: str = "master"):
        url = "https://ci.appveyor.com/api"
        super().__init__(token, url, branch)

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        Returns:
            Dictionary with API headers.
        """
        return {"Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json"}

    def projects(self) -> List[Dict[str, Any]]:
        """Return projects information from the API.

        Returns:
            Json dictionary with API response.
        """
        response = requests.get(f"{self._url}/projects", headers=self.headers)

        return response.json()

    async def astatus(self, repo: str, account: str):
        """Print name and build status for the given repo and branch.

        Args:
            repo: Repository name.
            account: Account name.
        """
        url = f"{self._url}/projects/{account}/{repo}/branch/{self._branch}"
        status = await self.aget(url, headers=self.headers)
        try:
            repo_stat = status.get("build").get("status")
            self._found = True
            click.secho(f"\t{repo} -> {repo_stat}", fg=self.colours[repo_stat])
        except AttributeError:  # no builds within the given branch
            return
        return

    def status(self):
        """Perform the async call to retrieve repo status for each repo
        available in self.projects() for the current account.
        """
        if self._token == "replace_me":
            click.secho("Please replace the default token with a valid one "
                        "using `quickci config update`, or provide one "
                        "directly using `--token`.", fg="red")
            return
        projs = self.projects()
        account = projs[0].get("accountName")
        loop = asyncio.get_event_loop()
        tasks = [self.astatus(el.get("slug"), account) for el in projs]
        loop.run_until_complete(asyncio.gather(*tasks))
        if self._found is False:
            click.secho("\tNo build found.", fg="magenta")
        return


class Buddy(_CIService):
    """Class used to get and manipulate data from the Buddy platform."""

    def __init__(self, token: str = "replace_me", branch: str = "master"):
        url = "https://api.buddy.works"
        super().__init__(token, url, branch)

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        Returns:
            Dictionary with API headers.
        """
        return {"Authorization": f"Bearer {self._token}"}

    def workspaces(self) -> List[str]:
        """Return user's workspaces from the API.

        Returns:
            List of urls for each workspace.
        """
        response = requests.get(f"{self._url}/workspaces", headers=self.headers)
        wspaces = response.json()

        return [el["url"] for el in wspaces.get("workspaces")]

    def projects(self) -> List[Tuple[str, str]]:
        """Return user's projects for each workspace from the API.

        Returns:
            List of projects for each workspace.
        """
        wspaces = self.workspaces()
        loop = asyncio.get_event_loop()
        tasks = [self.aget(f"{ws}/projects", headers=self.headers)
                 for ws in wspaces]
        projs = loop.run_until_complete(asyncio.gather(*tasks))

        return [(el.get("name"), el.get("url"))
                for proj in projs for el in proj.get("projects")]

    async def astatus(self, repo: Tuple[str, Any]):
        """Print name and build status for the given repo and branch.

        Args:
            repo: Repo tuple as returned by self.projects().
        """
        repo_name = repo[0]
        status = await self.aget(f"{repo[1]}/pipelines", headers=self.headers)
        pipes = status.get("pipelines")
        for pipe in pipes:
            pipe_name = pipe.get("name")
            pipe_url = pipe.get("url")
            response = await self.aget(f"{pipe_url}/executions",
                                       headers=self.headers)
            executions = response.get("executions")
            for ex in executions:
                ex_branch = ex.get("branch").get("name")
                if ex_branch == self._branch:
                    self._found = True
                    pipe_stat = ex.get("status")
                    click.secho(f"\t{repo_name} ({pipe_name} pipeline) -> "
                                f"{pipe_stat.casefold()}",
                                fg=self.colours[pipe_stat])
                    break

        return

    def status(self):
        """Perform the async call to retrieve repo status for each repo
        available in self.projects() for the current account.
        """
        if self._token == "replace_me":
            click.secho("Please replace the default token with a valid one "
                        "using `quickci config update`, or provide one "
                        "directly using `--token`.", fg="red")
            return
        projs = self.projects()
        loop = asyncio.get_event_loop()
        tasks = [self.astatus(repo) for repo in projs]
        loop.run_until_complete(asyncio.gather(*tasks))
        if self._found is False:
            click.secho("\tNo build found.", fg="magenta")
        return


class DroneCI(_CIService):
    """Class used to get and manipulate data from the Drone CI platform."""

    def __init__(self, token: str = "replace_me", branch: str = "master"):
        url = "https://cloud.drone.io/api"
        super().__init__(token, url, branch)

    @property
    def headers(self) -> Dict[str, str]:
        """Return headers used to connect to the API.

        Returns:
            Dictionary with API headers.
        """
        return {"Authorization": f"Bearer {self._token}"}

    def projects(self) -> List[Tuple[str, str, int]]:
        """Return user's projects from the API.

        Returns:
            List of projects.
        """
        response = requests.get(f"{self._url}/user/repos",
                                headers=self.headers)
        repos = response.json()
        actives = filter(lambda d: d["active"] is True, repos)
        # projs = [(el["name"], el["namespace"], el["counter"])
        projs = [(el["name"], el["slug"], el["counter"])
                 for el in actives]
        return projs

    async def astatus(self, repo: Tuple[str, str, int]):
        """Print name and build status for the given repo (latest build only).

        Args:
            repo: Repo tuple as returned by self.projects().
        """
        build = repo[2]
        while build > 0:
            status = await self.aget(f"{self._url}/repos/{repo[1]}/builds/{build}",
                                     headers=self.headers)
            build_source = status.get("source")
            if build_source == self._branch:
                self._found = True
                break
            else:
                build -= 1
        else:  # no builds within the given branch
            return

        repo_name = repo[0]
        repo_stat = status.get("status")
        click.secho(f"\t{repo_name} -> {repo_stat}", fg=self.colours[repo_stat])
        return

    def status(self):
        """Perform the async call to retrieve repo status for each repo
        available in self.projects() for the current account.
        """
        if self._token == "replace_me":
            click.secho("Please replace the default token with a valid one "
                        "using `quickci config update`, or provide one "
                        "directly using `--token`.", fg="red")
            return
        projs = self.projects()
        loop = asyncio.get_event_loop()
        tasks = [self.astatus(repo) for repo in projs]
        loop.run_until_complete(asyncio.gather(*tasks))
        if self._found is False:
            click.secho("\tNo build found.", fg="magenta")
        return


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
        q = requests.get(f"{self._url}/users/{self.username}/projects",
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
    """Class that controls the config file used to store and retrieve tokens."""

    DEFAULT_CONFIG = """
{
    "TRAVISCI_TOKEN": "replace_me", 
    "CIRCLECI_TOKEN": "replace_me", 
    "APPVEYOR_TOKEN": "replace_me", 
    "BUDDY_TOKEN": "replace_me", 
    "DRONE_TOKEN": "replace_me"
}
"""

    SERVICES = {"travis": "TRAVISCI_TOKEN",
                "circle": "CIRCLECI_TOKEN",
                "appveyor": "APPVEYOR_TOKEN",
                "buddy": "BUDDY_TOKEN",
                "drone": "DRONE_TOKEN"}

    def __init__(self):
        self._temporary = False
        self._config_dir = os.path.expanduser("~/.config/quickci")
        self._config_file = "tokens.json"
        self._content = self.parse()

    @property
    def config_path(self):
        return os.path.join(self._config_dir, self._config_file)

    def parse(self) -> Dict[str, str]:
        """Parse and return the existing config dict or return the
        default one otherwise.
        """
        try:
            with open(self.config_path) as f:
                conf = json.loads(f.read())
        except FileNotFoundError:
            conf = json.loads(self.DEFAULT_CONFIG)
            self._temporary = True
        return conf

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def temporary(self):
        return self._temporary

    def check_dir(self) -> bool:
        """Check whether the config dir exists or not.
        """
        return os.path.isdir(self._config_dir)

    def check_file(self) -> bool:
        """Check whether the config file exists or not.
        """
        return os.path.isfile(self.config_path)

    def create(self):
        """Create the config file in the default config dir.
        """
        if not self.check_dir():
            os.makedirs(self._config_dir)
        with open(self.config_path, "w") as f:
            f.write(self.DEFAULT_CONFIG)
        self._temporary = False

    def update(self, service: str, token: str):
        """Update a given service token with a new one.

        Args:
            service: Service name.
            token: New token.
        """
        self.content[self.SERVICES[service]] = token

    def save(self):
        """Write the updated config to the default path.
        """
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.content))

    def show(self):
        """Return a screen-friendly representation of the config.
        """
        return pprint.pprint(self.content)

    def __getitem__(self, item):
        return self.content[self.SERVICES[item]]
