# Spyke

**Ceux qui savent, savent**

## Description

Spyke est un script Python conçu pour extraire des données de divers sites web cyclistes. Il prend actuellement en charge Alltricks, Culture vélo, materiel-velo.com et My Velo.

## Installation

### Prérequis
- [Python 3](https://www.python.org/downloads/)
- [pip (installateur de packages Python)](https://pip.pypa.io/en/stable/installation/)

### Étapes d'installation (Windows)

1. Clonez le dépôt Spyke sur votre machine locale:

   ```cmd
   git clone https://github.com/N1borg/Spyke.git
2. Accédez au répertoire Spyke:

    ```cmd
    cd spyke
3. Exécutez le script d'installation:

    ```cmd
    install.bat
Ce script s'assurera que les packages Python requis seront installés.

## Utilisation

Après l'installation, vous pouvez exécuter le script Spyke en utilisant le script de lancement fourni.

    C:\Users\%USERNAME%\Documents\spyke\launching.bat

Le script vous demandera d'entrer l'URL de la page que vous souhaitez extraire. Il suffit de faire la recherche sur le site avec les filtres souhaités et de copier l'URL de la page directement dans le programme.

Suivez les invites pour sélectionner le dossier de sortie CSV, fournir un préfixe de fichier CSV et confirmer l'exécution.
Le script tentera ensuite d'extraire des données de l'URL fournie, et le fichier CSV résultant sera enregistré dans le dossier spécifié.

## État sites Web pris en charge

- [x] www.alltricks.fr
- [ ] www.culturevelo.com
- [x] www.materiel-velo.com
- [x] my-velo.fr

## Signalement de Bugs

Si vous rencontrez des bugs, des erreurs, ou si vous avez des préoccupations, veuillez les signaler en ouvrant un ticket sur le tracker d'issues. Vos retours sont précieux pour améliorer la qualité du script.

## Clause de non-responsabilité

Ce script est fourni tel quel, et les mainteneurs ne sont pas responsables de tout mauvais usage ou extraction non autorisée de sites web. Utilisez-le de manière responsable et en conformité avec les conditions d'utilisation des sites que vous extrayez.

Happy scraping!
