
import six
import pandas as pd
from unittest import TestCase

try:
    from unittest.mock import patch, MagicMock, mock_open
except ImportError:
    from mock import patch, MagicMock, mock_open

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
        self.sqlalchemy_p = MagicMock()
        patch.dict("sys.modules", sqlalchemy=self.sqlalchemy_p).start()

    def tearDown(self):
        patch.stopall()

    def test_simple_report(self):
        config = Config(self.config)
        self.assertEqual(config['reports']['some_query']['type'], 'query')

        query = 'select foo from bar;'
        res = pd.DataFrame([[1, 1], [2, 2]])
        self.pd_sql_query.return_value = res
        open_s = six.moves.builtins.__name__
        with patch(open_s + '.open', mock_open(read_data=query)):
            runner = Runner(config)
            runner.run()

        constring = self.config['connections'][0]['constring']
        self.sqlalchemy_p.create_engine.assert_called_once_with(constring)
        expected_con = self.sqlalchemy_p.create_engine.return_value
        self.pd_sql_query.assert_called_once_with(query, con=expected_con)

        self.pd_sql_query.return_value.to_csv.assert_called_once_with('report.csv', encoding='utf-8', float_format=None, header=True, index=True)
