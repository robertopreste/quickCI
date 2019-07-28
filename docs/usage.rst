=====
Usage
=====

Command Line Interface
======================

``quickci`` offers two main CLI commands:

* ``status`` shows the current status of your projects on one or more CI services;
* ``config`` creates or updates the configuration file needed.


``quickci status``
------------------

This command retrieves the status of your projects on one or more CI services (``master`` branch by default).

If issued as ``quickci status``, will retrieve these information for all the CI services for which an authentication token is available in the config file::

    $ quickci status

    CircleCI (master branch)
        project1 -> success
        project2 -> failed
    Travis CI (master branch)
        project1 -> passed
        project2 -> passed
    AppVeyor (master branch)
        project1 -> passed
    Buddy (master branch)
        project2 -> enqueued
    Drone CI (master branch)
        project1 -> success

If you want to monitor one specific branch of your repositories (suppose you have many repos with a dedicated ``dev`` branch for development), you can easily add the ``--branch <branch_name>`` option::

    $ quickci status --branch dev

If the ``--branch`` option is not provided, the build status of the ``master`` branch will be retrieved by default.
It is also possible to check a specific service using subcommands of ``quickci status``::

    $ quickci status travis
    $ quickci status circle
    $ quickci status appveyor
    $ quickci status buddy
    $ quickci status drone

These subcommands also accept the ``--branch`` option::

    $ quickci status travis --branch master
    $ quickci status circle --branch feature1
    $ quickci status drone --branch new_feature

If you have not set up a config file, you can still retrieve information from CI services providing their authentication token right into the command::

    $ quickci status travis --token <TRAVIS_CI_TOKEN>


``quickci config``
------------------

This command allows to create a config file for ``quickci``, or update it if a config file is already available.

The ``create`` command will create a brand new config file, located in ``~/.config/quickci/tokens.json``::

    $ quickci config create

If a config file is already present at that location, you will be prompted to confirm your desire to clear it and create a new one. New config files fill the authentication tokens with a temporary string, which you will need to update with proper tokens.

The ``update`` command allows to update one of the authentication tokens in the existing config file::

    $ quickci config update <CIservice> <token>

The ``show`` command will show all the stored authentication tokens::

    $ quickci config show

