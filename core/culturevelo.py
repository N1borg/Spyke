import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.loading_bar import loading_bar

n_products = 0

def get_url():
    return "www.culturevelo.com"

def get_nproducts(url, headers):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['productsPerPage'] = ["1"]
    new_url = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))

    response = requests.get(new_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text.strip(), 'html.parser')
        number_articles = soup.find('div', class_='count')
        if number_articles:
            return int(number_articles.text)
        else:
            return 0
    elif response.status_code == 302:
        print("Site: Pas de produit trouvé!")
        exit(0)
    else:
        print("Erreur lors de l'accès au site:", new_url)
        exit(0)

def parse_article(parent_div, output_file, n_products_site):
    global n_products
    articles = parent_div.find_all('a')
    if articles:
        for article in articles:
            article_label = article.find('h3')
            article_model = article.find('h4')
            article_price = article.find('div', class_='dalle-prix')
            if article_label and article_model and article_price:
                n_products += 1
                loading_bar(n_products_site, n_products)
                output_file.write(f"{article_label.text.strip()};{article_model.text.strip()};{article_price.text.strip()}\n")
            else:
                print("Erreur lors de récupération des informations du produit.")
                return 0
        return 1
    else:
        print("Erreur lors de la structuration des produits.")
        return 0

def main(page, csv_file, headers):
    url = f"https://{get_url()}" + page
    n_products_site = get_nproducts(url, headers)

    if n_products_site <= 0:
        print("Aucun produit trouvé.")
        exit(1)

    print(f"{n_products_site} produits trouvé(s)!")

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['productsPerPage'] = [str(n_products_site)]
    new_url = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
    returned = i = 1
    while returned == 1:
        print("URL:", new_url + "&page=" + str(i))
        response = requests.get(new_url + "&page=" + str(i), headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            parent_div = soup.find('div', attrs={
                'id': 'LISTE',
                'class': 'velos'
            })
        else:
            print("Erreur lors de l'accès au site:", new_url)
        if not parent_div:
            print("Erreur lors de la structuration des données!")
            exit(0)
        with open(csv_file, 'a', encoding='utf-8') as output_file:
            output_file.write("Marque;Modèle;Prix\n")
            returned = parse_article(parent_div, output_file, n_products_site) 
        i += 1
    print(f"\nNombre de résultats affichés par le site: {n_products_site}\nNombre de résultats trouvés: {n_products}")
