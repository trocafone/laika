
import pandas as pd
from mock import patch, MagicMock
from unittest import TestCase

from laika.reports import Config, Runner


class LaikaTest(TestCase):
    """ Integration test for reporter components. """

    def setUp(self):
        self.config = {
            'profiles': [
            ],
            'connections': [
                {
                  'name': 'local',
                  'type': 'postgre',
                  'constring': 'postgresql://local@localhost:5432/local_db'
                }
            ],
            'reports': [
                {
                    'name': 'some_query',
                    'type': 'query',
                    'connection': 'local',
                    'query_file': 'query.sql',
                    'results': [
                        {
                          "type": "file",
                          "filename": "report.csv"
                        }
                    ]
                }
            ]
        }
        self.pd_sql_query = patch('pandas.read_sql_query').start()
        self.pd_write_csv = patch('pandas.DataFrame.to_csv').start()
        # TODO: rewrite test to not use sqlalchemy
        self.create_engine = patch('sqlalchemy.create_engine').start()

    def tearDown(self):
        patch.stopall()

    def test_simple_report(self):
        config = Config(self.config)
        self.assertEqual(config['reports']['some_query']['type'], 'query')

        query = 'select foo from bar;'
        res = pd.DataFrame([[1, 1], [2, 2]])
        self.pd_sql_query.return_value = res
        with patch('__builtin__.open', create=True) as mock_open:
            f = MagicMock(spec=file)
            mock_open.return_value = f
            f.__enter__.return_value.read.return_value = query
            runner = Runner(config)
            runner.run()

        self.create_engine.assert_called_once_with(self.config['connections'][0]['constring'])
        expected_con = self.create_engine.return_value
        self.pd_sql_query.assert_called_once_with(query, con=expected_con)

        self.pd_sql_query.return_value.to_csv.assert_called_once_with('report.csv', encoding='utf-8', float_format=None, header=True, index=True)
