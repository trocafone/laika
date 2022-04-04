
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
      "results": [

      ]
    }

Query
^^^^^

.. note:: To use query report you must install ``sql`` dependency (for
   Sqlalchemy): ``pip install laika-lib[sql]``.
   You also have the libraries needed to access your specific database.

   For postgres: ``pip install laika-lib[postgres]``

   For Presto(Pyhive): ``pip install laika-lib[presto]``

   We only tested it with postgres and Presto, but it should work with
   all databases supported by SQLAlchemy.


``type: query``. This report runs a query to some database. Should work
with any database supported by Sqlalchemy but right now it's only tested
with PostgreSQL and Presto. These are the configurations:

-  query: sql code to execute.
-  query\_file: path to a file that contains plane sql code. Will be ignored if
   query is specified.
-  connection: name of the connection to use.
-  variables: A dictionary with values to replace in query code. You can find
   further explanation in :ref:`query-templating`.

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
      "results": [

      ]
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
      "results": [

      ]
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
      "column_2": ["data_row_1", "data_row_2", "data_row_3"]
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
    ]

Download From Google Drive
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: To use drive report you must install ``drive`` dependency:
    ``pip install laika-lib[drive]``

``type: drive``. This report downloads a file from Google Drive. It uses file
parsing logic from the File report.

Configuration:

-  profile: Name of the profile to use. Credentials must be ones of
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
-  drive\_id: shared drive's id in case the file is in a shared drive.
-  start_timeout, max_timeout, retry_status_codes: drive API calls sometimes
   fail with 500 errors. To work around this behaviour, in case of error the
   call is retried after waiting *start_timeout* (2 by default) seconds,
   doubling the waiting time after each error until reaching *max_timeout* (300
   by default). If the error persists after that, the exception will be raised.
   *retry_status_codes* is a list of extra status codes to retry after,
   ``[429]`` by default (429 is "too many requests").

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

.. code:: json

    {
        "aws_access_key_id": "my key id",
        "aws_secret_access_key": "my secret access key"
    }

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
      "results": [

      ]
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
-  refresh: True if you want an updated report. **Important**: For refresh
   to work the api\_key must be of user type.
-  parameters: Dictionary of query parameters. They should be written as
   they are defined in the query, without ``p_`` prefix. You can use
   :ref:`filenames-templating` on the values.
-  result_format: the format to download the results in. Can be ``json`` (default) or ``csv``.

Example of a redash query:

.. code:: json

    {
      "name": "some_redash_query",
      "type": "redash",
      "api_key": "some api key",
      "query_id": "123",
      "redash_url": "https://some.redash.com",
      "refresh": true,
      "result_format": "json",
      "parameters": {
          "hello": "world"
      },
      "results": [

      ]
    }

Google Ads Report
^^^^^^^^^^^^^^^^^

.. note:: To use google ads report you must install ``googleads`` dependency:
    ``pip install laika-lib[googleads]``

``type: googleads``. This report makes a query to Google Ads reporting API. To
learn more about Google Ads reporting queries, please refer to
`the documentation <https://developers.google.com/google-ads/api/docs/reporting/overview>`__.

Configuration:

-  profile: Name of profile to use. Credentials file is a *.yaml*, you can learn
   more about it's contents `here <https://developers.google.com/google-ads/api/docs/client-libs/python/configuration>`__.
-  query: Plain text query to send to Google Ads API. This field is templated.
-  query_file: Alternatively you can specify a file which contents will be
   templated and used as query.
-  `customer\_id <https://support.google.com/adwords/answer/29198?hl=en>`__.
   Ids of google ads customers to get the data from. Can be a string in format
   "1234567890" or a list of such strings, in which case the query results for
   each customer will be concatenated.
-  header: Optional text to add as the first line in the resulting report. This
   field is templated.
-  fieldnames: Optional list of column names to use in the resulting report.
   header and fieldnames parameters serve to achieve the same format as in the
   deprecated adwords report.

Example of Google Ads report:

.. code:: json

    {
      "name": "google_ads_shopping_performance_yesterday",
      "type": "googleads",
      "customer_id": "1234567890",
      "query": "SELECT segments.device, segments.date, customer.descriptive_name, campaign.name, ad_group.name, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions FROM shopping_performance_view WHERE segments.date BETWEEN '{Y-1d}-{m-1d}-{d-1d}' AND '{Y-1d}-{m-1d}-{d-1d}'",
      "profile": "my_googleads_profile",
      "header": "Shopping Daily Performance ({Y}-{m}-{d})",
      "results": [

      ]
    }

Adwords
^^^^^^^

.. Warning:: This API is being deprecated by google, use googleads report instead.
    `More about deprecation <https://ads-developers.googleblog.com/2021/04/upgrade-to-google-ads-api-from-adwords.html>`__.

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
   can overwrite date range it uses with this configuration. `Here <https://developers.google.com/adwords/api/docs/guides/reporting#date_ranges>`__
   you can read more about date range types you can chose from.
-  date_range: if dateRangeType is set to ``CUSTOM_DATE``, you can define a
   custom range of dates to extract. The definition must be a dictionary with
   min and max values. In both you can use relative dates with :ref:`filenames-templating`.
-  `client\_customer\_id <https://support.google.com/adwords/answer/29198?hl=en>`__.
   Id or list of ids of adwords customers, whose data you want in the
   report.

Example of adwords query:

