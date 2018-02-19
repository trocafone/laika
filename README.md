# Reports

*reports* is a business reporting library that allows you to request data from different sources and send it to someone as or save it at some destination. For example: you can query your database, send the result as an excel attachment via email and save it on Google Drive or Amazon S3.

TODO: document what it is and what it is not

## Installation

TODO: document this

## Usage

Reporter is a script that lets you use reports library. You can run it like this:

```bash
$ reporter.py some_report
```

This command will run the report named *some_report*. This report must be defined in some configuration file. By default reporter looks for `config.json` in the same directory. You can specify a custom config passing `-c` parameter:

```bash
$ reporter.py -c my_config.json
```

Path to configuration file can also be specified with the `REPORTER_CONFIG_FILE_PATH` environment variable:

```bash
$ export REPORTER_CONFIG_FILE='/home/me/my_config.json'
./reporter.py my_report
```

Another parameter you can use is `--pwd` which server for specifying working directory. It can also be specified in configuration file or `REPORTER_PWD` environment variable.

### Arguments

You can check all the predefined reporter arguments with `--help`.

Undefined arguments will be added to reports definition overwriting default values. Thus, if for example the configuration for `my_report` defines field `my_field` with value `foo`, if you call it like this:

```bash
$ ./reporter.py my_report --my_field bar
```

`my_field` configuration will contain `bar` as value.


## Configuration

Reporter will read reports definition from a json file. The file must have this structure:

```json
{
  "include": [...],
  "profiles": [...],
  "connections": [...],
  "reports": [...]
}
```

The configuration can be separated in multiple files. You must have a base configuration file, which can have `"include"` field with a list of paths:

```json
"include": [
  "another_config.json",
  "/some/config.json"
]
```

This files will be included in the configuration. The only constraint is they only can have `reports`, `connections` and `profiles` field defined.

### Profiles

Profiles are all kind of credentials used for accessing external APIs (like Google Drive). You must specify a name and a path to credentials for each profile. For example:

```json
{
  "name": "my_drive",
  "credentials": "secret.json"
}
```

Credentials is always a json file, but it's format depends on each type of report or result. For example email credentials are defined like this:

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

Reports are json objects that must define these fields:

 - name: this name will be used to call the report through cli.
 - type: report's type. Supported report types are defined below.
 - results: list of results configuration that define how to save the reports ([Results documentation](#Results)).
 - Set of required or optional fields that are detailed below.

#### Query

`type: query`. This report runs a query to some database. Should work with any database supported by Sqlalchemy but right now it's only tested with PostgreSQL. These are the configurations:

 - query_file: path to a file that contains plane sql code.
 - connection: name of the connection to use.
 - variables: A dictionary with values to replace in query code. You can find further explanation in [Reports parametrization](#reports-parametrization)

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


#### Redash


