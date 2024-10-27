
# toomsearch

Script de Recherche Avancée et Détection de Répertoires

## Description
**toomsearch** est un script Python avancé destiné aux professionnels de la sécurité pour effectuer des recherches en ligne de commande dans divers moteurs de recherche. Il cible spécifiquement les répertoires ouverts et les pages contenant des fichiers téléchargeables en automatisant la recherche de liens "index of" et "parent directory". Le script inclut également une gestion de CAPTCHA et une rotation de proxies pour éviter les blocages.

### Fonctionnalités Principales
- **Recherche avancée** de liens "index of" et "parent directory" sur plusieurs moteurs de recherche.
- **Rotation de proxies publics** et de **User-Agents** pour éviter le blocage.
- **Détection automatique et gestion des CAPTCHA** avec résolution manuelle.
- **Compatibilité multi-moteur** : Google, Bing, DuckDuckGo, Qwant, Brave, et d’autres.
- **Sauvegarde des résultats** en texte et JSON, avec suppression automatique des doublons.
- **Interface utilisateur colorée** pour une meilleure lisibilité en ligne de commande.

## Prérequis

- **Python 3.x**
- **Bibliothèques Python** :
  - `requests` pour les requêtes HTTP
  - `beautifulsoup4` pour le parsing HTML
  - `colorama` pour les couleurs en terminal
  - `tqdm` pour les barres de progression
  
Vous pouvez installer les dépendances nécessaires avec :

```
pip install requests beautifulsoup4 colorama tqdm
```

## Installation

1. Clonez le dépôt sur votre machine locale :
    ```
    git clone https://github.com/PLATON-y/toomsearch.git
    cd toomsearch
    ```

2. Assurez-vous que toutes les dépendances sont installées en suivant la section [Prérequis](#prérequis).

## Utilisation

### Lancer une Recherche Avancée
Pour lancer une recherche avancée par défaut :
```
python toomsearch.py
```

### Options Disponibles

1. **Recherche avancée par défaut** : Lancer simplement le script pour une recherche basique avec des mots-clés uniquement.
2. **Recherche personnalisée** : Choisissez le moteur de recherche, les mots-clés et le type de fichier. Vous pouvez également opter pour une recherche de répertoires ouverts ("index of" ou "parent directory").

### Exemple d'Utilisation
1. **Recherche avancée par défaut :**
    - Lancer le script
    - Saisir les mots-clés pour la recherche
    - Les résultats seront sauvegardés dans `resultats_avances.txt` et `resultats_avances.json`

2. **Recherche personnalisée :**
    - Choisissez un moteur de recherche
    - Entrez les mots-clés et spécifiez le type de fichier
    - Choisissez si vous souhaitez rechercher dans des répertoires ouverts

### Résolution de CAPTCHA
En cas de détection d’un CAPTCHA, le script ouvre le navigateur par défaut et vous invite à résoudre manuellement le CAPTCHA avant de continuer la recherche.

## Structure du Projet

- **toomsearch.py** : Script principal pour la recherche et la détection de répertoires.
- **requirements.txt** : Liste des dépendances du projet.
- **resultats_repertoires.txt** : Fichier texte où les résultats des recherches sont sauvegardés.
- **resultats_repertoires.json** : Fichier JSON pour sauvegarder les résultats au format JSON.
- **search_errors.log** : Fichier de logs pour enregistrer les erreurs rencontrées lors de l’exécution.


## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez ajouter des fonctionnalités ou corriger des bugs, veuillez créer une branche ou soumettre une pull request. Assurez-vous de documenter toute modification dans le code et dans ce fichier README.

## Licence

Ce projet est sous licence EOS. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---
