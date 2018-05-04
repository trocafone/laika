.. laika documentation master file, created by
   sphinx-quickstart on Mon Mar 19 15:27:43 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Laika
=====

*laika* is a business reporting library that allows you to request data
from different sources and send it to someone as or save it at some
destination. For example: you can query your database, send the result
as an excel attachment via email and save it on Google Drive or Amazon
S3.

TODO: document what it is and what it is not

Installation
------------

TODO: document this

Usage
-----

``laika.py`` is a script that lets you use laika library. You can run it
like this:

.. code:: bash

    $ laika.py some_report

This command will run the report named *some\_report*. This report must
be defined in some configuration file. By default laika looks for
``config.json`` in the same directory. You can specify a custom config
passing ``-c`` parameter:

.. code:: bash

    $ laika.py -c my_config.json

Path to configuration file can also be specified with the
``LAIKA_CONFIG_FILE_PATH`` environment variable:

.. code:: bash

    $ export LAIKA_CONFIG_FILE_PATH='/home/me/my_config.json'
    $ laika.py my_report

Another parameter you can use is ``--pwd`` which serves for specifying
working directory. It can also be specified in configuration file or
``LAIKA_PWD`` environment variable.

Arguments
~~~~~~~~~

You can check all the predefined ``laika.py`` arguments with ``--help``.

Undefined arguments will be added to report's definition overwriting
default values. Thus, if for example the configuration for ``my_report``
defines field ``my_field`` with value ``foo``, if you execute it like
this:

.. code:: bash

    $ laika.py my_report --my_field bar

``my_field`` configuration will contain ``bar`` as value.


Testing
-------

To run test, you must install test dependencies:

TODO: document

Then, run test from laika directory:

.. code:: bash

    $ cd path/to/laika
    $ python -m unittest discover


Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2

   configuration
   reports
   results
   templating


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
