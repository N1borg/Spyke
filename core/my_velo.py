import requests
from bs4 import BeautifulSoup

n_products_site = n_products = 0

def get_url():
    return "my-velo.fr"

def get_first_page(url, output_file, headers):
    global n_products_site
    global n_products
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        no_result = soup.find('p', class_="alert alert-warning")
        if no_result:
            print("Erreur: réponse du site:" + no_result.text)
            exit(0)
        parent_div = soup.find('h1', class_='page-heading product-listing')
        if parent_div:
            n_products_site = int(parent_div.text.split('"')[2].split()[0])
            if n_products_site < 1:
                exit(1)
        try:
            parent_div = soup.find('ul', attrs={'id': 'product_list', 'class': 'product_list grid row', 'data-classnames': 'col-lg-4 col-md-4 col-sm-4 col-xs-4 col-xxs-4', 'data-view-mobile': ' grid ', 'data-view': ' grid '})
            if parent_div:
                products = parent_div.find_all('li')
                if products:
                    output_file.write("Marque;Modèle;Prix\n")
                    for product in products:
                        product_info = product.find('div', class_='pro_second_box')
                        if product_info:
                            product_name = product_info.find('h5', attrs={'itemprop', 'name', 'class', 's_title_block nohidden'}).text
                            product_price = product_info.find('div', attrs={'class', 'price_container', 'itemprop', 'offers', 'itemtype', 'https://schema.org/Offer'}).text
                            n_products += 1
                            output_file.write(f"{product_name};{product_price}\n")
        except Exception as e:
            print(f"Erreur lors de la structuration des données: {e}")
        parent_div = soup.find('ul', class_='pagination')
        if parent_div:
            number_of_pages = parent_div.find_all('li')[-2].find('a').text
            number_of_pages = int(number_of_pages)
            return number_of_pages
        else:
            return 1
    else:
        print("Erreur lors de l'accès au site:", url)

def parse_page(url, output_file, headers):
    global n_products
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            parent_div = soup.find('ul', attrs={'id': 'product_list', 'class': 'product_list grid row', 'data-classnames': 'col-lg-4 col-md-4 col-sm-4 col-xs-4 col-xxs-4', 'data-view-mobile': ' grid ', 'data-view': ' grid '})
            if parent_div:
                products = parent_div.find_all('li')
                if products:
                    for product in products:
                        product_info = product.find('div', class_='pro_second_box')
                        if product_info:
                            product_name = product_info.find('h5', attrs={'itemprop', 'name', 'class', 's_title_block nohidden'}).text
                            product_price = product_info.find('div', attrs={'class', 'price_container', 'itemprop', 'offers', 'itemtype', 'https://schema.org/Offer'}).text
                            n_products += 1
                            output_file.write(f"{product_name};{product_price}\n")
        except Exception as e:
            print(f"Erreur lors de la structuration des données: {e}")
    else:
        print("Erreur lors de l'accès au site:", url)

def main(qarticle, csv_file, headers):
    website = f"https://{get_url()}/fr/module/ambjolisearch"
    page = "/jolisearch?search_query="
    parameters = "&orderby=position&orderway=desc&search_query=" + qarticle + "&id_Ambjolisearch=0&n=120"
    url = website + page + qarticle + parameters

    with open(csv_file, 'a', encoding='utf-8') as output_file:
        n_pages = get_first_page(url, output_file, headers)
        print(f"Structuration de {n_pages} page(s) ({n_products_site} produits trouvés d'après le site)")
        if n_pages > 1:
            for page in range(2, n_pages):
                page_url = f"{url}&p={page}"
                print(f"Parsing {page}/{n_pages}...")
                parse_page(page_url, output_file, headers)
    print(f"Nombre de résultats affichés par le site: {n_products_site}\nNombre de résultats trouvés: {n_products}")
