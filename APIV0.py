import requests
import json
import time
import random

def fetch_vinted_items(query="sneakers", pages=1):
    # 1. Configuration de la session
    session = requests.Session()
    
    # Il est CRITIQUE d'avoir un User-Agent réaliste pour ne pas être rejeté immédiatement
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.vinted.fr/"
    }
    session.headers.update(headers)

    try:
        # 2. Étape Initiale : Visiter la page d'accueil pour obtenir les cookies (CSRF, session)
        print("Initialisation de la session (récupération des cookies)...")
        response_home = session.get("https://www.vinted.fr/")
        
        if response_home.status_code != 200:
            print(f"Erreur lors de l'accès à la page d'accueil: {response_home.status_code}")
            return

        # Pause aléatoire pour imiter un humain
        time.sleep(random.uniform(1, 3))

        # 3. Requête vers l'API interne
        api_url = "https://www.vinted.fr/api/v2/catalog/items"
        
        all_items = []
        
        for page in range(1, pages + 1):
            params = {
                "search_text": query,
                "page": page,
                "per_page": 20,  # Nombre d'articles par page
                "order": "newest_first" # Tri par nouveauté
            }
            
            print(f"Scraping page {page} pour '{query}'...")
            response_api = session.get(api_url, params=params)

            # Gestion des erreurs (notamment les blocages 403/429)
            if response_api.status_code == 200:
                data = response_api.json()
                items = data.get("items", [])
                
                for item in items:
                    item_info = {
                        "id": item.get("id"),
                        "titre": item.get("title"),
                        "prix": item.get("total_item_price"),
                        "taille": item.get("size_title"),
                        "marque": item.get("brand_title"),
                        "url": item.get("url")
                    }
                    all_items.append(item_info)
                    print(f"Trouvé: {item_info['titre']} - {item_info['prix']}")
            
            elif response_api.status_code == 403:
                print("ERREUR 403: Accès refusé par Datadome/Cloudflare. Bot détecté.")
                break
            elif response_api.status_code == 429:
                print("ERREUR 429: Trop de requêtes (Rate Limit).")
                break
            else:
                print(f"Erreur inconnue: {response_api.status_code}")
            
            # Pause entre les pages pour réduire le risque de ban
            time.sleep(random.uniform(2, 5))

        return all_items

    except Exception as e:
        print(f"Une erreur est survenue: {e}")

if __name__ == "__main__":
    resultats = fetch_vinted_items(query="jean levi's", pages=1)
    print(f"\nTotal articles récupérés : {len(resultats)}")