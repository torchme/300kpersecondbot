import urllib.request as libreq
from urllib.parse import quote_plus
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json


def xml_to_json(xml_data):
    root = ET.fromstring(xml_data)
    namespaces = {"atom": "http://www.w3.org/2005/Atom"}  # Пространство имён Atom

    articles_list = []
    for entry in root.findall("atom:entry", namespaces):
        article = {
            "id": entry.find("atom:id", namespaces).text,
            "title": entry.find("atom:title", namespaces).text,
            "summary": entry.find("atom:summary", namespaces).text.strip(),
            "published": entry.find("atom:published", namespaces).text,
            "updated": entry.find("atom:updated", namespaces).text,
            "authors": [
                author.find("atom:name", namespaces).text
                for author in entry.findall("atom:author", namespaces)
            ],
        }
        articles_list.append(article)
    return json.dumps(articles_list, indent=4, ensure_ascii=False)


# Параметры запроса
categories = ["cs.LG", "cs.AI"]  # Machine Learning и Artificial Intelligence
keywords = "Recommendation system"
date_start = (datetime.now() - timedelta(days=7)).strftime(
    "%Y%m%d"
)  # Начальная дата (7 дней назад)
date_end = datetime.now().strftime("%Y%m%d")  # Конечная дата (сегодня)
max_results = 10

# Формируем часть запроса с категориями
category_query = "+OR+".join([f"cat:{category}" for category in categories])

# Формируем полный запрос
search_query = f'({category_query})+AND+all:"{keywords}"+AND+submittedDate:[{date_start}+TO+{date_end}]'
encoded_query = quote_plus(search_query, safe=":/+[]")

# Склеиваем базовый URL и закодированный запрос
base_url = "http://export.arxiv.org/api/query?"
full_url = f"{base_url}search_query={encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

# Выполнение запроса
with libreq.urlopen(full_url) as url:
    response = url.read()
    json_output = xml_to_json(response)
    print(json_output)
