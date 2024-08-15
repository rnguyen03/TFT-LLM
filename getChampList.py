import requests
from bs4 import BeautifulSoup
import json

url = 'https://mobalytics.gg/tft/set11/champions'
print(f"Fetching data from {url}...")
response = requests.get(url)
print("Data fetched successfully.")
soup = BeautifulSoup(response.content, 'html.parser')
print("HTML content parsed successfully.")

champions = {}
champion_containers = soup.find_all('div', class_='m-2ni1l0')
print(f"Found {len(champion_containers)} champions.")

for champ in champion_containers:
    print(champ)
    name_elem = champ.find('span', class_='m-1xvjosc')
    cost_elem = champ.find('div', class_='m-s5xdrg')
    trait_elems = champ.find_all('div', class_='m-1jj7hqe')

    if name_elem is not None:
        name = name_elem.text.strip()
    else:
        name = "Unknown"
        print("Champion name element not found.")

    if cost_elem is not None:
        cost = cost_elem.text.strip()[-1]
    else:
        cost = "Unknown"
        print("Champion cost element not found.")

    if trait_elems:
        traits = [trait.get_text(strip=True) for trait in trait_elems]
    else:
        traits = []
        print("Champion traits elements not found.")

    print(f"Processing champion: {name}")
    print(f"  Cost: {cost}")
    print(f"  Traits: {traits}")

    champions[name] = {'cost': cost, 'traits': traits}

print("All champions processed. Saving to JSON file...")
with open('tft_champions.json', 'w') as json_file:
    json.dump(champions, json_file, indent=4)
print("Data saved to tft_champions.json.")
