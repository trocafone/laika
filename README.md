
# Laika

![laika_stamp](http://3.bp.blogspot.com/_r7sReQYd6vU/R_eomB1FWfI/AAAAAAAAAVM/PBKP7ng7KVA/s400/Romania_Laika.jpg)

*laika* is a business reporting library that allows you to request data from different sources and send it to someone or save it at some destination. For example: you can query your database, send the result as an excel attachment via email and save it on Google Drive or Amazon S3.

Check out the documentation at [readthedocs](http://laika.readthedocs.io/en/latest/index.html).

<!-- TODO: document what it is and what it is not -->

Laika was tested on Python 2.7 and 3.5 or higher.

## Installation

You can install it directly using `pip`:

```bash
$ pip install laika-lib
```

You can specify extra dependencies. To find out what dependencies you need to install, check out reports and results documentation. For example, to install libraries to use Google Drive and Amazon S3 in your reports you must run:

```bash
$ pip install laika-lib[drive, s3]
```

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


## Testing

To run test, you must install test dependencies:

```bash
$ pip install laika-lib[test]
```

Then, run test from laika directory:

```bash
$ cd path/to/laika
$ python -m unittest discover
```
