

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
You can find more about it in `Filenames
templating <#filenames-templating>`__. Example of email result:

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

.. note:: To use S3 result you must install ``drive`` dependency:
    ``pip install laika-lib[drive]``

``type: s3``. Saves the result in Amazon S3. In order to use this
result, you have to install
`boto3 <http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation>`__.

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
