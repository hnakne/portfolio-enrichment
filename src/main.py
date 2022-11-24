import datetime
import json
import os.path
import requests
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from portfolio_parsing import parse_portfolio

divestments_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/divestments/page-data.json'

portfolio_page_data_url = 'https://eqtgroup.com/page-data/current-portfolio/page-data.json'

DIVESTMENTS_HTML_FILE_NAME = 'current_portfolio_divestments.html'

PORTFOLIO_HTML_FILE_NAME = 'current_portfolio.html'

PORTFOLIO_FUNDS_URL = 'https://eqtgroup.com/current-portfolio/funds'

PORTFOLIO_URL = 'https://eqtgroup.com/current-portfolio'
DIVESTMENTS_URL = 'https://eqtgroup.com/current-portfolio/divestments'


def get_chrome_driver() -> WebDriver:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    return webdriver.Chrome(options=options, executable_path='chromedriver')


def get_page_source(web_driver: WebDriver, url: str, file_name=None) -> str:
    if file_name and os.path.exists(file_name):
        with open(file_name, 'r') as f:
            r = f.read()
            f.close()
            return r
    web_driver.get(url)
    page_source = web_driver.page_source
    with open(file_name, 'w') as f:
        f.write(page_source)
        f.close()
    return page_source


def soup_from_string(page_source: str) -> BeautifulSoup:
    return BeautifulSoup(page_source, "html.parser")


def sanity_check(item: dict):
    return 'name' in item and 'fund' in item


def check_and_print_metrics(items: list, url: str):
    print(f'URL: {url}')
    errors = filter(lambda e: 'parse_error' in e, items)
    print(f'# of unparsable lines: {len(list(errors))}')
    valid_elems = list(filter(lambda e: 'parse_error' not in e and sanity_check(e), items))
    print(f'# of parsed lines: {len(valid_elems)}')


def save_to_json(dir: str, output_file_name: str, l: list):
    Path(dir).mkdir(parents=True, exist_ok=True)
    with open(output_file_name, 'w') as f:
        for d in l:
            json.dump(d, f)
            f.write('\n')
    f.close()


def build_dir_path(date, data_name):
    return f'output/{data_name}/{date}'


def today_as_string():
    return datetime.date.today().isoformat()


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


def enrich(items: list, url: str, date: str):
    for item in items:
        item['source_url'] = url
        item['date'] = date
    # don't have to return but easier to reason about
    return items


def curl_and_get(url: str) -> dict:
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f'Not 200: {str(r)}')


def process(page_data_response: dict, url: str, date: str) -> (dict, list):
    items = items_from_page_data(page_data_response)
    enriched_portfolio_items = enrich(items=items, url=url, date=date)
    return enriched_portfolio_items


def main_curl():
    today_str = today_as_string()
    # separate from divestments
    portfolio_data = curl_and_get(portfolio_page_data_url)
    enriched_portfolio_items = process(portfolio_data, portfolio_page_data_url, str)
    print_basic_metrics(enriched_portfolio_items, portfolio_page_data_url)
    save_to_json(f'output/output_portfolio_{today_str}.json', enriched_portfolio_items)

    divestments_data = curl_and_get(divestments_page_data_url)
    enriched_divestment_items = process(divestments_data, divestments_page_data_url, date=today_str)
    print_basic_metrics(enriched_divestment_items, divestments_page_data_url)
    save_to_json(f'output/output_divestments_{today_str}.json', enriched_portfolio_items)

    output = enriched_divestment_items + enriched_portfolio_items
    save_to_json()


def main(args: list):
    output = []

    driver = get_chrome_driver()
    driver.get('https://eqtgroup.com/page-data/current-portfolio/page-data.json')

    if 'portfolio' in args:
        driver = get_chrome_driver()
        portfolio_source = get_page_source(driver, PORTFOLIO_URL, PORTFOLIO_HTML_FILE_NAME)
        driver.close()
        portfolio = soup_from_string(portfolio_source)

        portfolio_items = parse_portfolio(portfolio)
        output = output + portfolio_items
        check_and_print_metrics(portfolio_items, PORTFOLIO_URL)

    if 'divestments' in args:
        driver = get_chrome_driver()
        divestments_source = get_page_source(driver, DIVESTMENTS_URL, DIVESTMENTS_HTML_FILE_NAME)
        driver.close()
        divestments = soup_from_string(divestments_source)

        divestment_items = parse_portfolio(divestments)
        output = output + divestment_items
        check_and_print_metrics(divestment_items, DIVESTMENTS_URL)

    save_to_json('output/output_portfolio.json', output)
    # todo enrich with fund and details data
    # input/output by time/date


if __name__ == '__main__':
    # args = sys.argv[1:]
    # main(args)
    main_curl()
