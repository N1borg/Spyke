import os
from re import match
from datetime import datetime
from urllib.parse import urlparse
import core.alltricks as alt
import core.culturevelo as cuv
import core.materiel_velo as mav
import core.my_velo as myv

DEFAULT_FOLDER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_folder.txt")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}
WEBSITES = [alt, cuv, mav, myv]

def is_url(url):
    url_pattern = r"^http(s)?://[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$"

    domain = urlparse(url).netloc
    compatible_website_found = any(domain == website.get_url() for website in WEBSITES)

    if not match(url_pattern, url) or not compatible_website_found:
        print("Mauvais format d'URL ou domaine incompatible!")
        if not compatible_website_found:
            print(f"Le script est compatible avec ces sites:")
            display_websites(WEBSITES)
        return False
    return True

def verify_folder_path():
    try:
        with open(DEFAULT_FOLDER_FILE, 'r') as file:
            folder_path = file.read().strip()
            if folder_path and os.path.exists(folder_path) and os.path.isdir(folder_path):
                use_remembered = input(f"Réutiliser le dossier par défaut '{folder_path}'? (oui/non): ").lower()
                if use_remembered in {'oui', 'o', ''}:
                    return folder_path
    except FileNotFoundError:
        pass

    while True:
        folder_path = input("Chemin d'enregistrement du CSV: ")
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            remember = input("Enregistrer ce chemin comme chemin par défaut? (oui/non): ").lower()
            if remember in {'oui', 'o', ''}:
                with open(DEFAULT_FOLDER_FILE, 'w') as file:
                    file.write(folder_path)
                    print("Chemin enregistré.")
            return folder_path
        else:
            print("Entrez un chemin de dossier valide.")

def display_websites(websites):
    for website in websites:
        print(website.get_url())

def run_url(url, csv_file):
    parsed_url = urlparse(url)
    page = parsed_url.path + ('?' + parsed_url.query if parsed_url.query else '')
    domain = urlparse(url).netloc

    for website in WEBSITES:
        if domain in website.get_url():
            website.main(page, csv_file, HEADERS)
            return
    print(f"Pas de domaine correspondant à {url}\nLe script est compatible avec ces sites:")
    display_websites(WEBSITES)

def main():
    csv_path_file = ""

    # Website URL to parse
    url = input("Entrez l'URL de la page de cette forme 'https://site.tld/page': ")
    while not is_url(url):
        url = input("Entrez l'URL de la page de cette forme 'https://site.tld/page': ")

    # Path to CSV file
    while not csv_path_file:
        csv_path_file = verify_folder_path()
    if not csv_path_file.endswith(('/', '\\')):
        csv_path_file += '/'

    # CSV file prefix
    prefix = input("Préfixe du fichier CSV: ")
    csv_filename = f"export-{prefix}{'-' if prefix else ''}{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.csv"
    csv_file = os.path.join(csv_path_file, csv_filename)
    print(csv_file)

    # Confirmation and parsing
    user_agree = input("Continuer? (oui/non) ").lower()
    if user_agree in {'oui', 'o', ''}:
        run_url(url, csv_file)
        print("Terminé.")
    else:
        print("Abandonné.")
        exit(0)

if __name__ == '__main__':
    main()
