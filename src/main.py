import datetime
import json
import os.path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.portfolio_parsing import parse_portfolio

DIVESTMENTS_HTML_FILE_NAME = 'current_portfolio_divestments.html'

CURRENT_PORTFOLIO_HTML_FILE_NAME = 'current_portfolio.html'

CURRENT_PORTFOLIO_FUNDS_URL = 'https://eqtgroup.com/current-portfolio/funds'

CURRENT_PORTFOLIO_URL = 'https://eqtgroup.com/current-portfolio'
CURRENT_PORTFOLIO_DIVESTMENTS_URL = 'https://eqtgroup.com/current-portfolio/divestments'

drivers = []


def get_chrome_driver() -> WebDriver:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    d = webdriver.Chrome(options=options, executable_path='chromedriver')
    drivers.append(d)
    return d


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


def check_and_print_metrics(items: list, url: str):
    print(f'URL: {url}')
    errors = filter(lambda e: 'parse_error' in e, items)
    print(f'# of unparsable lines: {len(list(errors))}')
    valid_elems = list(filter(lambda e: 'parse_error' not in e, items))
    print(f'# of parsed lines: {len(valid_elems)}')


def save_to_json(output_file_name: str, l: list):
    with open(output_file_name, 'w') as f:
        for d in l:
            json.dump(d, f)
    f.close()


if __name__ == '__main__':
    driver = get_chrome_driver()

    portfolio_source = get_page_source(driver, CURRENT_PORTFOLIO_URL, CURRENT_PORTFOLIO_HTML_FILE_NAME)
    portfolio = soup_from_string(portfolio_source)

    portfolio_divestments_source = get_page_source(driver, CURRENT_PORTFOLIO_DIVESTMENTS_URL,
                                                   DIVESTMENTS_HTML_FILE_NAME)
    divestments = soup_from_string(portfolio_divestments_source)

    now = datetime.datetime.now()
    portfolio_items = parse_portfolio(portfolio)
    check_and_print_metrics(portfolio_items, CURRENT_PORTFOLIO_URL)

    divestment_items = parse_portfolio(divestments)
    check_and_print_metrics(divestment_items, CURRENT_PORTFOLIO_DIVESTMENTS_URL)


    save_to_json('output.json', portfolio_items + divestment_items)
