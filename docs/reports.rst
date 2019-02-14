
Reports
~~~~~~~

Reports are defined as json objects that must define these fields:

-  name: this name will be used to execute the report through cli.
-  type: report's type. Supported report types are defined below.
-  results: list of results configuration that define how to save the
   reports (`Results documentation <#Results>`__).
-  Set of required or optional fields that are detailed below.

File
^^^^

``type: file``. This report reads the data from local file. These are the
configurations:

-  filename: path to the file. Laika parses the file based on it's extension.
   *csv* and *tsv* files are parsed out of the box. To parse excel files, you
   need to install ``laika-lib[excel]`` dependency.
-  raw: if this parameter is set to ``true``, file's extension will be ignored
   and file contents will be passed to result unparsed.

Example of a file report:

.. code:: json

    {
      "name": "my_file_report",
      "type": "file",
      "filename": "/path/to/filename.xlsx",
      "results": [...]
    }

Query
^^^^^

.. note:: To use query report you must install ``sql`` dependency (for
   Sqlalchemy): ``pip install laika-lib[sql]``.
   You also have the libraries needed to access your specific database.

   For postgres: ``pip install laika-lib[postgres]``

   For Presto(Pyhive): ``pip install laika-lib[presto]``


``type: query``. This report runs a query to some database. Should work
with any database supported by Sqlalchemy but right now it's only tested
with PostgreSQL and Presto. These are the configurations:

-  query\_file: path to a file that contains plane sql code.
-  connection: name of the connection to use.
-  variables: A dictionary with values to replace in query code. You can
   find further explanation in `Query templating <#query-templating>`__

Example of a query report:

.. code:: json

    {
      "name": "my_shiny_query",
      "type": "query",
      "query_file": "/my/dir/query.sql",
      "connection": "local",
      "variables": {
        "foo": "bar"
      },
      "results": [...]
    }

Bash Script
^^^^^^^^^^^

``type: bash``. This report executes a bash command and reads it's
output. You can interpret this report as the ``read_output`` part of
this example:

.. code:: bash

    $ bash_script | read_output

These are the configurations:

-  script: command to execute
-  script\_file: path to the file with bash script to execute. If
   *script* is defined, this field will be ignored.
-  result\_type: type of output data format. Can be *csv*, *json* or
   *raw*. In case of *raw*, the content will not be converted and will
   be passed as is to the result. The explanation of *json* format is
   explained below.

Example bash script report:

.. code:: json

    {
      "name": "some_bash_script",
      "type": "bash",
      "script_file": "some_script.sh",
      "result_type": "json",
      "results": [...]
    }

