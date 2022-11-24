import datetime


def build_dir_path(data_name, date: datetime.date):
    return f'output/{data_name}/{date}'
