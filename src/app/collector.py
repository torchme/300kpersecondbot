import xml.etree.ElementTree as ET

import requests
from loguru import logger
from scholarly import scholarly
from tqdm import tqdm


class Collector:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query?"

    def get_citations(self, author_name):
        search_query = scholarly.search_author(author_name)
        try:
            author = next(search_query)
            author = scholarly.fill(author, sections=["basics", "indices"])
            h_index = author.get("hindex", 0)
            i10_index = author.get("i10index", 0)
            return h_index, i10_index
        except StopIteration:
            logger.warning(f"Author not found: {author_name}")
            return 0, 0
        except Exception as exception:
            logger.error(f"An error occurred: {exception}")
            return 0, 0

    def fetch_arxiv_papers(self, query, max_results=10):
        query = f'search_query=all:"{query}"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
        url = self.base_url + query

        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Ошибка при запросе: {response.status_code}")
            return None

        root = ET.fromstring(response.content)
        papers = []
        for entry in tqdm(root.findall("{http://www.w3.org/2005/Atom}entry")):
            authors = [
                author.find("{http://www.w3.org/2005/Atom}name").text
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
            ]
            paper_info = {
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
                "link": entry.find("{http://www.w3.org/2005/Atom}id").text.strip(),
                "authors": authors,
            }

            h_indices = []
            i10_indices = []

            for author in authors:
                h_index, i10_index = self.get_citations(author)
                h_indices.append(h_index)
                i10_indices.append(i10_index)

            average_h_index = sum(h_indices) / len(h_indices) if h_indices else 0
            average_i10_index = (
                sum(i10_indices) / len(i10_indices) if i10_indices else 0
            )

            paper_info["h_index"] = average_h_index
            paper_info["i10_index"] = average_i10_index

            papers.append(paper_info)

        return papers