.. code:: json

    {
      "name": "some_adwords_report",
      "type": "adwords",
      "date_range": {"min": "{Y-1d}{m-1d}{d-1d}", "max": "{Y-1d}{m-1d}{d-1d}"},
      "client_customer_ids": "123-456-7890",
      "report_definition": {
        "reportName": "Shopping Performance Last Month",
        "dateRangeType": "CUSTOM_DATE",
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
      "results": [

      ]
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
-  since: Starting date for a custom date range. Will only be used if
   ``date_preset``, ``time_range`` or ``time_ranges`` are not present among
   report parameters. You can set relative dates using :ref:`filenames-templating`.
-  until: Same as since, but for the ending date.

Example of facebook report:

.. code:: json

    {
        "name": "my_facebook_insights_report",
        "type": "facebook",
        "profile": "my_facebook_profile",
        "object_id": "foo_1234567890123456",
        "since": "{Y-1d}-{m-1d}-{d-1d}",
        "until": "{Y-1d}-{m-1d}-{d-1d}",
        "params": {
            "level": "ad",
            "limit": 10000000,
            "filtering": "[{\"operator\": \"NOT_IN\", \"field\": \"ad.effective_status\", \"value\": [\"DELETED\"]}]",
            "fields": "impressions,reach",
            "action_attribution_windows": "28d_click"
        },
        "results": [
        ]
    }


RTBHouse
^^^^^^^^

``type: rtbhouse``. Downloads marketing costs report from RTBHouse API.
Reported campaigns (advertisers) are all those created by the account.

Configuration:

-  profile: Name of profile to use. Credentials must be a json containing
   ``username`` and ``password`` fields.
-  day_from: Starting date for the period to retrieve costs for. You can set
   a relative date using :ref:`filenames-templating`.
-  day_to: Same as day_from, but for the ending date.
-  group_by and convention_type: Optional parameters to send to RTBHouse.
-  campaign_names: Mapping from campaign hash to a readable name for the
   resulting report.
-  column_names: Mapping to rename columns in the resulting report.

Example of rtbhouse report:

.. code:: json

    {
      "name": "my_rtbhouse_report",
      "type": "rtbhouse",
      "profile": "my_rtbhouse_profile",
      "group_by": "day",
      "convention_type": "ATTRIBUTED",
      "day_from": "{Y-1d}-{m-1d}-{d-1d}",
      "day_to": "{Y-1d}-{m-1d}-{d-1d}",
      "campaign_names": {
        "1234567890": "Some readable campaign name"
      },
      "column_names": {
        "hash": "CampaignID",
        "name": "Campaign",
        "campaignCost": "Cost",
        "day": "Date"
      },
      "results": [

      ]
    }


Rakuten
^^^^^^^

``type: rakuten``. Downloads a report from Rakuten marketing platform by name.

Configuration:

-  profile: Name of profile to use. Credentials must be a json containing
   ``token`` key, with a token to access Rakuten API.
-  report_name: Existing report to download from the platform.
-  filters: A set of filters to send to the API. Must be a dictionay, you can
   use :ref:`filenames-templating` on the values.

Example of rakuten report:

.. code:: json

    {
      "name": "my_rakuten_report",
      "type": "rakuten",
      "profile": "my_rakuten_profile",
      "report_name": "some-report",
      "filters": {
        "start_date": "{Y-10d}-{m-10d}-{d-10d}",
        "end_date": "{Y-1d}-{m-1d}-{d-1d}",
        "include_summary": "N",
        "date_type": "transaction"
      }
    }


BingAds
^^^^^^^

.. note:: To use bingads report you must install ``bingads`` dependency:
    ``pip install laika-lib[bingads]``

``type: bingads``. Downloads reports from Microsoft Ads portal using Bingads SDK. The
configurations are:

-  profile: Name of profile to use. Credentials file must be a a *.json* containing ``client_id``, ``developer_token``, ``state`` and ``refresh_token``. Find more about authentication `here <https://docs.microsoft.com/en-us/advertising/guides/authentication-oauth?view=bingads-13>`__.
-  customer_id and account_id: IDs of accounts you want to authenticate for. You can see how to obtain these IDs in `this part of documentation <https://docs.microsoft.com/en-us/advertising/guides/get-started?view=bingads-13#get-ids>`__.
-  report_request_type: Report request data object. You can see all the available data object `here <https://docs.microsoft.com/en-us/advertising/reporting-service/reporting-data-objects>`__.
-  start_date and end_date: you can define a period for the data you want. These fields are templated via :ref:`filenames-templating`.
-  predefined_time: in case you don't specify start_date and end_date, you can set a predefined_time. Default value is "Yesterday"

BingAds report accepts more parameters, you can see examples in `Microsoft's documenentation <https://docs.microsoft.com/en-us/advertising/guides/code-example-report-requests?view=bingads-13>`__ and verify which of the parameters laika accepts checking source code.

Example of BingAds report:

.. code:: json

    {
      "name": "bingads_keyword_performance",
      "type": "bingads",
      "profile": "my_bingads_profile",
      "customer_id": 1234567,
      "report_request_type": "KeywordPerformanceReportRequest",
      "report_account_ids": [1234567, 2345678],
      "report_columns": [
          "TimePeriod",
          "AccountId",
          "CampaignId",
          "CampaignName",
          "Keyword",
          "DeviceType",
          "Network",
          "Impressions",
          "Clicks",
          "Spend",
          "BidMatchType",
          "Ctr",
          "AverageCpc",
          "QualityScore"
      ],
      "start_date": "{Y}-{m}-{d}",
      "end_date": "{Y}-{m}-{d}"
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