Bash Script json format
'''''''''''''''''''''''

Json data will be converted to a pandas dataframe using ``pd.read_json``
function
(`Docs <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html>`__).
These are some examples of the formats it accept:

*Example 1 (all arrays must have the same size)*:

.. code:: json

    {
      "column_1": ["data_row_1", "data_row_2", "data_row_3"],
      "column_2": ["data_row_1", "data_row_2", "data_row_3"],
      ...
    }

*Example 2*:

.. code:: json

    [
      {
        "column_1": "data_row_1",
        "column_2": "data_row_1",
        "column_3": "data_row_1",
      },
      {
        "column_1": "data_row_2",
        "column_3": "data_row_2"
      }
      ...
    ]

Download From Google Drive
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: To use drive report you must install ``drive`` dependency:
    ``pip install laika-lib[drive]``

``type: drive``. This report downloads a file from Google Drive. It uses file
parsing logic from the File report.

Configuration:

-  profile: Name of the profile to use. It's credentials must be ones of
   a service account with access to Google Drive's API.
-  grant: email of a grant account, in the name of which the document
   will be downloaded. Grant must have access to specified folder.
-  filename: name of the file to download.
-  folder: directory in which the report will search for the specified
   file.
-  folder\_id: google drive's id of the above folder. If specified,
   folder option is ignored. It's useful if there is more than one
   folder with the same name.
-  subfolder: optional, if specified, this report will look for a
   subfolder inside a folder and, if found, will look there for
   filename. In other words, it will look for this structure:
   ``<folder>/<subfolder>/<filename>``
-  file\_id: google drive's id of the file to download. If specified,
   all other file options are ignored.

Example of a drive report:

.. code:: json

    {
      "type": "drive",
      "profile": "drive_service_account",
      "grant": "me@mail.com",
      "folder_id": "my_folder_id",
      "folder": "TestFolder",
      "subfolder": "TestSubFolder",
      "file_id": "my_file_id",
      "filename":"file_to_download.xlsx"
    }

Download From S3
^^^^^^^^^^^^^^^^

.. note:: To use S3 report you must install ``s3`` dependency:
    ``pip install laika-lib[s3]``

``type: s3``. This report downloads a file from Amazon S3. It uses file
parsing logic from the File report. In order to use this report, you have to
install `boto3 <http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation>`__.

Configuration:

-  profile: Name of profile to use (laika profile, no to confuse with
   aws profiles). Credentials file of the specified profile must contain
   data to be passed to
   `Session <http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session>`__
   constructor. Example of a minimal aws credentials file for laika:

``json   {     "aws_access_key_id": "my key id",     "aws_secret_access_key": "my secret access key"   }``

-  bucket: s3 bucket to download the file from.
-  filename: File to download. This config is the *key* of the file in
   bucket.

Example of a s3 report:

.. code:: json

    {
      "name": "s3_report_example",
      "type": "s3",
      "profile": "my_aws_profile",
      "bucket": "some.bucket",
      "filename": "reports/custom_report.csv",
      "results": [...]
    }

Redash
^^^^^^

``type: redash``. This report downloads query result from
`redash <https://redash.io/>`__ API. These are the configurations:

-  redash\_url: the url of your redash instance.
-  query\_id: id of the query to download. You can get from the query's
   url, it's last part is the id (for example, for
   ``https://some.redash.com/queries/67``, 67 is the id).
-  api\_key: token to access the query, either for user or for query.
   You can find user's token in the profile, token for query can be
   found in the source page.

Example of a redash query:

.. code:: json

    {
      "name": "some_redash_query",
      "type": "redash",
      "api_key": "some api key",
      "query_id": "123",
      "redash_url": "https://some.redash.com",
      "results": [...]
    }

Adwords
^^^^^^^

.. note:: To use adwords report you must install ``adwords`` dependency:
    ``pip install laika-lib[adwords]``

``type: adwords``. This report is generated by Google Adwords API. To
use it, you will need to install
`googleads <https://github.com/googleads/googleads-python-lib/>`__. The
configurations are:

-  profile: Name of profile to use. Credentials file is a *.yaml*, you
   can find out how to generate it in `adwords API
   tutorial <https://developers.google.com/adwords/api/docs/guides/start>`__.
-  report\_definition: the definition of the report which will be passed
   to
   `DownloadReport <http://googleads.github.io/googleads-python-lib/googleads.adwords.ReportDownloader-class.html#DownloadReport>`__
   method of googleads API. You will normally define fields
   ``reportName``, ``dateRangeType``, ``reportType``,
   ``downloadFormat``, ``selector``, but these will vary depending on
   the report type.
-  reportName: In order not to repeat reports definitions, you can
   specify this name and reuse the definition. In other words, you can
   have multiple reports with the same name, but only one
   report\_definition, which will be used for all of them.
-  dateRangeType: if you use report\_definition from another report, you
   can overwrite date range it uses with this configuration.
-  `client\_customer\_id <https://support.google.com/adwords/answer/29198?hl=en>`__.
   Id or list of ids of adwords customers, whose data you want in the
   report.

Example of adwords query:

.. code:: json

    {
      "name": "some_adwords_report",
      "type": "adwords",
      "client_customer_ids": "123-456-7890",
      "report_definition": {
        "reportName": "Shopping Performance Last Month",
        "dateRangeType": "THIS_MONTH",
        "reportType": "SHOPPING_PERFORMANCE_REPORT",
        "downloadFormat": "CSV",
        "selector": {
            "fields": [
                "AccountDescriptiveName",
                "CampaignId",
                "CampaignName",
                "AdGroupName",
                "AdGroupId",
                "Clicks",
                "Impressions",
                "AverageCpc",
                "Cost",
                "ConvertedClicks",
                "CrossDeviceConversions",
                "SearchImpressionShare",
                "SearchClickShare",
                "CustomAttribute1",
                "CustomAttribute2",
                "Brand"
            ]
        }
      },
      "results": [...]
    }

Facebook Insights
^^^^^^^^^^^^^^^^^

``type: facebook``. Retrieves the data from the `Facebook's Insights API <https://developers.facebook.com/docs/marketing-api/insights>`__. The report is
requested as `asynchronous job <https://developers.facebook.com/docs/marketing-api/insights/best-practices/#asynchronous>`__
and is polled for completion every few seconds.

Configuration:

-  profile: Name of profile to use. Credentials file must contain access token
   with at least ``read_insights`` permission. You can generate it in Facebook's
   developers panel for you app. Example ``facebook`` credentials:

.. code:: json

    {
      "access_token": "..."
    }


-  object_id: Facebook's object id from which you want to obtain the data.
-  params: Set of parameters that will be added to the request. Check the
   example report to know what values are used by default, consult Facebook's
   Insights API documentation to discover what parameters you can use.
-  sleep_per_tick: Number of seconds to wait between requests to Facebook API
   to check if the job is finished.

Example of facebook report:

.. code:: json

    {
        "name": "my_facebook_insights_report",
        "type": "facebook",
        "profile": "my_facebook_profile",
        "object_id": "foo_1234567890123456",
        "params": {
            'level': 'ad',
            'limit': 10000000,
            'filtering': '[{"operator": "NOT_IN", "field": "ad.effective_status", "value": ["DELETED"]}]',
            'fields': 'impressions,reach',
            'action_attribution_windows': '28d_click',
            'date_preset': 'last_30d'
        },
        "results": [...]
    }


Module
^^^^^^

``type: module``. Allows you to use a python module with custom report
class to obtain the data. This module will be loaded dynamically and
executed. Currently it has the same configuration as the module result, which
can be confusing.

Configuration:

-  result\_file: Path to python file.
-  result\_class: Name of the class to use as result inside the python
   file. This class must inherit ``Report`` class and define ``process``
   method, which should normally return report data. Simple example of a
   custom report class:

   .. code:: python

       from laika.reports import Report

       class FooResult(Report):

           def process(self):
               # using some custom configs
               filename = self.custom_filename
               # returning some data
               with open(filename) as f:
                   return do_stuff(f.read())

This report will be executed as any other report - it will have
available all the extra configuration you define.

.. Warning:: This report will load and execute arbitrary code, which implies a
   series of security holes. Always check custom modules before using them.

Example of a module report definition:

.. code:: json

    {
      "type": "module",
      "result_file": "./some_folder/my_custom_report.py",
      "result_class": "MyReport",
      "my_custom_config": "value"
    }
