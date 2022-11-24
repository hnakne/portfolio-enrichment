import datetime
import json
import sys
import time
from pathlib import Path

import requests

from src.utils import build_dir_path, make_dir_if_not_exists

EQT_PAGE_DATA = 'https://eqtgroup.com/page-data'
PAGE_DATA_JSON = 'page-data.json'

divestments_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/divestments/page-data.json'
portfolio_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/page-data.json'
funds_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/funds/page-data.json'


def save_as_json(directory: str, output_file_name: str, json_blob: dict):
    make_dir_if_not_exists(directory)
    with open(f'{directory}/{output_file_name}', 'w') as f:
        json.dump(json_blob, f)
        f.close()


def save_as_json_per_item(directory: str, output_file_name: str, items: list):
    make_dir_if_not_exists(directory)
    with open(f'{directory}/{output_file_name}', 'w') as f:
        for d in items:
            json.dump(d, f)
            f.write('\n')
        f.close()


# basic sanity checks
def validate(item):
    return 'title' in item and 'country' in item


def print_basic_metrics(items, url):
    print(f'URL: {url}')
    print(f'total {len(items)} fetched')
    valid_items = list(filter(lambda i: validate(i), items))
    print(f'total {len(valid_items)} valid')


def get_active_funds(j: dict):
    active_funds = j['result']['data']['activeFunds']['nodes']
    return active_funds


def get_realised_funds(j: dict):
    active_funds = j['result']['data']['realizedFunds']['nodes']
    return active_funds


def items_from_portfolio_page_data(j: dict):
    items = j['result']['data']['allSanityCompanyPage']['nodes']
    return items


def items_from_company_page_page_data(j: dict):
    items = j['result']['data']['sanityCompanyPage']
    return items


def enrich(items: list, source_url: str, company_details_by_path: dict, date_str: str):
    for item in items:
        item['source_url'] = source_url
        item['date'] = date_str
        if 'path' in item and item['path'] in company_details_by_path:
            item['company_details'] = company_details_by_path[item['path']]
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
    paths = set(paths)  # don't do lookup > 1 per path
    r = {}
    for path in paths:
        full_url = build_page_data_from_path(path)
        blob = curl_and_get(full_url)
        r[path] = items_from_company_page_page_data(blob)
    return r


def process(page_data_response: dict, url: str, date: datetime.date) -> (dict, list):
    items = items_from_portfolio_page_data(page_data_response)
    paths = list(filter(lambda p: p is not None, map(lambda i: extract_path(i), items)))
    company_page_info_by_path = lookup_urls(paths)
    enriched_items = enrich(items=items, source_url=url, company_details_by_path=company_page_info_by_path,
                            date_str=date.isoformat())
    return enriched_items


# todo - add checks if data is already written. Handle with Override/backfill flag.
def save(data_source_name: str, items: list, date: datetime.date):
    directory = build_dir_path(data_source_name, date)
    save_as_json_per_item(directory=directory, output_file_name='output.json', items=items)


def save_blob(data_source_name: str, blob: dict, date: datetime.date):
    directory = build_dir_path(data_source_name, date)
    save_as_json(directory=directory, output_file_name='output.json', json_blob=blob)


def main(args):
    today = datetime.date.today()
    if 'portfolio' in args or len(args) == 0:
        fetch_and_store_portfolio(today)

    if 'divestments' in args or len(args) == 0:
        fetch_and_store_divestments(today)

    # TODO - parse funds
    # if 'funds' in args:
    #     funds_data = ???


def fetch_and_store_portfolio(today):
    portfolio_page_data = curl_and_get(portfolio_page_data_url)  # could be wrapped with some caching of responses
    save_blob('portfolio_raw', portfolio_page_data, today)  # not used, in real system good for debugging
    enriched_portfolio_items = process(portfolio_page_data, portfolio_page_data_url, date=today)
    print_basic_metrics(enriched_portfolio_items, portfolio_page_data_url)
    save('portfolio', enriched_portfolio_items, today)


def fetch_and_store_divestments(today):
    divestments_page_data = curl_and_get(divestments_page_data_url)
    save_blob('divestments_raw', divestments_page_data, today)  # not used, in real system good for debugging
    enriched_divestment_items = process(divestments_page_data, divestments_page_data_url, date=today)
    print_basic_metrics(enriched_divestment_items, divestments_page_data_url)
    save('divestments', enriched_divestment_items, today)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
