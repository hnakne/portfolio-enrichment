from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

CURRENT_PORTFOLIO_FUNDS_URL = 'https://eqtgroup.com/current-portfolio/funds'

CURRENT_PORTFOLIO_URL = 'https://eqtgroup.com/current-portfolio'

drivers = []


def get_chrome_driver() -> WebDriver:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    d = webdriver.Chrome(options=options, executable_path='chromedriver')
    drivers.append(d)
    return d


def get_page_source(web_driver: WebDriver, url: str) -> BeautifulSoup:
    web_driver.get(url)
    return web_driver.page_source


def soup_from_string(page_source: str) -> BeautifulSoup:
    return BeautifulSoup(page_source, "html.parser")


def save_to_file(filename: str, content: str, ):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def parse_portfolio_list_element(list_element: BeautifulSoup):
    r = {
            'raw_html': str(list_element)
    }
    try:
        name = list_element.find('span', class_='inline-block')
        country = value_by_text_key(list_element, 'Country')
        sector_elem = value_by_text_key(list_element, 'Sector')
        fund_elem = value_by_text_key(list_element, 'Fund')
        entry_elem = value_by_text_key(list_element, 'Entry')
        r['name'] = name
        r['country'] = country.text
        r['sector'] = sector_elem.text
        r['entry'] = entry_elem.text
        r['fund'] = fund_elem.text

        hyperlink = fund_elem.find('a')
        if hyperlink:
            fund_link = hyperlink['href']
            r['fund_link'] = fund_link
    except Exception as e:
        r['parse_error'] = str(e)

    return r


def value_by_text_key(li_element: BeautifulSoup, text: str):
    return list(li_element.find_all('span', text=text)[0].parent.children)[1]


def parse_portfolio(portfolio_soup: BeautifulSoup) -> list:
    items_in_portfolio = portfolio_soup \
        .find("div", class_="order-last") \
        .find("ul") \
        .find_all("li", class_="flex", recursive=False)

    portfolio_items = list(map(lambda i: parse_portfolio_list_element(i), list(items_in_portfolio)))
    # for name in elems:
    #     print(name)
    errors = filter(lambda e: 'parse_error' in e, portfolio_items)
    print(f'Found {len(items_in_portfolio)} portfolio items on {CURRENT_PORTFOLIO_URL}')
    print(f'# of unparsable lines: {len(list(errors))}')
    valid_elems = list(filter(lambda e: 'parse_error' not in e, portfolio_items))
    print(f'# of parsed lines: {len(valid_elems)}')
    return portfolio_items


if __name__ == '__main__':
    driver = get_chrome_driver()
    # portfolio_url = CURRENT_PORTFOLIO_URL
    # funds_page = CURRENT_PORTFOLIO_FUNDS_URL

    porfolio_source = get_page_source(driver, CURRENT_PORTFOLIO_URL)
    save_to_file('current_portfolio.html', porfolio_source)
    portfolio = soup_from_string(porfolio_source)
    out = parse_portfolio(portfolio)

    funds_source = get_page_source(driver, CURRENT_PORTFOLIO_FUNDS_URL)
    save_to_file('current_portfolio_funds.html', funds_source)
    # //*[@id="content"]/div[2]/div/div
    # /html/body/div[1]/div[1]/div[6]/div[2]/div[2]/div/div

    funds = soup_from_string(funds_source)

    # for page in pages:
    #     html = get_page_html(get_chrome_driver, )
