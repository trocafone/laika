# Laika

*laika* is a business reporting library that allows you to request data from different sources and send it to someone as or save it at some destination. For example: you can query your database, send the result as an excel attachment via email and save it on Google Drive or Amazon S3.

TODO: document what it is and what it is not

## Installation

TODO: document this

## Usage

`laika.py` is a script that lets you use laika library. You can run it like this:

```bash
$ laika.py some_report
```

This command will run the report named *some_report*. This report must be defined in some configuration file. By default laika looks for `config.json` in the same directory. You can specify a custom config passing `-c` parameter:

```bash
$ laika.py -c my_config.json
```

Path to configuration file can also be specified with the `LAIKA_CONFIG_FILE_PATH` environment variable:

```bash
$ export LAIKA_CONFIG_FILE_PATH='/home/me/my_config.json'
$ laika.py my_report
```

Another parameter you can use is `--pwd` which serves for specifying working directory. It can also be specified in configuration file or `LAIKA_PWD` environment variable.

### Arguments

You can check all the predefined `laika.py` arguments with `--help`.

Undefined arguments will be added to report's definition overwriting default values. Thus, if for example the configuration for `my_report` defines field `my_field` with value `foo`, if you execute it like this:

```bash
$ laika.py my_report --my_field bar
```

`my_field` configuration will contain `bar` as value.


## Configuration

Laika reads reports definitions from a json file which must have this structure:

```json
{
  "include": [...],
  "profiles": [...],
  "connections": [...],
  "reports": [...]
}
```

The configuration can be separated in multiple files. In this case there must be a base configuration file that will have to include the other files via `"include"` field with a list of paths:

```json
"include": [
  "another_config.json",
  "/some/config.json"
]
```

These files will be included in the configuration. The only constraint is they can only have `reports`, `connections` and `profiles` fields defined.

You can check the [example configuration file](config.json) for more information.

### Profiles

Profiles are all kind of credentials used for accessing external APIs (like Google Drive). You must specify a name and a path to credentials for each profile. For example:

```json
{
  "name": "my_drive",
  "credentials": "secret.json"
}
```

`credentials` is always a path to a json file, but it's format depends on each type of report or result. For example email credentials are defined like this:

```json
{
  "username": "me@gmail.com",
  "password": "secret"
}
```

### Connections

Connections are used to access data sources or destinations. They must have a *name* and a *type*, and a set of specific fields. Currently supported connections are described below.

#### Postgres

PostgreSQL database connection is defined like this:

```json
{
  "name": "local",
  "type": "postgre",
  "constring": "postgresql://user@localhost:5432/database"
}
```

#### Email

Example of a smtp connection:


```json
{
  "name": "gmail_smtp",
  "type": "email",
  "host": "smtp.gmail.com",
  "port": 587
}
```


#### Ftp

Example of a ftp connection:

```json
{
  "name": "some_ftp",
  "type": "ftp",
  "host": "ftp.home.com"
}
```


### Reports

