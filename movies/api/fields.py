from django.forms import ValidationError, Field
from movies.api.mixins import DateParsable

class DateFromStringField(DateParsable, Field):
    def to_python(self, value):
        try:
            date = self.date_from_string(value)
        except Exception:
            raise ValidationError("Wrong format, accepted format is 01 Jan 2000")
        return date

    def to_representation(self, value):
        return value.strftime('%d %b %Y')

    def to_internal_value(self, value):
        self.to_python(value)
