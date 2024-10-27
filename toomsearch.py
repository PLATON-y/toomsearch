#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Recherche Avancée et Détection de Répertoires
Version : 1.2.0
Auteur  : Platon-Y pour pctamalou.fr
Date    : 27 octobre 2024
Mise à jour de la version initiale du 15 août 2017

Description :
Ce script permet d'effectuer des recherches avancées dans des moteurs de recherche en ligne de commande,
en ciblant les répertoires ouverts ou les pages contenant des fichiers, avec une option de gestion de CAPTCHA.
Fonctionnalités principales :
- Recherche de liens "index of" et "parent directory"
- Gestion avancée de l'interface utilisateur en couleur
- Détection automatique et résolution des CAPTCHA via le navigateur
- Sauvegarde et suppression des doublons dans les résultats
- Compatibilité multi-moteur (Google, Bing, DuckDuckGo, etc.)

Usage :
1. Pour une recherche avancée par défaut :
   - Lancer le script et sélectionner l'option de recherche par défaut (mots-clés seulement).
2. Pour une recherche personnalisée :
   - Spécifier un moteur de recherche, des mots-clés, et des types de fichiers spécifiques.
   - L'utilisateur peut choisir de rechercher dans des répertoires "index of" ou "parent directory".

Ce script est conçu pour être utilisé sous Linux, particulièrement sur Kali Linux, et se destine aux professionnels en sécurité.

"""

import requests
from bs4 import BeautifulSoup
import random
import time
import webbrowser
from colorama import init, Fore, Style

# Initialisation de colorama pour la couleur en terminal
init(autoreset=True)

# Rotation de User-Agents pour éviter le blocage
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    # Ajoutez davantage de User-Agents ici
]

# Liste des moteurs de recherche
engines = {
    "google": "https://www.google.com/search?q={}",
    "bing": "https://www.bing.com/search?q={}",
    "duckduckgo": "https://duckduckgo.com/?q={}",
    "qwant": "https://www.qwant.com/?q={}",
    "mojeek": "https://www.mojeek.com/search?q={}",
    "brave": "https://search.brave.com/search?q={}",
    "gigablast": "https://www.gigablast.com/search?q={}",
    "startpage": "https://www.startpage.com/sp/search?q={}",
    "swisscows": "https://swisscows.com/web?query={}",
    "yahoo": "https://search.yahoo.com/search?p={}",
    "ask": "https://www.ask.com/web?q={}",
    "baidu": "https://www.baidu.com/s?wd={}"
}

# Construire l'URL de recherche selon les paramètres
def build_search_url(query, engine, filetype=None, advanced=False):
    file_filter = f" filetype:{filetype}" if filetype else ""
    advanced_filter = " intitle:'index of' OR 'parent directory'" if advanced else ""
    full_query = f"{query}{file_filter} {advanced_filter}"
    return engines[engine].format(full_query)

# Vérifie si une réponse contient un CAPTCHA
def detect_captcha(response_text):
    captcha_keywords = ["captcha", "verify", "not a robot"]
    return any(keyword in response_text.lower() for keyword in captcha_keywords)

# Ouvre le CAPTCHA dans le navigateur pour résolution manuelle
def open_browser_for_captcha(url):
    print(Fore.YELLOW + "CAPTCHA détecté. Ouverture du navigateur pour résolution manuelle...")
    webbrowser.open(url)
    input(Fore.LIGHTGREEN_EX + "Appuyez sur Entrée une fois que vous avez résolu le CAPTCHA dans le navigateur...")

# Récupération des résultats de recherche avec gestion des CAPTCHA
def fetch_search_results(query, engine, filetype=None, advanced=False):
    url = build_search_url(query, engine, filetype, advanced)
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Détecte si un CAPTCHA est présent
        if detect_captcha(response.text):
            open_browser_for_captcha(url)
            response = requests.get(url, headers=headers, timeout=10)  # Relance la requête après résolution
        
        # Analyse du contenu de la réponse
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for item in soup.find_all('h3'):
            link_tag = item.find_parent("a")
            if link_tag and link_tag.get('href'):
                results.append((item.text, link_tag['href']))
        return results
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erreur lors de la connexion à {engine} : {e}")
        return []

# Génération de variantes de requêtes
def generate_query_variations(base_query):
    keywords = ["index.of", "parent directory", "backup", "downloads", "files", "documents"]
    return [f"{base_query} intitle:'{kw}'" for kw in keywords]

# Recherche avec variantes et enregistrement des résultats
def search_with_variations(base_query, engine, filetype=None):
    query_variations = generate_query_variations(base_query)
    all_results = []
    for query in query_variations:
        print(Fore.CYAN + f"\n🔍 Recherche avec la requête : {query}")
        results = fetch_search_results(query, engine, filetype, advanced=True)
        all_results.extend(results)
        time.sleep(1)  # Pause pour éviter le blocage
    if all_results:
        save_results(all_results, "resultats_repertoires.txt")
    else:
        print(Fore.YELLOW + "⚠️ Aucun lien trouvé.")

# Sauvegarde des résultats dans un fichier
def save_results(results, filename):
    unique_results = list(set(results))  # Suppression des doublons
    with open(filename, "w", encoding="utf-8") as file:
        for title, link in unique_results:
            file.write(f"{title}\n{link}\n\n")
    print(Fore.GREEN + f"📁 Résultats sauvegardés dans {filename}")

# Recherche avancée multi-moteur avec support des CAPTCHA
def perform_deep_search(query, engines=None):
    engines = engines or list(engines.keys())
    print(Fore.MAGENTA + "\nLancement de la recherche avancée sur plusieurs moteurs...")
    all_results = []
    for engine in engines:
        print(Fore.BLUE + f"\n🔍 Recherche sur {engine.capitalize()}")
        results = fetch_search_results(query, engine, advanced=True)
        all_results.extend(results)
        time.sleep(1)  # Pause entre chaque moteur
    if all_results:
        save_results(all_results, "resultats_avances.txt")
    else:
        print(Fore.YELLOW + "⚠️ Aucun résultat trouvé.")

# Interaction utilisateur
def user_interaction():
    while True:
        use_default = input(Fore.LIGHTWHITE_EX + "Utiliser la recherche avancée par défaut (mots-clés seulement) ? (oui/non) : ").lower()
        if use_default == "oui":
            query = input("Entrez votre requête de recherche : ")
            perform_deep_search(query)
        else:
            engine = input(Fore.LIGHTWHITE_EX + "Choisissez un moteur de recherche (google, bing, etc.) : ").lower()
            if engine not in engines:
                print(Fore.RED + "⚠️ Moteur de recherche non supporté.")
                continue

            query = input("Entrez votre requête de recherche : ")
            advanced = input("Chercher des répertoires 'index of' et 'parent directory' ? (oui/non) : ").lower() == 'oui'
            filetype = input("Type de fichier (ex : pdf, mp3, txt) : ").lower()

            if advanced:
                search_with_variations(query, engine, filetype)
            else:
                results = fetch_search_results(query, engine, filetype, advanced=False)
                if results:
                    save_results(results, "resultats_simple.txt")
                else:
                    print(Fore.YELLOW + "⚠️ Aucun résultat trouvé.")

        if input("Voulez-vous continuer ? (oui/non) : ").lower() != 'oui':
            break

if __name__ == "__main__":
    user_interaction()
