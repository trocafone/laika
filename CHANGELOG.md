# Changelog

## [Unreleased]

## [1.4.0] - 2020-07-12

 - Updated Facebook Graph API version to v10.0
 - Updated RTBHouse API version to 5
 - Allow overwriting configuration values from cli
 - Added BingAds report

## [1.3.8] - 2020-02-04

 - Patch PyDrive to work with new version of httplib2

## [1.3.7] - 2020-02-03

 - Fixed interaction between google api and httplib2 libraries

## [1.3.6] - 2020-01-30

 - Added support for shared drives in Google Drive report and result
 - Reash parameters can now be templated

## [1.3.5] - 2019-12-18

 - Updated Facebook API version to 5.0

## [1.3.4] - 2019-09-11

 - FileResult now accepts extra arguments for pandas io methods
 - Allow specifying plain sql queries instead of files

## [1.3.3] - 2019-08-16

 - RTBHouse report now uses API instead of sdk

## [1.3.2] - 2019-07-02

 - Paramiko upgraded to 2.6.0

## [1.3.1] - 2019-06-10

 - Google Drive API calls now are retried on unexpected errors

## [1.3.0] - 2019-05-24

 - Credentials can now be specified through environment variable
 - Added Partitioned Result
 - Updated required pandas version to 0.23.4
 - Updated required psycopg2 version to 2.7.7
 - Updated Facebook API version to 3.3

## [1.2.2] - 2019-05-17

 - Updated Facebook API version to 3.2
 - Updated required googleads version to 19.0.0

## [1.2.1] - 2019-03-21

 - Updated adwords version to v201809

## [1.2.0] - 2019-02-15

 - Added reports from RTBHouse and Rakuten
 - Added fixed columnar result
 - Added a possiblity to configure Adwords and Facebook reports with relative dates.
 - Added an option to refresh a Redash query before downloading
 - Added a parameter/configuration to override current date.
 - Updated Facebook API version to 3.1
 - Updated required requests version to >= 2.21.0
 - Updated required SQLAlchemy version to == 1.2.17
 - Added presto optional dependency

## [1.1.1] - 2018-09-10

 - Added password parameter to SFTP result
 - Fixed mime_type parameter for Google Drive result

## [1.1.0] - 2018-06-24

 - Added Python 3 support (>= 3.5)
 - Updated adwords version to v201806

## [1.0.1] - 2018-05-17

 - Bugfixes

## [1.0.0] - 2018-05-09

 - First release
