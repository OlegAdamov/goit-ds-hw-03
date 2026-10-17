import json
import requests

from pymongo import MongoClient
from bs4 import BeautifulSoup

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client.my_database

BASE_URL = "http://quotes.toscrape.com"







def authors_item(authors) -> list:
    """
    Збираємо дані по автору за визначеною структурою
    """
    authors_list = []
    for author in authors:
        author_dict = {}
        author_dict['fullname'] = ''
        author_dict['born_date'] = ''
        author_dict['born_location'] = ''
        author_dict['description'] = ''
        author_dict.update(authors_list)


def quotes_item(quotes) -> list:
    """
    Збираємо дані по статті за визначеною структурою
    """
    quotes_list = []
    for quote in quotes:
        quote_dict = {}
        quote_dict['tags'] = ''
        quote_dict['author'] = ''
        quote_dict['quote'] = ''
        quote_dict.update(quotes_list)


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


def main():
    # quotes = soup.find_all('span', class_='text')
    # authors = soup.find_all('small', class_='author')
    # tags = soup.find_all('div', class_='tags')
    ...
