# Downloads pokemon card images images from https://pocket.limitlesstcg.com/
# All rights goes to https://pocket.limitlesstcg.com/

# Use venv to install virtual environment, then 
# python -m venv venv && source venv/Scripts/activate
# pip install requests beautifulsoup4
# to deactivate: deactivate

# To run script
# python3 download.py

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pprint
import re

def snake_case(name):
    """Convert set name to snake_case."""
    name = re.sub(r'[^a-zA-Z0-9\s]', '', name)  # Remove special characters
    return '_'.join(name.lower().split())

def download_image(img_url, folder):
    """Download an image from the given URL to the specified folder."""
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(img_url, headers=headers, stream=True)
    if response.status_code == 200:
        filename = os.path.join(folder, os.path.basename(img_url))
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f'Downloaded: {filename}')
    else:
        print(f'Failed to download: {img_url}')

def fetch_card_data(soup: BeautifulSoup, set_identifier: str):
    """Fetches card data from soup html and adds it into the specified folder"""
    
    card_data = {}

    # Card details (id, rarity, pack)
    card_details = soup.find("div", class_="prints-current-details").find_all("span")[1].text
    card_data["id"] = card_details.split("·")[0].strip()[1:] # take out the #
    card_data["rarity"] = map_rarity(card_details.split("·")[1].strip())

    # Card set data
    card_set = {}
    card_set["id"] = set_identifier
    card_set["name"] = soup.find("div", class_="prints-current-details").find("span", class_="text-lg").text.strip()
    card_data["set"] = card_set

    # Has the card pack exist
    if len(card_details.split("·")) >= 3:
        card_pack = card_details.split("·")[2].strip()
        card_data["pack"] = map_card_pack(card_pack)
    else:
        card_data["pack"] = map_card_pack("")

    # Card text type
    card_type = soup.find("p", class_="card-text-type").text.split("-")[0].strip()
    card_data['name'] = soup.find("p", class_="card-text-title").text.split("-")[0].strip()

    if (card_type == "Trainer"):
        card_data['card_type'] = soup.find("p", class_="card-text-type").text.split("-")[0].strip()
        card_data["type"] = soup.find("p", class_="card-text-type").text.split("-")[1].strip()
        card_data["effect"] = soup.findAll("div", class_="card-text-section")[1].text.strip()
        card_data["text"] = map_trainer_text(card_data["type"])

    else:
        card_data["card_type"] = "Pokemon"
        card_data["stage"] = soup.find("p", class_="card-text-type").text.split("-")[1].strip()
        if (card_data["stage"] != "Basic"):
            card_data["evolutionFrom"] = soup.find("p", class_="card-text-type").find("a").text.strip()

        card_data['type'] = soup.find("p", class_="card-text-title").text.split("-")[1].strip()
        card_data['hp'] = soup.find("p", class_="card-text-title").text.split("-")[2].strip()
        
        card_data_text = soup.find("div", class_="card-text-section card-text-flavor")
        if card_data_text != None:
            card_data["text"] = card_data_text.text.strip()

    
    
    # Artist
    card_data["artist"] = soup.find("div", class_="card-text-section card-text-artist").find("a").text.strip()
    
    pprint.pp(card_data)

def map_rarity(rarity: str):
    """Maps rarity symbol to string"""

    rarityMap = {
        "◊": "Common",
        "◊◊": "Uncommon",
        "◊◊◊": "Rare",
        "◊◊◊◊": "Double Rare",
        "☆": "Illustration Rare",
        "☆☆": "Special Art Rare",
        "☆☆☆": "Immersive Rare",
        "Crown Rare": "Crown Rare"
    }

    return rarityMap[rarity]

def map_card_pack(pack: str):
    """Maps card pack to string"""

    cardPackMap = {
        "Charizard  pack": ["Charizard"],
        "Mewtwo  pack": ["Mewtwo"],
        "Pikachu  pack": ["Pikachu"],
        "": ["Charizard", "Mewtwo", "Pikachu"]
    }

    return cardPackMap[pack]

def map_trainer_text(trainer_type: str):
    """Maps trainer type to a text string"""

    cardTypeMap = {
        "Supporter": "You may play only 1 Supporter card during your turn.",
        "Item": "You may play any number of Item cards during your turn.",
    }

    return cardTypeMap[trainer_type]


def main(set_identifier):
    base_url = f'https://pocket.limitlesstcg.com/cards/{set_identifier}'
    
    # Fetch the set page to get the set name
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; YourBot/1.0; +http://yourdomain.com/bot)'
    }
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve the set page: {base_url}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    set_name_tag = soup.find('div', class_="infobox-heading")
    if set_name_tag:
        set_name = set_name_tag.text.strip()
        set_folder_name = snake_case(set_name)
    else:
        print(f'Failed to determine set name from: {base_url}')
        return

    # Directory to save images
    output_dir = os.path.join('..', 'images', 'sets', set_folder_name)
    os.makedirs(output_dir, exist_ok=True)

    # Find all card links on the set page
    card_links = soup.select(f'a[href^="/cards/{set_identifier}/"]')

    # Iterate through each card link to find and download images
    for link in card_links:

        # TMP to get the trainer
        if link["href"] != "/cards/A1/216":
            continue

        card_url = urljoin(base_url, link['href'])
        card_response = requests.get(card_url, headers=headers)
        if card_response.status_code != 200:
            print(f'Failed to retrieve card page: {card_url}')
            continue

        card_soup = BeautifulSoup(card_response.text, 'html.parser')

        # Card details
        fetch_card_data(card_soup, set_identifier)

        # Card image
        card_div = card_soup.find("div", class_="card-image")
        if card_div:
            img_tag = card_div.find('img', class_="card shadow resp-w")
            if img_tag:
                img_url = img_tag['src']
                download_image(img_url, output_dir)
            else:
                print(f'No image found on page: {card_url}')
        else:
            print(f'No card image container found on page: {card_url}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python download.py <set_identifier>")
        print("Example: python download.py A1")
    else:
        set_identifier = sys.argv[1]
        main(set_identifier)