import datetime
import json
import time
from pathlib import Path

import requests

EQT_DOMAIN = 'https://eqtgroup.com'
EQT_PAGE_DATA = 'https://eqtgroup.com/page-data'
PAGE_DATA_JSON = 'page-data.json'

divestments_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/divestments/page-data.json'
portfolio_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/page-data.json'


def save_to_json(dir: str, output_file_name: str, blob: dict):
    Path(dir).mkdir(parents=True, exist_ok=True)
    with open(f'{dir}/{output_file_name}', 'w') as f:
        json.dump(blob, f)
        f.close()


def save_to_json_by_item(dir: str, output_file_name: str, items: list):
    Path(dir).mkdir(parents=True, exist_ok=True)
    with open(f'{dir}/{output_file_name}', 'w') as f:
        for d in items:
            json.dump(d, f)
            f.write('\n')
        f.close()


def build_dir_path(data_name, date: datetime.date):
    return f'output/{data_name}/{date}'


def to_string(dt: datetime.date):
    return dt.isoformat()


# basic sanity checks
def validate(item):
    return 'title' in item and 'country' in item


def print_basic_metrics(items, url):
    print(f'URL: {url}')
    print(f'total {len(items)} fetched')
    valid_items = list(filter(lambda i: validate(i), items))
    print(f'total {len(valid_items)} valid')


# same structure
def items_from_page_data(j: dict):
    items = j['result']['data']['allSanityCompanyPage']['nodes']
    return items


def items_from_company_page(j: dict):
    items = j['result']['data']['sanityCompanyPage']
    return items


def enrich(items: list, source_url: str, blob_lookup: dict, date_str: str):
    for item in items:
        item['source_url'] = source_url
        item['date'] = date_str
        if 'path' in item and item['path'] in blob_lookup:
            item['company_details'] = blob_lookup[item['path']]
    return items


def curl_and_get(url: str) -> dict:
    time.sleep(0.05)  # hide "client details
    print(f"getting contents of {url}")  # debug logging
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f'Not 200: {str(r)}')


def build_page_data_from_path(path: str) -> str:
    return f'{EQT_PAGE_DATA}{path}/{PAGE_DATA_JSON}'


def extract_path(item):
    if 'path' in item and item['path']:
        path = item['path']
        if path.startswith('/'):
            return path

    return None


def lookup_urls(paths):
    paths = set(paths)
    r = {}
    for path in paths:
        full_url = build_page_data_from_path(path)
        blob = curl_and_get(full_url)
        r[path] = items_from_company_page(blob)
    return r


def process(page_data_response: dict, url: str, date: datetime.date) -> (dict, list):
    items = items_from_page_data(page_data_response)
    paths = list(filter(lambda p: p is not None, map(lambda i: extract_path(i), items)))
    blob_by_path = lookup_urls(paths)
    enriched_items = enrich(items=items, source_url=url, blob_lookup=blob_by_path, date_str=to_string(date))
    return enriched_items


# todo - add checks if data is already written. Handle with Override/backfill flag.
def save(data_source_name: str, items: list, date: datetime.date):
    directory = build_dir_path(data_source_name, date)
    save_to_json_by_item(dir=directory, output_file_name='output.json', items=items)


def main_curl():
    today = datetime.date.today()
    # separate from divestments
    portfolio_data = curl_and_get(portfolio_page_data_url)
    enriched_portfolio_items = process(portfolio_data, portfolio_page_data_url, date=today)
    print_basic_metrics(enriched_portfolio_items, portfolio_page_data_url)
    save('portfolio', enriched_portfolio_items, today)

    divestments_data = curl_and_get(divestments_page_data_url)
    enriched_divestment_items = process(divestments_data, divestments_page_data_url, date=today)
    print_basic_metrics(enriched_divestment_items, divestments_page_data_url)
    save('divestments', enriched_divestment_items, today)


if __name__ == '__main__':
    main_curl()
