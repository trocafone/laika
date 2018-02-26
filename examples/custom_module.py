
from laika.reports import Result, BasicReport


class BarReport(BasicReport):

    def process(self):
        return 'Wow! Such data! Much custom!'


class FooResult(Result):

    def save(self):
        print str(self.data)
