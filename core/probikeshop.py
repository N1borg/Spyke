import requests
from bs4 import BeautifulSoup
from core.loading_bar import loading_bar

nArticles = 0
nArticlesDone = 0


def get_url():
    return "www.probikeshop.fr"


def get_num_art(page):
    url = f"https://{get_url()}{page}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text.strip(), 'html.parser')
        number_articles = soup.find('p', attrs={
            'class': 'product-count__text'
        })

        try:
            if number_articles:
                return int(number_articles.text.split()[0])
            else:
                print("Site: Pas de produit trouvé!")
        except ValueError:
            raise ValueError("Can't get number of articles.")
    elif response.status_code == 302:
        print("Site: Pas de produit trouvé!")
        exit(0)
    else:
        print("Erreur lors de l'accès au site:", url)
        exit(0)


def parse_pages(url, page, csv_file, headers):
    global nArticlesDone

    with open(csv_file, 'a', encoding='utf-8') as output_file:
        output_file.write("Marque;Modèle;Prix\n")
        with requests.Session() as session:
            i = 1
            while True:
                response = session.get(f"{url}{page}{'&' if '?' in page else '?'}page={i}", headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('div', attrs={
                    'class': 'card-wrapper'
                })

                if response.status_code != 200 or not articles:
                    break

                for article in articles:
                    brand = ""
                    # brand = article.find('strong', attrs={
                    #     'class': 'alltricks-Product-brandLabel'
                    # }).text.strip()
                    model = article.find('h2', attrs={
                        'class': 'card__heading'
                    }).text.strip()
                    price = article.find('span', attrs={
                        'class': 'price-item'
                    }).text.strip()

                    nArticlesDone += 1
                    output_file.write(f"{brand};{model};{price}\n")
                    loading_bar(nArticles, nArticlesDone)

                i += 1
        if nArticlesDone == 0:
            raise ValueError("No articles found.")


def main(page, csv_file, headers):
    global nArticles

    url = f"https://{get_url()}"
    try:
        nArticles = get_num_art(page)
        print(f"Articles: {nArticles}")
    except ValueError as e:
        print(f"Erreur : {str(e)}")

    try:
        parse_pages(url, page, csv_file, headers)
        print(f"\n\nNombre de résultats affichés par le site: {nArticles}\nNombre de résultats trouvés: {nArticlesDone}")
    except ValueError as e:
        print(f"Erreur : {str(e)}")
