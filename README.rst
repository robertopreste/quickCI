=======
quickCI
=======


.. image:: https://img.shields.io/pypi/v/quickci.svg
        :target: https://pypi.python.org/pypi/quickci

.. image:: https://www.repostatus.org/badges/latest/wip.svg
    :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
    :target: https://www.repostatus.org/#wip

.. image:: https://travis-ci.com/robertopreste/quickCI.svg?branch=master
    :target: https://travis-ci.com/robertopreste/quickCI

.. image:: https://readthedocs.org/projects/quickci/badge/?version=latest
        :target: https://quickci.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/robertopreste


Have a quick look at the status of CI projects from the command line.


* Free software: MIT license
* Documentation: https://quickci.readthedocs.io
* GitHub repo: https://github.com/robertopreste/quickci


Features
========

quickCI allows to have a quick overview of the status of build jobs on several CI services, for a specific branch of the repository being built.
Currently, quickCI supports checking build status for the following CI services:

* `Travis CI`_
* CircleCI_
* AppVeyor_
* Buddy_
* Drone_

More services to come!

Usage
=====

Configuration
-------------

1. Create a config file (it will be located in ``~/.config/quickci/tokens.json``)::

    $ quickci config create

2. Replace placeholders with your own authentication tokens::

    $ quickci config update <service> <token>

Available services are:
    * Travis CI: ``travis``
    * CircleCI: ``circle``
    * AppVeyor: ``appveyor``
    * Buddy: ``buddy``
    * Drone: ``drone``

3. Check that everything is correct::

    $ quickci config show

Check build status
------------------

Check the build status of your projects::

    $ quickci status

The build status of your Travis CI, CircleCI, AppVeyor, Buddy and Drone projects will be returned (``master`` branch).
If you want to monitor one specific branch of your repositories (suppose you have many repos with a dedicated ``dev`` branch for development), you can easily add the ``--branch <branch_name>`` option::

    $ quickci status --branch dev

If the ``--branch`` option is not provided, the build status of the ``master`` branch will be retrieved by default.
It is also possible to check a specific service using subcommands of ``quickci status``::

    $ quickci status travis
    $ quickci status circle
    $ quickci status appveyor
    $ quickci status buddy
    $ quickci status drone

These subcommands also accept the ``--branch`` option.
If the token for a specific service is not listed in ``~/.config/quickci/tokens.json``, it is possible to provide it using the ``--token <service_token>`` option::

    $ quickci status travis --token <TravisCI token>

Please refer to the Usage_ section of the documentation for further information.

Installation
============

quickCI can be installed using pip (**Python>=3.6 only**)::

    $ pip install quickci

Please refer to the Installation_ section of the documentation for further information.

Credits
=======

This package was created with Cookiecutter_ and the `cc-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cc-pypackage`: https://github.com/robertopreste/cc-pypackage
.. _`Travis CI`: https://travis-ci.com/
.. _CircleCI: https://circleci.com/
.. _AppVeyor: https://www.appveyor.com/
.. _Buddy: https://buddy.works
.. _Drone: https://drone.io
.. _Usage: https://quickci.readthedocs.io/en/latest/usage.html
.. _Installation: https://quickci.readthedocs.io/en/latest/installation.html
