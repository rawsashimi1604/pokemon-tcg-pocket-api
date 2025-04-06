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
import re

def snake_case(name):
    """Convert set name to snake_case."""
    name = re.sub(r'[^a-zA-Z0-9\s]', '', name)  # Remove special characters
    return '_'.join(name.lower().split())

def download_image(img_url, folder):
    """Download an image from the given URL to the specified folder."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; YourBot/1.0; +http://yourdomain.com/bot)'
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

def fetch_card_data(soup: BeautifulSoup):
    """Fetches card data from soup html and adds it into the specified folder"""
    
    card_data = {}

    # Card name
    card_data['name'] = soup.find("p", class_="card-text-title").text.split("-")[0].strip()
    card_data['type'] = soup.find("p", class_="card-text-title").text.split("-")[1].strip() 
    card_data['hp'] = soup.find("p", class_="card-text-title").text.split("-")[2].strip()

    # Card details (id, rarity, pack)
    card_details = soup.find("div", class_="prints-current-details").find_all("span")[1].text
    card_data["id"] = card_details.split("·")[0].strip()[1:] # take out the #
    card_data["rarity"] = card_details.split("·")[1].strip()
    card_data["pack"] = card_details.split("·")[2].strip() # Should format the pack name

    print(card_data)


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
        card_url = urljoin(base_url, link['href'])
        card_response = requests.get(card_url, headers=headers)
        if card_response.status_code != 200:
            print(f'Failed to retrieve card page: {card_url}')
            continue

        card_soup = BeautifulSoup(card_response.text, 'html.parser')

        # Card details
        fetch_card_data(card_soup)

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