import requests
from bs4 import BeautifulSoup

def get_url():
    return "www.alltricks.fr"

def get_pages(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        parent_div = soup.find('div', attrs={
            'id': 'alltricks-Pager',
            'class': 'alltricks-Pager',
            'data-controller': 'pager',
            'data-action': 'pageshow@window->pager#displayLastPageLoadedInBackNavigationContext scroll@window->pager#handleScroll',
            'data-pager-current-page': '1'
        })

        ajax_urls = [item['data-ajax-url'].strip() for item in parent_div.find_all('div', attrs={
            'class': 'alltricks-Pager__item',
            'data-action': 'click->product-listing#storeLastPageLoaded'
        })]
        return ajax_urls
    else:
        print("Erreur lors de l'accès au site:", url)
        return None

def parse_page(url, output_file, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        parent_divs = soup.find_all('div', attrs={
            'class': 'alltricks-Product alltricks-Product--grid',
            'data-childselectorparenttarget': '',
            'data-productread': '',
            'data-controller': 'selectItemDatalayerEvent addToCartDatalayerEvent wishlist'
        })

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
    else:
        print("Erreur lors de la structuration des données:", url)
        return None

def main(page, csv_file, headers):
    url = f"https://{get_url()}"
    ajax_urls = get_pages(url + page, headers)

    if ajax_urls is not None:
        with open(csv_file, 'a', encoding='utf-8') as output_file:
            output_file.write("Marque;Modèle;Prix\n")
            for ajax_url in ajax_urls:
                parse_page(url + ajax_url, output_file, headers)
    else:
        print("Pas de page trouvée!")
        exit(1)
