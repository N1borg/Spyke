import requests, json

def get_url():
    return "www.materiel-velo.com"

def main(qarticle, csv_file, headers):
    url = 'https://l2ulfyy23k-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.51.1)%3B%20JS%20Helper%20(3.11.3)&x-algolia-api-key=0b68ab6666e5c93b9141d82c377dd4b0&x-algolia-application-id=L2ULFYY23K'

    data = {
        "requests": [
            {
                "indexName": "mv_product_fr_1",
                "params": f"clickAnalytics=true&facetFilters=price.pr%3E0%2Cactive%3Atrue&facets=%5B%22category_default.name%22%2C%22manufacturer.name%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=96&maxValuesPerFacet=200&page=0&query={qarticle}&tagFilters="
            },
            {
                "indexName": "mv_product_fr_1_query_suggestions",
                "params": f"clickAnalytics=true&facetFilters=&facets=%5B%22category_default.name%22%2C%22manufacturer.name%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=200&page=0&query={qarticle}&tagFilters="
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result_json = json.loads(response.text)
        with open('result.json', 'w', encoding='utf-8') as output_file:
            output_file.write(response.text)
        nb_hits = result_json['results'][0]['nbHits']
        nb_pages = result_json['results'][0]['nbPages']
        print(f"Number of hits: {nb_hits}")
        with open(csv_file, 'a', encoding='utf-8') as output_file:
            n_product = 0
            output_file.write("Marque;Modèle;Prix\n")
            for i in range(nb_pages):
                print(f"Structuration de la page: {i + 1}...")
                data['requests'][0]['params'] = data['requests'][0]['params'].replace('page=0', f'page={i}')
                data['requests'][1]['params'] = data['requests'][1]['params'].replace('page=0', f'page={i}')
                response_updated = requests.post(url, json=data, headers=headers)
                if response_updated.status_code == 200:
                    response_json = json.loads(response_updated.text)

                    for hit in response_json['results'][0]['hits']:
                        n_product += 1
                        brand = hit['manufacturer']['name']
                        model = hit['name']
                        price = hit['price']['fpr']
                        output_file.write(f"{n_product} - {brand};{model};{price}\n")
                else:
                    print(f"Erreur: {response_updated.status_code}\n{response_updated.text}")
                    break
    else:
        print(f"Erreur: {response.status_code}\n{response.text}")
