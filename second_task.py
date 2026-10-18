import json
import requests

from pymongo import MongoClient
from bs4 import BeautifulSoup


BASE_URL = "http://quotes.toscrape.com"
uri = "mongodb://localhost:27017"

def create_author_item(author) -> dict:
    """
    Збираємо дані по автору за визначеною структурою
    """
    author_dict = {}
    author_dict['fullname'] = author.find('h3', class_='author-title').text
    author_dict['born_date'] = author.find('span', class_='author-born-date').text
    author_dict['born_location'] = author.find('span', class_='author-born-location').text
    author_dict['description'] = author.find('div', class_='author-description').text.strip()

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
    quote_dict['author'] = quote.find('small', class_='author').text.strip()
    quote_dict['quote'] = quote.find('span', class_='text').text.strip()

    return quote_dict


def find_all_authors_in_page(page, authors_fullname) -> list:
    all_authors = []
    authors_fullname = authors_fullname
    for author in page.find_all('small', class_='author'):
        author_fullname = author.text.strip()
        if author_fullname in authors_fullname:
            continue
        authors_fullname.append(author_fullname)
        author_pre_url = author.find_next_sibling('a')['href']
        author_url = f"{BASE_URL}{author_pre_url}"
        author_doc = requests.get(author_url)
        if not author_doc.status_code == 200:
            print('Server not found')
            return all_authors
        author_soup = BeautifulSoup(author_doc.content, 'html.parser')
        author = author_soup.find('div', class_='author-details')
        author_dict = create_author_item(author)
        all_authors.append(author_dict)
    return all_authors, author_fullname


def find_all_quotes_in_page(page) -> list:
    all_quotes = []
    for quote in page.find_all('div', class_='quote'):
        quote_dict = create_quote_item(quote)
        all_quotes.append(quote_dict)
    return all_quotes


def get_request(url):
    html_doc = requests.get(url)
    if not html_doc.status_code == 200:
        return 'Server not found'

    soup = BeautifulSoup(html_doc.content, 'html.parser')
    return soup


def main():

    client = MongoClient(uri)
    db = client.my_database

    quotes_list = []
    authors_list = []
    authors_fullname_list = []
    url = BASE_URL

    while True:
        print(url)

        soup = get_request(url)
        all_quotes = find_all_quotes_in_page(soup)
        all_authors, authors_fullname = find_all_authors_in_page(soup, authors_fullname_list)
        authors_fullname_list.extend(authors_fullname)
        quotes_list.extend(all_quotes)
        authors_list.extend(all_authors)

        try:
            next_page = soup.find('li', class_='next').find('a')['href']
            url = BASE_URL + next_page
        except:
            break

    create_files_json(quotes_list, authors_list)


if __name__ == '__main__':
    main()