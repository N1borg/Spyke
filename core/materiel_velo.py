import requests
from bs4 import BeautifulSoup
from core.loading_bar import loading_bar

nArticles = -1
nArticlesDone = 0

def get_url():
    return "www.materiel-velo.com"

def get_num_art(html):
    num_articles = html.find('p', attrs={
        'class' : 'u-txt-sm u-txt-dark u-mb-0'
    })

    if num_articles:
        num_articles = int(num_articles.text.strip().split()[0])
        return num_articles
    raise ValueError("Erreur lors de la récupération du nombre d'articles.")

def parse_page(url, output_file, headers, session):
    global nArticles
    global nArticlesDone

    response = session.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if nArticles == -1:
            nArticles = get_num_art(soup)

        articles = soup.find_all('div', attrs={
            'class' : 'c-pdt-mini__body'
        })

        if not articles:
            return 0

        for article in articles:
            model = article.find('a', attrs={
                'class' : 'stretched-link u-l-o /js js-hover-pdt'
            })
            price = article.find('div', attrs={
                'class' : 'u-d-flex u-flex-column'
            })
            if model and price:
                output_file.write(f";{model.text.strip()};{price.text.strip()}\n")
            nArticlesDone += 1
            loading_bar(nArticles, nArticlesDone)
        return 1
    else:
        print("Erreur lors de l'accès au site:", url)
        return 0

def main(page, csv_file, headers):
    url = f"https://{get_url()}"

    with requests.Session() as session:
        with open(csv_file, 'a', encoding='utf-8') as output_file:
            output_file.write("Marque;Modèle;Prix\n")
            i = 1
            while True:
                returned = parse_page(f"{url}{page}&page={str(i)}", output_file, headers, session)
                i += 1
                if returned == 0 or nArticlesDone >= nArticles:
                    break
            print(f"\nNombre de résultats affichés par le site: {nArticles}\nNombre de résultats trouvés: {nArticlesDone}")
