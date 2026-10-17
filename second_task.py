import json
from pprint import pprint

import requests

from pymongo import MongoClient
from bs4 import BeautifulSoup





def create_author_item(authors) -> dict:
    """
    Збираємо дані по автору за визначеною структурою
    """
    author_dict = {}
    author_dict['fullname'] = ''
    author_dict['born_date'] = ''
    author_dict['born_location'] = ''
    author_dict['description'] = ''

    return author_dict


def create_files_json(quotes_list:list, authors_list:list) -> None:
    """
    Create and write the json files
    :param quotes: list of quotes
    :param authors: list of authors :
    :return: None
    """
    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(quotes_list, fd, ensure_ascii=False, indent=4)
    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(authors_list, fd, ensure_ascii=False, indent=4)


def create_quote_item(quote) -> dict:
    """
    Збираємо дані по статті за визначеною структурою
    """
    quote_dict = {}
    quote_dict['tags'] = quote.find('div', class_='tags').find('meta', content=True)['content'].split(',') # ['', '', '']
    quote_dict['author'] = quote.find('small', class_='author').text
    quote_dict['quote'] = quote.find('span', class_='text').text

    return quote_dict


def find_all_authors_in_page(page) -> list:
    all_authors = []
    for author in page.find_all('div', class_='author'):
        author_dict = create_author_item(author)
        all_authors.append(author_dict)
    return all_authors


def find_all_quotes_in_page(page) -> list:
    all_quotes = []
    for quote in page.find_all('div', class_='quote'):
        quote_dict = create_quote_item(quote)
        all_quotes.append(quote_dict)
    return all_quotes



def main():
    # uri = "mongodb://localhost:27017"
    # client = MongoClient(uri)
    # db = client.my_database

    BASE_URL = "http://quotes.toscrape.com"
    html_doc = requests.get(BASE_URL)
    # If the result is unsuccessful and the response code is not 200, we return an indication that the site is absent.
    if not html_doc.status_code == 200:
        return 'Server Error'

    # We perform data parsing from HTML code.
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    # find_quotes = soup.find_all('div', class_='quote')
    pprint(find_all_quotes_in_page(soup))
    pprint(find_all_authors_in_page(soup))
    # quotes = []
    # authors = []
    # for i in range(1, 11):
    #         continue
    ...


if __name__ == '__main__':
    main()