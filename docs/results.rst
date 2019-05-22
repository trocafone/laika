

Results
~~~~~~~

Results are defined for each report in a list. Each result is an object,
that must define *type* field. The rest of the fields depend on the type
of result. Below are described all the supported results.

.. note:: Results will be executed in the same order they are defined. If the
    first one raises an exception, the execution will be suspended (the next
    ones will not execute).

File
^^^^

``type: file``. This result will save the data as a file. The
configurations for this result are:

-  filename: path to the file. Depending on the file extension this file
   will be saved as excel (xls or xlsx), tsv or csv.

Example of a file result:

.. code:: json

    "result": {
      "type": "file",
      "filename": "output.csv"
    }

Email
^^^^^

``type: email``. Sends the data as an attachment in an email.
Configurations for this result are:

-  connection: Name of a connection with type *email*.
-  profile: Profile name to use. Credentials from this profile must have
   ``username`` and ``password`` field from smtp service you will use.
-  filename: name of the file to attach.
-  recipients: one or more recipients for the email. Can be a string
   with one recipient or a list of recipients. This camp is required.
-  subject: subject of the email.
-  body: text the email will contain.
-  attachments: Optional. list of files to attach to the email. Must be
   a list of paths to files.

Subject and body can be formatted the same way filenames are formatted.
You can find more about it in :ref:`filenames-templating`.
Example of email result:

.. code:: json

    {
      "type": "email",
      "filename": "report_{Y}-{m}-{d}_{H}-{M}.xlsx",
      "recipients": ["some_recipient@mail.com", "another_recipient@foo.com"],
      "subject": "Some report",
      "body": "Report generated {Y}-{m}-{d} {H}:{M}. \nDo not reply this email!",
      "profile": "my_gmail",
      "connection": "gmail_smtp"
    }

Ftp
^^^

``type: ftp``. Uploads the data to a ftp server. Configurations for this
result are:

-  profile: Name of the profile to use. Credentials must have
   ``username`` and ``password`` fields to authenticate in the ftp
   service.
-  connection: Name of a connection of ftp type.
-  filename: Name with which the file will be uploaded to ftp.

Example of ftp result:

.. code:: json

    {
      "type": "ftp",
      "profile": "my_ftp_profile",
      "connection": "some_ftp",
      "filename": "my_report.csv"
    }

Google Drive
^^^^^^^^^^^^

.. note:: To use drive result you must install ``drive`` dependency:
    ``pip install laika-lib[drive]``

``type: drive``. Saves report data in Google Drive. These are the
configurations:

-  profile: Name of the profile to use. Credentials of this profile must
   be ones of a service account with access to Google Drive API.
-  filename: Name for the resulting file.
-  folder: Directory in which the file will be stored. If not specified,
   the file is stored in the root of given drive. If there is more than
   one directory with the same name, the file will be stored in the
   first one this result finds (depends on Drive API).
-  folder\_id: Id of the directory in which the result will be saved. If
   specified, *folder* configuration will be ignored. You can get this
   id from the url in Google Drive web interface.
-  grant: Email of user, in the name of whom the file will be uploaded.
   Must have access to specified folder.
-  mime_type: Media type of the file to be uploaded. If none is specified
   it will take the type of the filename extension.

Example of drive result:

.. code:: json

    {
      "type": "drive",
      "profile": "my_service_drive_account",
      "filename": "report.xlsx",
      "folder": "TestFolder",
      "grant": "me@mail.com"
    }

Amazon S3
^^^^^^^^^

.. note:: To use S3 result you must install ``s3`` dependency:
    ``pip install laika-lib[s3]``

``type: s3``. Saves the result in Amazon S3.

Configuration:

-  profile: Name of profile to use (laika profile, no to confuse with
   aws profiles). Credentials file of the specified profile must contain
   data to be passed to
   `Session <http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session>`__
   constructor. Example of a minimal aws credentials file for laika:

``json   {     "aws_access_key_id": "my key id",     "aws_secret_access_key": "my secret access key"   }``

-  bucket: s3 bucket in which you want to save your data.
-  filename: Name of the file to save. This config is the *key* of the
   file in bucket.

Example of s3 result:

.. code:: json

    {
      "type": "s3",
      "profile": "my_aws_profile",
      "bucket": "some.bucket",
      "filename": "reports/custom_report.csv"
    }

SFTP
^^^^

``type: sftp``. Uploads the data to a SFTP server. Configurations for this
kind of result are:

-  profile: Name of the profile to use. Credentials file must have
   ``username`` and optionally ``password`` fields and/or ``private_key`` to
   authenticate in the SFTP service. ``private_key`` should be a path to a file
   with the private key.