Reports are defined as json objects that must define these fields:

 - name: this name will be used to execute the report through cli.
 - type: report's type. Supported report types are defined below.
 - results: list of results configuration that define how to save the reports ([Results documentation](#Results)).
 - Set of required or optional fields that are detailed below.


#### File

TODO: document

#### Query

`type: query`. This report runs a query to some database. Should work with any database supported by Sqlalchemy but right now it's only tested with PostgreSQL. These are the configurations:

 - query_file: path to a file that contains plane sql code.
 - connection: name of the connection to use.
 - variables: A dictionary with values to replace in query code. You can find further explanation in [Query templating](#query-templating)

Example of a *query* report:

```json
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
```

#### Bash Script

`type: bash`. This report executes a bash command and reads it's output. You can interpret this report as the `read_output` part of this example:

```bash
$ bash_script | read_output
```

These are the configurations:

 - script: command to execute
 - script_file: path to the file with bash script to execute. If *script* is defined, this field will be ignored.
 - result_type: type of output data format. Can be *csv*, *json* or *raw*. In case of *raw*, the content will not be converted and will be passed as is to the result. The explanation of *json* format is explained below.

Example bash script report:

```json
{
  "name": "some_bash_script",
  "type": "bash",
  "script_file": "some_script.sh",
  "result_type": "json",
  "results": [...]
}
```


##### Bash Script json format

Json data will be converted to a pandas dataframe using `pd.read_json` function ([Docs](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html)). These are some examples of the formats it accept:

*Example 1 (all arrays must have the same size)*:

```json
{
  "column_1": ["data_row_1", "data_row_2", "data_row_3"],
  "column_2": ["data_row_1", "data_row_2", "data_row_3"],
  ...
}
```

*Example 2*:

```json
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
```


#### Download From Google Drive

`type: drive`. This report downloads a file from Google Drive.

Configuration:

 - profile: Name of the profile to use. It's credentials must be ones of a service account with access to Google Drive's API.
 - grant: email of a grant account, in the name of which the document will be downloaded. Grant must have access to specified folder.
 - filename: name of the file to download.
 - folder: directory in which the report will search for the specified file.
 - folder_id: google drive's id of the above folder. If specified, folder option is ignored. It's useful if there is more than one folder with the same name.
 - subfolder: optional, if specified, this report will look for a subfolder inside a folder and, if found, will look there for filename. In other words, it will look for this structure: `<folder>/<subfolder>/<filename>`
 - file_id: google drive's id of the file to download. If specified, all other file options are ignored.


Example of a drive report:

```json
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
```



#### Download From S3

`type: s3`. This report downloads a file from Amazon S3. In order to use this report, you have to install [boto3](http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation).

Configuration:

 - profile: Name of profile to use (laika profile, no to confuse with aws profiles). Credentials file of the specified profile must contain data to be passed to [Session](http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session) constructor. Example of a minimal aws credentials file for laika:

  ```json
  {
    "aws_access_key_id": "my key id",
    "aws_secret_access_key": "my secret access key"
  }
  ```

  - bucket: s3 bucket to download the file from.
  - filename: File to download. This config is the *key* of the file in bucket.

Example of a s3 report:

```json
{
  "name": "s3_report_example",
  "type": "s3",
  "profile": "my_aws_profile",
  "bucket": "some.bucket",
  "filename": "reports/custom_report.csv",
  "results": [...]
}
```


#### Redash

`type: redash`. This report downloads query result from [redash](https://redash.io/) API. These are the configurations:

 - redash_url: the url of your redash instance.
 - query_id: id of the query to download. You can get from the query's url, it's last part is the id (for example, for `https://some.redash.com/queries/67`, 67 is the id).
 - api_key: token to access the query, either for user or for query. You can find user's token in the profile, token for query can be found in the source page.

Example of a redash query:

```json
{
  "name": "some_redash_query",
  "type": "redash",
  "api_key": "some api key",
  "query_id": "123",
  "redash_url": "https://some.redash.com",
  "results": [...]
}
```


#### Adwords

`type: adwords`. This report is generated by Google Adwords API. To use it, you will need to install [googleads](https://github.com/googleads/googleads-python-lib/). The configurations are:

 - profile: Name of profile to use. Credentials file is a *.yaml*, you can find out how to generate it in [adwords API tutorial](https://developers.google.com/adwords/api/docs/guides/start).
 - report_definition: the definition of the report which will be passed to [DownloadReport](http://googleads.github.io/googleads-python-lib/googleads.adwords.ReportDownloader-class.html#DownloadReport) method of googleads API. You will normally define fields `reportName`, `dateRangeType`, `reportType`, `downloadFormat`, `selector`, but these will vary depending on the report type.
 - reportName: In order not to repeat reports definitions, you can specify this name and reuse the definition. In other words, you can have multiple reports with the same name, but only one report_definition, which will be used for all of them.
 - dateRangeType: if you use report_definition from another report, you can overwrite date range it uses with this configuration.
 - [client_customer_id](https://support.google.com/adwords/answer/29198?hl=en). Id or list of ids of adwords customers, whose data you want in the report.

Example of adwords query:

```json
{
  "name": "some_adwords_report",
  "type": "adwords",
  "client_customer_id": "123-456-7890",
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
```


#### Facebook Insights

TODO: document


#### Module

TODO: document


### Results

Results are defined for each report in a list. Each result is an object, that must define *type* field. The rest of the fields depend on the type of result. Below are described all the supported results.

#### File

`type: file`. This result will save the data as a file. The configurations for this result are:

 - filename: path to the file. Depending on the file extension this file will be saved as excel (xls or xlsx), tsv or csv.

Example of a file result:

```json
"result": {
  "type": "file",
  "filename": "output.csv"
}
```


#### Email

`type: email`. Sends the data as an attachment in an email. Configurations for this result are:

 - connection: Name of a connection with type *email*.
 - profile: Profile name to use. Credentials from this profile must have `username` and `password` field from smtp service you will use.
 - filename: name of the file to attach.
 - recipients: one or more recipients for the email. Can be a string with one recipient or a list of recipients. This camp is required.
 - subject: subject of the email.
 - body: text the email will contain.
 - attachments: Optional. list of files to attach to the email. Must be a list of paths to files.


Subject and body can be formatted the same way filenames are formatted. You can find more about it in [Filenames templating](#filenames-templating). Example of email result:


```json
{
  "type": "email",
  "filename": "report_{Y}-{m}-{d}_{H}-{M}.xlsx",
  "recipients": ["some_recipient@mail.com", "another_recipient@foo.com"],
  "subject": "Some report",
  "body": "Report generated {Y}-{m}-{d} {H}:{M}. \nDo not reply this email!",
  "profile": "my_gmail",
  "connection": "gmail_smtp"
}
```

#### Ftp

`type: ftp`. Uploads the data to a ftp server. Configurations for this result are:

 - profile: Name of the profile to use. Credentials must have `username` and `password` fields to authenticate in the ftp service.
 - connection: Name of a connection of ftp type.
 - filename: Name with which the file will be uploaded to ftp.

Example of ftp result:

```json
{
  "type": "ftp",
  "profile": "my_ftp_profile",
  "connection": "some_ftp",
  "filename": "my_report.csv"
}
```


#### Google Drive

`type: drive`. Saves report data in Google Drive. These are the configurations:

 - profile: Name of the profile to use. Credentials of this profile must be ones of a service account with access to Google Drive API.
 - filename: Name for the resulting file.
 - folder: Directory, inside which the file will be stored. If not specified, the file is stored in the root of given drive. If there are more than one directory with the same name, the file will be stored in the first this result find (depends on Drive API).
 - folder_id: Id of the directory in which the result will be saved. If specified, *folder* configuration will be ignored. You can get this id from the url in Google Drive web interface.
 - grant: Email of user, in the name of whom the file will be uploaded. Must have access to specified folder.

Example of drive result:

```json
{
  "type": "drive",
  "profile": "my_service_drive_account",
  "filename": "report.xlsx",
  "folder": "TestFolder",
  "grant": "me@mail.com"
}
```


#### S3

`type: s3`. Saves the result in Amazon S3. In order to use this result, you have to install [boto3](http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation).

Configuration:

Configuration:

 - profile: Name of profile to use (laika profile, no to confuse with aws profiles). Credentials file of the specified profile must contain data to be passed to [Session](http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session) constructor. Example of a minimal aws credentials file for laika:

  ```json
  {
    "aws_access_key_id": "my key id",
    "aws_secret_access_key": "my secret access key"
  }
  ```

  - bucket: s3 bucket in which you want to save your data.
  - filename: Name of the file to save. This config is the *key* of the file in bucket.

Example of s3 result:

```json
{
  "type": "s3",
  "profile": "my_aws_profile",
  "bucket": "some.bucket",
  "filename": "reports/custom_report.csv"
}
```


#### Redash

`type: redash`. Saves the data as *json* file in format which redash understands. You can then expose it to redash via API, redash will be able to consume it using url datasource. Configuration has the same fields as [File](#file) result, with the exception of the fact that the file must be json (it will be saved as json, regardless of the extension).


#### Module

`type: module`. Allows you to use a python module with custom result class to save the data. This module will be loaded dynamically and executed.

Configuration:

 - result_file: Path to python file.
 - result_class: Name of the class to use as result inside the python file. This class must inherit `Result` class and define `save` method. Simple example of a custom result class:

    ```python
    from laika.reports import Result

    class FooResult(Result):

        def save(self):
            # using some custom configs
            filename = self.custom_filename
            # doing the actual save
            print str(self.data)
    ```

This result will be executed as any other result - it will have available all the extra configuration you define.

**Warning**: this will load and execute arbitrary code, which implies a series of security holes. Always check custom modules before using them.

Example of a module result definition:

```json
{
  "type": "module",
  "result_file": "./some_folder/my_custom_result.py",
  "result_class": "MyResult",
  "my_custom_config": "value"
}
```


### Global configuration

In addition to reports, connections and profiles you can define this configurations:

 - timezone: string of timezone to use. By default all the dates will be generated in UTC. You can overwrite it for each particular report.

 - pwd: directory, to which laika will change before executing reports. In this directory it will, for example, read query files, or save file results (if relative path is specified).

## Reports templating

In query definitions (or other templates inside laika) you can specify dynamic dates this way:

```sql
select * from some_table where date >= '{m}' and date < '{m+1m}'
```

laika will replace this dates by (supposing current month is February of 2016):

```sql
select * from some_table where date >= '2016-02-01 00:00:00' and date < '2016-03-01 00:00:00'
```

Dates are UTC by default, but you can modify that changing `timezone` configuration.

These are all the template variables you can use:

  - `{now}`: current date.
  - `{d}` o `{t}`: start of current date (00:00:00 of today)
  - `{m}`: start of first day of current month
  - `{y}`: start of current year (first day of January)
  - `{H}`: start of current hour
  - `{M}`: start of current minute
  - `{w}`: start of current week (Monday)

These variables may also receive modifiers. Modifier expression must start with one of these variables, continue with a sign (`+` o `-`), a number and finally, a measure. This measures can be:


  - `{y}`: years
  - `{m}`: months
  - `{d}`: days
  - `{h}`: hours
  - `{M}`: minutes
  - `{w}`: weeks

For example:

```
{now}, {now-1d}, {now+1y}, {now+15h}, {t-3m}
```

Results in:

ta en:

```
2016-02-12 18:19:09, 2016-02-11 18:19:09, 2017-02-12 18:19:09, 2016-02-13 09:19:09, 2015-11-12 00:00:00
```

Another possibility is to specify a start of week with `{f}`. For example, `{d-1f}` will move the date to Monday of the current week, and `{d+2f}` will mode the date to Monday within two weeks.

### Query templating

If the report have a dictionary of variables specified they will be replaced in the specified query file. For example, if you define a query like this:

```sql
select something from some_table where type = '{my_type}'
```

You can then pass the variables through configuration this way:

```json
{
  "variables": {
    "my_type": "some custom type"
  }
}
```

The query that will end up executing is this:

```sql
select something from some_table where type = 'some custom type'
```

These variables will be replaced first, and then laika will replace the dates, so you can define in your configuration variables like this:

```json
{
  "variables": {
    "yesterday": "{t-1d}"
  }
}
```

`{yesterday}` will be converted into `2016-02-12 17:19:09`.


### Filenames templating

`filename` configuration in all the reports and results can be formatted in a similar way. For example, if you specify:

```json
{
  "filename": "report_{Y}-{m}"
}
```

This will be formatted as `report_2016-02` (assuming the report ran in February of 2016).

You can also use the same modifiers:

```json
{
  "filename": "report_{Y}-{m-1m}"
}
```

Will result in `report_2016-01`.


## Testing

To run test, you must install test dependencies:

TODO: document

Then, run test from laika directory:

```bash
$ cd path/to/laika
$ python -m unittest discover
```
