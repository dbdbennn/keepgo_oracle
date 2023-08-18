import datetime

system_date_format = '%Y-%m-%d'


def isDate(input_date):
    try:
        datetime.datetime.strptime(input_date, system_date_format)
        return True
    except ValueError:
        return False
