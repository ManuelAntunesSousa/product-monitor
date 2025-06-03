import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

OUT_OF_STOCK_KEYWORDS = [
    "sold out",
    "out of stock",
    "currently unavailable",
    "notify me when available",
    "esgotado",
    "pre-order stock will be available soon",
]

def generic_checker(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        page_text = soup.text.lower()
        return not any(keyword in page_text for keyword in OUT_OF_STOCK_KEYWORDS)
    except Exception as e:
        print(f"⚠️ Error checking {url}: {e}")
        return False

def check_totalcards():
    url = "https://totalcards.net/collections/pokemon-elite-trainer-boxes/products/pokemon-scarlet-violet-white-flare-elite-trainer-box"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        page_text = soup.text.lower()
        if any(k in page_text for k in ["pre-order", "preorder", "out of stock"]):
            return False
        button = soup.find("button", {"name": "add"})
        return button and "disabled" not in button.attrs
    except Exception as e:
        print(f"⚠️ TotalCards error: {e}")
        return False

def check_gamestop():
    url = "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-white-flare-elite-trainer-box/20021658.html"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        button = soup.find("button", {"data-button": "add-to-cart"})
        return button and "disabled" not in button.attrs
    except Exception as e:
        print(f"⚠️ GameStop error: {e}")
        return False

def check_ventura():
    url = "https://venturacardgames.com/products/pokemon-tcg-scarlet-violet-white-flare-elite-trainer-box-reshiram-edition-english"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        button = soup.find("button", {"name": "add"})
        return button and "disabled" not in button.attrs
    except Exception as e:
        print(f"⚠️ Ventura error: {e}")
        return False

# Grouped product logic
PRODUCTS = {
    "White Flare ETB": [
        {
            "name": "Lotus Valley",
            "url": "https://lotusvalley.pt/produto/white-flare-elite-trainer-box/",
            "check": lambda: generic_checker("https://lotusvalley.pt/produto/white-flare-elite-trainer-box/")
        },
        {
            "name": "Total Cards",
            "url": "https://totalcards.net/collections/pokemon-elite-trainer-boxes/products/pokemon-scarlet-violet-white-flare-elite-trainer-box",
            "check": check_totalcards
        },
        {
            "name": "GameStop",
            "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-white-flare-elite-trainer-box/20021658.html",
            "check": check_gamestop
        },
        {
            "name": "Ventura",
            "url": "https://venturacardgames.com/products/pokemon-tcg-scarlet-violet-white-flare-elite-trainer-box-reshiram-edition-english",
            "check": check_ventura
        },
    ],
    "Black Bolt ETB": [
        {
            "name": "Lotus Valley",
            "url": "https://lotusvalley.pt/produto/black-bolt-elite-trainer-box/",
            "check": lambda: generic_checker("https://lotusvalley.pt/produto/black-bolt-elite-trainer-box/")
        },
        {
            "name": "Press Start",
            "url": "https://www.pressstart.pt/en/pokemon-tcg-scarlet-violet-white-flare/cartas-pokemon-tcg-scarlet-violet-black-bolt-elite-trainer-box.html",
            "check": lambda: generic_checker("https://www.pressstart.pt/en/pokemon-tcg-scarlet-violet-white-flare/cartas-pokemon-tcg-scarlet-violet-black-bolt-elite-trainer-box.html")
        },
        {
            "name": "Total Cards",
            "url": "https://totalcards.net/collections/pokemon-elite-trainer-boxes/products/pokemon-scarlet-violet-black-bolt-elite-trainer-box",
            "check": lambda: generic_checker("https://totalcards.net/collections/pokemon-elite-trainer-boxes/products/pokemon-scarlet-violet-black-bolt-elite-trainer-box")
        },
        {
            "name": "Ventura",
            "url": "https://venturacardgames.com/products/pokemon-tcg-scarlet-violet-black-bolt-elite-trainer-box-zekrom-edition-english-pre-order",
            "check": lambda: generic_checker("https://venturacardgames.com/products/pokemon-tcg-scarlet-violet-black-bolt-elite-trainer-box-zekrom-edition-english-pre-order")
        },
        {
            "name": "Fantasia Cards",
            "url": "https://fantasiacards.de/en/collections/pokemon-box-englisch-fantasiacards/products/pokemon-black-bolt-elite-trainer-box-eng",
            "check": lambda: generic_checker("https://fantasiacards.de/en/collections/pokemon-box-englisch-fantasiacards/products/pokemon-black-bolt-elite-trainer-box-eng")
        }
    ]
}
