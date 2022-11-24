import datetime
from pathlib import Path


def build_dir_path(data_name, date: str):
    return f'output/{data_name}/{date}'


def make_dir_if_not_exists(directory: str):
    Path(directory).mkdir(parents=True, exist_ok=True)
