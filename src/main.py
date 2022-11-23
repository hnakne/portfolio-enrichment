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


def get_page_html(page_source: str) -> BeautifulSoup:
    return BeautifulSoup(page_source, "html.parser")


def save_to_file(filename: str, content: str, ):
    f = open(filename, 'w')
    f.write(content)
    f.close()


if __name__ == '__main__':
    driver = get_chrome_driver()
    # portfolio_url = CURRENT_PORTFOLIO_URL
    # funds_page = CURRENT_PORTFOLIO_FUNDS_URL

    porfolio_content = get_page_source(driver, CURRENT_PORTFOLIO_URL)
    save_to_file('current_portfolio.html', porfolio_content)

    funds_content = get_page_source(driver, CURRENT_PORTFOLIO_FUNDS_URL)
    save_to_file('current_portfolio_funds.html', funds_content)

    # for page in pages:
    #     html = get_page_html(get_chrome_driver, )
