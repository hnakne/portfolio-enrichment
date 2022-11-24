import datetime

from bs4 import BeautifulSoup


def value_by_text_key(li_element: BeautifulSoup, text: str):
    key_element = li_element.find('span', text=text)

    return list(key_element.parent.children)[1] if key_element else None


def parse_portfolio_list_element(list_element: BeautifulSoup):
    r = {
            # 'raw_html': str(list_element)
    }
    try:
        name = list_element.find('span', class_='inline-block')
        country_elem = value_by_text_key(list_element, 'Country')
        sector_elem = value_by_text_key(list_element, 'Sector')
        fund_elem = value_by_text_key(list_element, 'Fund')
        entry_elem = value_by_text_key(list_element, 'Entry')
        exit_elem = value_by_text_key(list_element, 'Exit')
        if name: r['name'] = name.text
        if country_elem: r['country'] = country_elem.text
        if sector_elem: r['sector'] = sector_elem.text
        if entry_elem: r['entry'] = entry_elem.text
        if entry_elem: r['entry'] = entry_elem.text
        if exit_elem: r['exit'] = exit_elem.text
        if fund_elem:
            r['fund'] = fund_elem.text
            hyperlink = fund_elem.find('a')
            if hyperlink:
                fund_link = hyperlink['href']
                r['fund_link'] = fund_link

    except Exception as e:
        r['parse_error'] = str(e)

    return r


def parse_portfolio(portfolio_soup: BeautifulSoup) -> list:
    items_in_portfolio = portfolio_soup \
        .find("div", class_="order-last") \
        .find("ul") \
        .find_all("li", class_="flex", recursive=False)

    portfolio_items = list(map(lambda i: parse_portfolio_list_element(i), list(items_in_portfolio)))
    return portfolio_items
