import requests,json


TIERS = ['DIAMOND','EMERALD','PLATINUM','GOLD','SILVER','BRONZE','IRON']
UNTIERED = ['challenger','grandmaster','master']
DIVISIONS = ['I','II','III','IV']
REGION = 'na1'
BASE = f"https://{REGION}.api.riotgames.com"
API_KEY = 'RGAPI-d88bcffd-a236-4046-9111-50e2027c588f'
HEADERS = {"X-Riot-Token": API_KEY}
PLAYERDIR = 'data/players/'
GAMESDIR = 'data/games/'

def get_untiered():
    for tier in UNTIERED:
        url = f'{BASE}/tft/league/v1/{tier}'
        response = requests.get(url,headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print("success")
        else:
            print(f"{response.status_code}")
        with open(f'{PLAYERDIR}{tier}.json','w') as src:
            json.dump(data,src,indent = 4)

def get_tiered():
    for tier in TIERS:
        for division in DIVISIONS:
            url = f'{BASE}/tft/league/v1/entries/{tier}/{division}?queue=RANKED_TFT&page=1&api_key={API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("success")
            else:
                print(f"{response.status_code}")
            with open(f'{PLAYERDIR}{tier}{division}.json','w') as src:
                json.dump(data,src,indent = 4)

def get_summoner_puuids(fname: str):
    puuids = []

    with open(fname,'r') as src:
        data = json.load(src)

    for player in data:
        puuids.append(player['puuid'])
    return puuids


def get_match_ids(puuids):
    match_ids = set()

    for puuid in puuids:
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=100'

        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            match_data = response.json()
            match_ids.update(match_data)
            print(f"Successfully fetched match data for puuid {puuid}")
        else:
            print(f"Error fetching match data for puuid {puuid}: {response.status_code}")
            print(response.json())
        break

    return list(match_ids)

def get_match_data(match_ids):
    matches = []

    for match_id in match_ids:
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'

        response = requests.get(url, headers=HEADERS)
        # Check if the request was successful
        if response.status_code == 200:
            match_data = response.json()

            if match_data['info']['tft_set_number'] == 12:
                matches.append(match_data)
                print(f"Successfully fetched match data for ID {match_id}")
            else:
                print("Outdated set: ", match_data['info']['tft_set_number'])
                continue
        else:
            print(f"Error fetching match data for ID {match_id}: {response.status_code}")

    return matches

def get_comp_data(matches):
    
    # Initialize the list to store reformatted data
    reformatted_data = []

    # Iterate over each match and each participant in the match
    for match in matches:
        for participant in match['info']['participants']:
            reformatted_data.append(reformat_participant_data(participant))

    # Convert the reformatted data to a JSON string and return it
    return json.dumps(reformatted_data, indent=4)

def reformat_participant_data(participant):
    # Reformat a single participant's data
    return {
        "comp": {
            "champs": [
                {
                    champ['character_id']: {
                        "items": champ['itemNames'],
                        "tier": champ['tier'],
                    }
                }
                for champ in participant['units']
            ]
        },
        "augments": participant['augments'],
        "gold_left": participant['gold_left'],
        "last_round": participant['last_round']
    }

# get_untiered()
# get_tiered()
# print(get_summoner_puuids('data/players/IRONI.json'))
# print(get_match_ids(get_summoner_puuids('data/players/IRONI.json')))
# print(get_match_data(get_match_ids(get_summoner_puuids('data/players/IRONI.json'))))
# print(get_comp_data(get_match_data(get_match_ids(get_summoner_puuids('data/players/IRONI.json')))))