=======
quickCI
=======


.. image:: https://img.shields.io/pypi/v/quickci.svg
        :target: https://pypi.python.org/pypi/quickci

.. image:: https://www.repostatus.org/badges/latest/wip.svg
    :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
    :target: https://www.repostatus.org/#wip

.. image:: https://travis-ci.com/robertopreste/quickci.svg?branch=master
        :target: https://travis-ci.com/robertopreste/quickci

.. image:: https://circleci.com/gh/robertopreste/quickci.svg?style=svg
        :target: https://circleci.com/gh/robertopreste/quickci

.. image:: https://codecov.io/gh/robertopreste/quickci/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/robertopreste/quickci

.. image:: https://readthedocs.org/projects/quickci/badge/?version=latest
        :target: https://quickci.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/robertopreste/quickci/shield.svg
     :target: https://pyup.io/repos/github/robertopreste/quickci/
     :alt: Updates

.. image:: https://pyup.io/repos/github/robertopreste/quickci/python-3-shield.svg
     :target: https://pyup.io/repos/github/robertopreste/quickci/
     :alt: Python 3

.. image:: https://pepy.tech/badge/quickci
    :target: https://pepy.tech/project/quickci
    :alt: Downloads


Have a quick look at the status of CI projects from the command line.


* Free software: MIT license
* Documentation: https://quickci.readthedocs.io
* GitHub repo: https://github.com/robertopreste/quickci


Features
--------

Currently ``quickci`` supports checking build status for the following CI services:

* `Travis CI`_
* CircleCI_
* AppVeyor_
* Buddy_

TODO:

* GitLab
* CodeShip

Usage
-----

Configuration
=============

1. Create a config file (it will be located in ``~/.config/quickci/tokens.json``::

    $ quickci config create

2. Replace placeholders with your own authentication tokens::

    $ quickci config update <service> <token>

Available services are:
    * Travis CI: ``travis``
    * CircleCI: ``circle``
    * AppVeyor: ``appveyor``
    * Buddy: ``buddy``

3. Check that everything is correct::

    $ quickci config show

Build status
============

Check the build status of your projects::

    $ quickci status

The build status of your Travis CI, CircleCI, AppVeyor and Buddy projects will be returned (currently only master branch).

It is also possible to check a specific service using subcommands of ``quickci status``::

    $ quickci status travis
    $ quickci status circle
    $ quickci status appveyor
    $ quickci status buddy

If the token for a specific service is not listed in ``~/.config/quickci/tokens.json``, it is possible to provide it using the ``--token <service_token>`` option::

    $ quickci status travis --token <TravisCI token>

Installation
------------

``quickci`` can be installed using pip::

    $ pip install quickci


Credits
-------

This package was created with Cookiecutter_ and the `cc-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cc-pypackage`: https://github.com/robertopreste/cc-pypackage
.. _`Travis CI`: https://travis-ci.com/
.. _CircleCI: https://circleci.com/
.. _AppVeyor: https://www.appveyor.com/
.. _Buddy: https://buddy.works
