import requests
from bs4 import BeautifulSoup
import json

url = "https://www.modcs.org/?page_id=521"  # URL a ser verificada
invalid_urls = (
    []
)  # Lista para armazenar as URLs com status code diferente de 200

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    tbody = soup.find("table").find(
        "tbody"
    )  # Encontra o elemento tbody dentro da tabela
    for link in tbody.find_all(
        "a"
    ):  # Procura por todos os elementos <a> dentro do tbody
        href = link.get("href")
        if href is not None and "http" in href:
            # Verifica o status code da URL
            link_response = requests.get(href)
            if link_response.status_code != 200:
                invalid_urls.append(href)

# Adiciona as URLs inválidas em um arquivo JSON
with open("invalid_urls.json", "w", encoding="utf-8") as f:
    json.dump(invalid_urls, f, ensure_ascii=False, indent=4)

print(f"{len(invalid_urls)} URLs com status code diferente de 200 encontradas")
