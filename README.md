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

