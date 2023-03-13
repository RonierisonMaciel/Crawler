import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# URL da página inicial
url = "https://www.tacaratu.pe.gov.br/"

# lista para armazenar URLs válidos
valid_urls = set()

# lista para armazenar URLs já visitados
visited_urls = set()


# função para verificar se uma URL é válida
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# função para obter todas as URLs de uma página
def get_urls(url):
    urls = set()
    try:
        response = requests.get(url)
    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.ConnectionError,
    ):
        return urls
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None:
            href = urljoin(url, href)
            if is_valid(href):
                urls.add(href)
    return urls


# função para rastrear URLs válidos
def crawl(url):
    visited_urls.add(url)
    for link in get_urls(url):
        if link not in visited_urls:
            if is_valid(link):
                print(f"Valid URL: {link}")
                valid_urls.add(link)
                crawl(link)


# iniciar o rastreamento
crawl(url)
