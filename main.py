import csv

from selenium import webdriver
from selectolax.parser import HTMLParser
from colorama import Fore
from dataclasses import dataclass
from pprint import pprint


@dataclass
class WhiskeyItem:
    title: str
    price: float
    currency: str
    img_src: str
    cl_and_per: str


def get_html(url: str) -> str:
    """ Getting html code of the page with selenium """

    driver = webdriver.Chrome()
    try:
        driver.get(url)
        driver.maximize_window()
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        return driver.page_source

    except Exception as ex:
        print(Fore.BLUE, ex)

    finally:
        driver.close()


def scrape(html: str) -> list:
    """ Scraping Page """

    html = HTMLParser(html)

    product_card = html.css('li.product-grid__item')

    res = []
    for info in product_card:
        item = WhiskeyItem(
            title=info.css_first('a.product-card').attributes['title'],
            price=float(info.css_first('p.product-card__price').text().replace('£', '').replace(',', '.').strip()),
            currency='EURO',
            img_src=info.css_first('img.product-card__image').attributes['src'],
            cl_and_per=info.css_first('p.product-card__meta').text().strip()
        )
        res.append(item)

    return res


def write_csv(data: list) -> None:
    """ Writing Data to csv file """

    with open('data.csv', 'w', newline='') as csvFile:

        writer = csv.writer(csvFile)
        writer.writerow(['Title', 'Price', 'Currency', 'Img_src', 'Cl and Percent'])

        for d in data:
            writer.writerow([d.title, d.price, d.currency, d.img_src, d.cl_and_per])


def main():
    """ MAIN func"""

    html = get_html(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky')
    data = scrape(html)
    write_csv(data)
    pprint(data)


if __name__ == '__main__':
    main()
