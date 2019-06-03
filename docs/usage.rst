=====
Usage
=====

Command Line Interface
----------------------

``quickci`` offers two main CLI commands:

* ``status`` shows the current status of your projects on one or more CI services;
* ``config`` creates or updates the configuration file needed.


``quickci status``
==================

This command retrieves the status of the master branch of your projects on one or more CI services.

If issued as ``quickci status``, will retrieve these information for all the CI services for which an authentication token is available in the config file::

    $ quickci status

    CircleCI
        project1 -> passed
        project2 -> failed
    Travis CI
        project1 -> passed
        project2 -> passed

If you have not set up a config file, you can still retrieve information from CI services providing their authentication token right into the command::

    $ quickci status --travis <TRAVIS_CI_TOKEN> --circle <CIRCLE_CI_TOKEN> --codeship <CODESHIP_TOKEN>


``quickci config``
==================

This command allows to create a config file for ``quickci``, or update it if a config file is already available.

The ``--create`` option will create a brand new config file, located in ``~/.config/quickci/tokens.json``. If a config file is already present at that location, you will be prompted to confirm your desire to clear it and create a new one. New config files fill the authentication tokens with a temporary string, which you will need to update with proper tokens.

The ``--update`` option allows to update one of the authentication tokens in the existing config file::

    $ quickci config --update TRAVISCI_TOKEN <new_token>

The ``--show`` option will show all the stored authentication tokens.

