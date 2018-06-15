
from datetime import datetime
from unittest import TestCase

try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from laika.reports import ReportFormatter, FilenameFormatter


class ReportFormatterTest(TestCase):

    def setUp(self):
        now = datetime(2016, 2, 12, 18, 19, 9)
        self._p_now = patch('laika.reports.ReportFormatter.get_now', Mock(return_value=now)).start()
        self.formatter = ReportFormatter({})

    def tearDown(self):
        self._p_now.stop()

    def test_formatter_take_days(self):
        self.assertEqual(self.formatter.format('{now}'), '2016-02-12 18:19:09')
        self.assertEqual(self.formatter.format('{now-1d}'), '2016-02-11 18:19:09')
        self.assertEqual(self.formatter.format('{now-12d}'), '2016-01-31 18:19:09')

    def test_formatter_add_days(self):
        self.assertEqual(self.formatter.format('{now+1y}'), '2017-02-12 18:19:09')
        self.assertEqual(self.formatter.format('{now+18d}'), '2016-03-01 18:19:09')

    def test_formatter_change_time(self):
        self.assertEqual(self.formatter.format('{now+15h}'), '2016-02-13 09:19:09')
        self.assertEqual(self.formatter.format('{t-3m}'), '2015-11-12 00:00:00')

    def test_year(self):
        self.assertEqual(self.formatter.format('{Y}'), '2016-01-01 00:00:00')

    def test_formatter_start_of_week(self):
        self.assertEqual(self.formatter.format('{w}'), '2016-02-08 00:00:00')
        self.assertEqual(self.formatter.format('{w-3d}'), '2016-02-05 00:00:00')
        self.assertEqual(self.formatter.format('{w-3w}'), '2016-01-18 00:00:00')


class FilenameFormatterTest(TestCase):

    def setUp(self):
        now = datetime(2016, 2, 12, 18, 19, 9)
        self._p_now = patch('laika.reports.ReportFormatter.get_now', Mock(return_value=now)).start()
        self.formatter = FilenameFormatter({})

    def tearDown(self):
        self._p_now.stop()

    def test_file_formatter_change_months(self):
        self.assertEqual(self.formatter.format('{m}'), '02')

        self.assertEqual(self.formatter.format('{m-1m}'), '01')
        self.assertEqual(self.formatter.format('{m-1d}'), '02')
        self.assertEqual(self.formatter.format('{m-12d}'), '01')

        self.assertEqual(self.formatter.format('{m+1m}'), '03')
        self.assertEqual(self.formatter.format('{m+1d}'), '02')
        self.assertEqual(self.formatter.format('{m+18d}'), '03')

    def test_file_formatter_change_days(self):
        self.assertEqual(self.formatter.format('{d}'), '12')

        self.assertEqual(self.formatter.format('{d-1d}'), '11')
        self.assertEqual(self.formatter.format('{d-12d}'), '31')

        self.assertEqual(self.formatter.format('{d+8d}'), '20')
        self.assertEqual(self.formatter.format('{d+18d}'), '01')

    def test_file_formatter_change_years(self):
        self.assertEqual(self.formatter.format('{y}'), '2016')
        self.assertEqual(self.formatter.format('{y+1y}'), '2017')
        self.assertEqual(self.formatter.format('{y-1y}'), '2015')

        self.assertEqual(self.formatter.format('{Y-1m}'), '2016')
        self.assertEqual(self.formatter.format('{Y-3m}'), '2015')
        self.assertEqual(self.formatter.format('{Y+6m}'), '2016')
        self.assertEqual(self.formatter.format('{Y+11m}'), '2017')

        self.assertEqual(self.formatter.format('{Y-1d}'), '2016')
        self.assertEqual(self.formatter.format('{Y-43d}'), '2015')
        self.assertEqual(self.formatter.format('{Y+67d}'), '2016')
        self.assertEqual(self.formatter.format('{Y+325d}'), '2017')

        self.assertEqual(self.formatter.format('{h+15h}'), '09')
        self.assertEqual(self.formatter.format('{m-3m}'), '11')
        self.assertEqual(self.formatter.format('{Y-3m}'), '2015')

    def test_file_formatter_weeks_and_mondays(self):
        # a week ago
        self.assertEqual(self.formatter.format('{d-1w}'), '05')
        # three weeks ago
        self.assertEqual(self.formatter.format('{d-3w}'), '22')
        # This monday
        self.assertEqual(self.formatter.format('{d-1f}'), '08')
        # third monday from now
        self.assertEqual(self.formatter.format('{d-3f}'), '25')

        self.assertEqual(self.formatter.format('{d+1w}'), '19')
        self.assertEqual(self.formatter.format('{d+3w}'), '04')
        self.assertEqual(self.formatter.format('{d+1f}'), '15')
        self.assertEqual(self.formatter.format('{d+3f}'), '29')

    def test_file_formatter_weeks_and_mondays_for_month(self):
        self.assertEqual(self.formatter.format('{m-1w}'), '02')
        self.assertEqual(self.formatter.format('{m-3w}'), '01')
        self.assertEqual(self.formatter.format('{m-1f}'), '02')
        self.assertEqual(self.formatter.format('{m-3f}'), '01')

        self.assertEqual(self.formatter.format('{m+1w}'), '02')
        self.assertEqual(self.formatter.format('{m+3w}'), '03')
        self.assertEqual(self.formatter.format('{m+1f}'), '02')
        self.assertEqual(self.formatter.format('{m+3f}'), '02')

    def test_returns_the_string_if_nothing_to_format(self):
        self.assertEqual(self.formatter.format('foo'), 'foo')
        self.assertEqual(self.formatter.format('foo bar baz!!1'), 'foo bar baz!!1')
