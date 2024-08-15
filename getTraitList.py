import requests
from bs4 import BeautifulSoup
import json

url = 'https://blitz.gg/tft/traits/overview?set=11'  # Update with the correct URL if different
print(f"Fetching data from {url}...")
response = requests.get(url)
print("Data fetched successfully.")
soup = BeautifulSoup(response.content, 'html.parser')
print("HTML content parsed successfully.")

traits = {}
trait_containers = soup.find_all('div', class_='⚡cefe3e0c')
print(f"Found {len(trait_containers)} traits.")

for trait in trait_containers:
    trait_name_elem = trait.find('div', class_='type-body2')
    trait_tier_elems = trait.find_all('span', class_='⚡177c08b6')

    if trait_name_elem is not None:
        name = trait_name_elem.text.strip()
        print(f"Processing trait: {name}")
    else:
        name = "Unknown"
        print("Trait name element not found.")
        continue

    if trait_tier_elems:
        for tier_elem in trait_tier_elems:
            if tier_elem is not None:
                tier_value = tier_elem.text.strip()
                tier_key = f"{tier_value} {name}"
                if name not in traits:
                    traits[name] = {}
                traits[name][tier_key] = int(tier_value)
            else:
                print("Trait tier value element not found.")
    else:
        print("Trait tier elements not found.")

print("All traits processed. Saving to JSON file...")
with open('tft_traits.json', 'w') as json_file:
    json.dump(traits, json_file, indent=4)
print("Data saved to tft_traits.json.")
