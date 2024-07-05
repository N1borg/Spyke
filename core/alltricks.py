import requests
import re
from bs4 import BeautifulSoup
from core.loading_bar import loading_bar

nArticles = 0
nArticlesDone = 0


def get_url():
    return "www.alltricks.fr"


def get_num_art(page):
    url = f"https://{get_url()}{page}{'&' if '?' in page else '?'}frz-smartcache-fragment=true&frz-timeout=5000&frz-smartcache-v=2"
    response = requests.get(url)
    print(f"URL: {url}")

    if response.status_code == 200:
        pattern = r'<span>(\d+) articles</span>'
        match = re.search(pattern, response.text)

        if match:
            num_articles = int(match.group(1))
            print(f"Articles: {num_articles}")
            return num_articles

    raise ValueError("Can't get number of articles.")


def parse_pages(url, page, csv_file, headers):
    global nArticlesDone

    with open(csv_file, 'a', encoding='utf-8') as output_file:
        output_file.write("Marque;Modèle;Prix\n")
        with requests.Session() as session:
            i = 1
            while True:
                response = session.get(f"{url}/ajax/pagination{page}?Page={i}", headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('div', attrs={
                    'class': 'alltricks-Product'
                })

                if response.status_code != 200 or not articles:
                    if i == 1:
                        raise ValueError("No articles found.")
                    break

                for article in articles:
                    brand = article.find('strong', attrs={
                        'class': 'alltricks-Product-brandLabel'
                    }).text.strip()
                    model = article.find('a', attrs={
                        'class': 'alltricks-Product-description'
                    }).text.strip()
                    price = article.find('span', attrs={
                        'class': 'alltricks-Product-price'
                    }).text.strip()

                    nArticlesDone += 1
                    output_file.write(f"{brand};{model};{price}\n")
                    loading_bar(nArticles, nArticlesDone)

                i += 1


def main(page, csv_file, headers):
    global nArticles

    url = f"https://{get_url()}"
    try:
        try:
            nArticles = get_num_art(page)
        except ValueError as e:
            print(f"Erreur : {str(e)}")

        parse_pages(url, page, csv_file, headers)
        print(f"\n\nNombre de résultats affichés par le site: {nArticles}\nNombre de résultats trouvés: {nArticlesDone}")
    except ValueError as e:
        print(f"Erreur : {str(e)}")
