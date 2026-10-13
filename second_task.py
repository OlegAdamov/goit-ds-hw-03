from pymongo import MongoClient
import requests
import json

from bs4 import BeautifulSoup

uri = "mongodb://localhost:27017"

client = MongoClient(uri)

db = client.my_database

BASE_URL = "http://quotes.toscrape.com"

def get_urls():
    urls = ["/"]
    html_doc = requests.get(BASE_URL)
    soup = BeautifulSoup(html_doc.text, 'html.parser')