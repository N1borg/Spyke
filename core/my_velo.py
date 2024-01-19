import requests
from bs4 import BeautifulSoup
from core.loading_bar import loading_bar

nArticles = -1
nArticlesDone = 0

def get_url():
    return "my-velo.fr"

def get_num_art(html):
    num_articles = html.find('span', attrs={
        'class' : 'heading-counter'
    })

    if num_articles:
        num_articles = num_articles.text.strip().split()[0]
        num_articles = int(num_articles)
        return num_articles
    else:
        return 0

def parse_page(url, output_file, headers):
    global nArticles
    global nArticlesDone

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('div', attrs={
            'class' : 'pro_second_box'
        })
        if not articles:
            print("Erreur lors de la structuration des articles.")
            exit(1)
        for article in articles:
            model = article.find('a', attrs={
                'class' : 'product-name'
            })
            price = article.find('span', attrs={
                'itemprop' : 'price',
                'class' : 'price product-price'
            })
            if model and price:
                output_file.write(f";{model.text.strip()};{price.text.strip()}\n")
            nArticlesDone += 1
            loading_bar(nArticles, nArticlesDone)
        is_next = soup.find('a', attrs={
                'title' : 'Suivant',
                'rel' : 'next'
            })
        return is_next
    else:
        print("Erreur lors de l'accès au site:", url)
        exit(1)


def parse_pages(url, output_file, headers):
    global nArticles
    global nArticlesDone

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        nArticles = get_num_art(soup)

        output_file.write("Marque;Modèle;Prix\n")

        i = 1
        page = ""
        while True:
            is_next = parse_page(url + page, output_file, headers)
            if not is_next:
                break
            i += 1
            page = "&p=" + str(i)
    else:
        print("Erreur lors de l'accès au site:", url)
        return 0

def main(page, csv_file, headers):
    url = f"https://{get_url()}"

    with open(csv_file, 'a', encoding='utf-8') as output_file:
        parse_pages(url + page, output_file, headers)
        print(f"\nNombre de résultats affichés par le site: {nArticles}\nNombre de résultats trouvés: {nArticlesDone}")
