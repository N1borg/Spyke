import requests
from bs4 import BeautifulSoup
from core.loading_bar import loading_bar

nArticles = 0
nArticlesDone = 0

def get_url():
    return "www.alltricks.fr"

def get_num_art(html):
    num_articles = html.find('div', attrs={
        'class' : 'alltricks-ProductListingHeader__item--left'
    })

    if num_articles:
        num_articles = int(num_articles.text.strip().split()[0])
        return num_articles
    raise ValueError("Erreur lors de la récupération du nombre d'articles.")

def get_pages(url, headers, session):
    global nArticles
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nArticles = get_num_art(soup)

        parent_div = soup.find('div', attrs={
            'id': 'alltricks-Pager',
            'class': 'alltricks-Pager',
            'data-controller': 'pager',
            'data-action': 'pageshow@window->pager#displayLastPageLoadedInBackNavigationContext scroll@window->pager#handleScroll',
            'data-pager-current-page': '1'
        })

        if not parent_div:
            raise ValueError("Erreur lors de la récupération des articles.")

        ajax_urls = [item['data-ajax-url'].strip() for item in parent_div.find_all('div', attrs={
            'class': 'alltricks-Pager__item',
            'data-action': 'click->product-listing#storeLastPageLoaded'
        })]
        return ajax_urls
    else:
        raise ValueError(f"Erreur lors de l'accès au site : {url}")

def parse_page(url, output_file, headers, session):
    global nArticles
    global nArticlesDone

    response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        parent_divs = soup.find_all('div', attrs={
            'class': 'alltricks-Product alltricks-Product--grid',
            'data-childselectorparenttarget': '',
            'data-productread': '',
            'data-controller': 'selectItemDatalayerEvent addToCartDatalayerEvent wishlist'
        })

        if not parent_divs:
            raise ValueError("Erreur lors de la récupération des articles.")

        for parent_div in parent_divs:
            brand_label = parent_div.find('strong', attrs={
                'class': 'alltricks-Product-brandLabel',
                'data-titleproductbrand': ''
            }).text.strip()
            model = parent_div.find('a', attrs={
                'data-testid': 'product-url',
                'class': 'alltricks-Product-description',
                'data-titleproductread': ''
            }).text.strip()
            price = parent_div.find('span', attrs={'class': 'alltricks-Product-price'}).text.strip()
            output_file.write(f"{brand_label};{model};{price}\n")
            nArticlesDone += 1
            loading_bar(nArticles, nArticlesDone)
    else:
        raise ValueError(f"Erreur lors de la structuration des données : {url}")

def main(page, csv_file, headers):
    url = f"https://{get_url()}"
    with requests.Session() as session:
        try:
            ajax_urls = get_pages(url + page, headers, session)

            if ajax_urls is not None:
                with open(csv_file, 'a', encoding='utf-8') as output_file:
                    output_file.write("Marque;Modèle;Prix\n")
                    for ajax_url in ajax_urls:
                        print(url + ajax_url)
                        parse_page(url + ajax_url, output_file, headers, session)
                print(f"\nNombre de résultats affichés par le site: {nArticles}\nNombre de résultats trouvés: {nArticlesDone}")
            else:
                print("Pas de page trouvée!")
                exit(1)
        except ValueError as e:
            print(f"Erreur : {str(e)}")
