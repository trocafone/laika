Configuration
-------------

Laika reads reports definitions from a json file which must have this
structure:

.. code:: json

    {
      "include": [...],
      "profiles": [...],
      "connections": [...],
      "reports": [...]
    }

The configuration can be separated in multiple files. In this case there
must be a base configuration file that will have to include the other
files via ``"include"`` field with a list of paths:

.. code:: json

    "include": [
      "another_config.json",
      "/some/config.json"
    ]

These files will be included in the configuration. The only constraint
is they can only have ``reports``, ``connections`` and ``profiles``
fields defined.

You can check the `example configuration file <config.json>`__ for more
information.

Profiles
~~~~~~~~

Profiles are all kind of credentials used for accessing external APIs
(like Google Drive). You can specify that credentials are defined in a file
via ``credentials`` key:

.. code:: json

    {
      "name": "my_drive",
      "credentials": "secret.json"
    }

In this case ``credentials`` is path to a file, but file's format depends
on each type of report or result. For example email credentials are
defined in json format like this:

.. code:: json

    {
      "username": "me@gmail.com",
      "password": "secret"
    }

Other option is to define them in an enviroment variable. By default, laika
will search for credentials in ``LAIKA_CREDENTIALS_<profile>`` enviroment
variable, where *<profile>* is the uppercased name of the profile. Or you can
specify your own enviroment variable through ``env_variable`` key.
For example, given this profile definition:

.. code:: json

    {
      "name": "my_profile"
    }

Laika will look for credentials in ``LAIKA_CREDENTIALS_MY_PROFILE``. So if the
profile you're using is that for email result, make sure you defined this
environment variable like that:

.. code:: bash

    $ export LAIKA_CREDENTIALS_MY_PROFILE = '{"username": "me@gmail.com", "password": "secret"}'


And with this definition:


.. code:: json

    {
      "name": "my_profile",
      "env_variable": "CUSTOM_VARIABLE"
    }

Laika will take the credentials from ``CUSTOM_VARIABLE`` enviroment variable.

Connections
~~~~~~~~~~~

Connections are used to access data sources or destinations. They must
have a *name* and a *type*, and a set of specific fields. Currently
supported connections are described below.

Database
^^^^^^^^

Database connection examples:

Postgres

.. code:: json

    {
      "name": "local",
      "type": "sqlalchemy",
      "constring": "postgresql://user@localhost:5432/database"
    }

Presto

.. code:: json

    {
      "name": "local",
      "type": "sqlalchemy",
      "constring": "presto://user@localhost:8889/default"
    }

Email
^^^^^

Example of a smtp connection:

.. code:: json

    {
      "name": "gmail_smtp",
      "type": "email",
      "host": "smtp.gmail.com",
      "port": 587
    }

Ftp
^^^

Example of a ftp connection:

.. code:: json

    {
      "name": "some_ftp",
      "type": "ftp",
      "host": "ftp.home.com"
    }

.. _global-configuration:

Global configuration
~~~~~~~~~~~~~~~~~~~~

In addition to reports, connections and profiles you can define this
configurations:

-  now: string with a datetime to use as current datetime. Useful if your
   reports or results make use of templating to depend on dates relative to
   current date. Must match ``%Y-%m-%d %H:%M:%S`` format.

-  timezone: string of timezone to use. By default all the dates will be
   generated in UTC. You can overwrite it for each particular report.

-  pwd: directory, to which laika will change before executing reports.
   In this directory it will, for example, read query files, or save
   file results (if relative path is specified).


These configurations can be overwritten via command line arguments:

.. code:: bash

    $ laika.py my_report --now "2018-11-12 00:00:00"
