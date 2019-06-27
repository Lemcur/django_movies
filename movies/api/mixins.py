import datetime

class DateParsable():
    def date_from_string(self, value, format='%d %b %Y'):
        return datetime.datetime.strptime(value, '%d %b %Y').date()