-  connection: Name of a connection of ftp type.
-  folder: Folder in which the file will be saved. Can be a unix style path.
-  filename: Name with which the file will be uploaded to ftp.

Example of SFTP result:

.. code:: json

    {
      "type": "sftp",
      "profile": "my_sftp_profile",
      "connection": "some_sftp",
      "folder": "./some_folder/",
      "filename": "my_report.csv"
    }

Redash
^^^^^^

``type: redash``. Saves the data as *json* file in format which redash
understands. You can then expose it to redash via API, redash will be
able to consume it using url datasource. Configuration has the same
fields as `File <#file>`__ result, with the exception of the fact that
the file must be json (it will be saved as json, regardless of the
extension).


Fixed Columnar Result
^^^^^^^^^^^^^^^^^^^^^

``type: fixed``. Wrapper result that ensures the presence of a list of columns
in the data before sending them to an inner result. Columns not present in the
data will be added. Can only be used with reports that return a ``pandas.DataFrame``
as result (or some data structure accepted by DataFrame's constructor). All the
configuration keys, besides ones this result defines, will be passed to the
inner result. Can be useful if you need to adapt the data to some external
format (i.e. Hive schema).

Configuration:

-  columns: List of columns to leave in the data, in the order you want them
   to appear for the inner result.
-  inner_result_type: Type of result to use after fixing the data.
-  default_value: This value will be used to fill missing columns with
   (``np.nan`` by default).


Example of fixed columnar result:

.. code:: json

    {
      "type": "fixed",
      "columns": ["id", "date", "action", "value", "missing_column"],
      "default_value": "value_to_fill_missing_column_with",
      "inner_result_type": "file",
      "filename": "resulting_output.csv"
    }


As you can see in the example, you define both configurations for the fixed
columnar result, and the result it wraps (in this case a file result, with it's
corresponding filename). Only the columns defined in the configuration will be
passed to the inner result.


Partitioned Result
^^^^^^^^^^^^^^^^^^

``type: partitioned``. Wrapper result that partitions incoming data using one
of it's columns as a partition key. For each obtained partition an inner result
will be executed, with the data corresponding to the partition. The partition
key is passed to each inner result via ``partition_group`` variable, that can
be used in templates (see more in :ref:`filenames-templating`).
This result can only be used with reports that return a ``pandas.DataFrame``
(or some data structure accepted by DataFrame's constructor). All the
configuration keys, besides ones this result defines, will be passed to the
inner result.


Configuration:
 - partition_key: Name of the column to use as partition key. This field is
   required.
 - partition_date_format: Optional, if defined, partition key will be converted
   to a string with the provided format. Partition key must have datetime type,
   or be convertable to datetime trough `pandas.to_datetime <http://pandas.pydata.org/pandas-docs/version/0.19.2/generated/pandas.to_datetime.html>`__. The format
   must follow Python's `datetime.strftime guidelines <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`__.
 - inner_result_type: Type of result to for inner results.


Example of partitioned result:


.. code:: json

    {
      "type": "partitioned",
      "partition_key": "my_date",
      "partition_date_format": "%Y-%m",
      "inner_result_type": "file",
      "filename": "report_{partition_group}.csv"
    }


In this example, the incoming data will be partitioned by "my_date" column,
previously converted to *YYYY-MM* format (which will fail if "my_date" column
is not a date or datetime, nor it is directly convertable to one). Each of the
resulting partitions will be saved in a separate file. So if, for example,
"my_date" has dates in April and in May of 2019, this example will result in
two files, ``report_2019-04.csv`` and ``reports_2019-05.csv``.


Module
^^^^^^

``type: module``. Allows you to use a python module with custom result
class to save the data. This module will be loaded dynamically and
executed.

Configuration:

-  result\_file: Path to python file.
-  result\_class: Name of the class to use as result inside the python
   file. This class must inherit ``Result`` class and define ``save``
   method. Simple example of a custom result class:

   .. code:: python

       from laika.reports import Result

       class FooResult(Result):

           def save(self):
               # using some custom configs
               filename = self.custom_filename
               # doing the actual save
               print str(self.data)

This result will be executed as any other result - it will have
available all the extra configuration you define.

.. Warning:: this result will load and execute arbitrary code, which implies a
   series of security holes. Always check custom modules before using them.

Example of a module result definition:

.. code:: json

    {
      "type": "module",
      "result_file": "./some_folder/my_custom_result.py",
      "result_class": "MyResult",
      "my_custom_config": "value"
    }
