import requests
from bs4 import BeautifulSoup

n_products_site = n_products = 0

def get_url():
    return "www.culturevelo.com"

def get_num_articles(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        number_articles = soup.find('div', class_='count')
        if number_articles:
            return int(number_articles.text)
        else:
            return 0
    elif response.status_code == 302:
        print("Site: Pas de produit trouvé!")
        exit(0)
    else:
        print("Erreur lors de l'accès au site:", url)
        exit(0)

def parse_article(parent_div, output_file, n_products_site):
    global n_products
    articles = parent_div.find_all('a')
    if articles:
        for article in articles:
            article_label = article.find('h3')
            if article_label:
                n_products += 1
                print(f"Parsing {n_products}/{n_products_site}...")
                article_model = article.find('h4').find(string=True, recursive=False) if article.find('h4') else None
                article_price = article.find('div', class_='dalle-prix')
                if article_model and article_price:
                    print(f"{article_label.text};{article_model};{article_price.text}")
                    output_file.write(f"{article_label.text};{article_model};{article_price.text}\n")

def main(qarticle, csv_file, headers):
    page = f"https://{get_url()}/shop/Produits/ListeFF"
    product_per_page = 1
    parameters = f"?productsPerPage={product_per_page}&query="
    url = page + parameters + qarticle
    n_products_site = get_num_articles(url, headers)
    if not n_products_site > 0:
        print("Pas de produit trouvé!")
        exit(0)
    parameters = f"?productsPerPage={n_products_site}&query="
    url = page + parameters + qarticle
    print(f"{n_products_site} produits trouvé(s)!")
    print("...")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        parent_div = soup.find('div', attrs={'class': 'velos', 'id': 'LISTE'})
    else:
        print("Erreur lors de l'accès au site:", url)
    if not parent_div:
        print("Erreur lors de la structuration des données!")
        exit(0)
    with open(csv_file, 'a', encoding='utf-8') as output_file:
        output_file.write("Marque;Modèle;Prix\n")
        parse_article(parent_div, output_file, n_products_site)        
    print(f"Nombre de résultats affichés par le site: {n_products_site}\nNombre de résultats trouvés: {n_products}")
