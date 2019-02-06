
from laika.reports import Result, FormattedReport


class BarReport(FormattedReport):

    def process(self):
        current_date = self.formatter.format('{t}')
        return 'Wow! Such data! Much custom! Even with a date: ' + current_date


class FooResult(Result):

    def save(self):
        print(str(self.data))
