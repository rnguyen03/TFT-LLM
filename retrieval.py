import requests,json,time


TIERS = ['DIAMOND','EMERALD','PLATINUM','GOLD','SILVER','BRONZE','IRON']
UNTIERED = ['challenger','grandmaster','master']
DIVISIONS = ['I','II','III','IV']
REGION = 'na1'
BASE = f"https://{REGION}.api.riotgames.com"
API_KEY = 'RGAPI-0a703964-1b3a-44aa-b97a-051d46ebdee3'
HEADERS = {"X-Riot-Token": API_KEY}
PLAYERDIR = 'data/players/'
GAMESDIR = 'data/games/'
GAMESPERPLAYER = 1

def get_untiered():
    for tier in UNTIERED:
        url = f'{BASE}/tft/league/v1/{tier}'
        response = requests.get(url,headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print("success")
        else:
            print(f"{response.status_code}")
        with open(f'{PLAYERDIR}{tier}/{tier}.json','w') as src:
            json.dump(data,src,indent = 4)

def get_tiered():
    for tier in TIERS:
        for i,division in enumerate(DIVISIONS):
            
            url = f'{BASE}/tft/league/v1/entries/{tier}/{division}?queue=RANKED_TFT&page=1&api_key={API_KEY}'
            response = requests.get(url)
            time.sleep(0.6)
            if response.status_code == 200:
                data = response.json()
                print("success")
            else:
                print(f"{response.status_code}")
            with open(f'{PLAYERDIR}{tier}{i}.json','w') as src:
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
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={GAMESPERPLAYER}'

        response = requests.get(url, headers=HEADERS)
        time.sleep(0.6)
        if response.status_code == 200:
            match_data = response.json()
            match_ids.update(match_data)
            print(f"Successfully fetched match data for puuid {puuid}")
        else:
            print(f"Error fetching match data for puuid {puuid}: {response.status_code}")
            print(response.json())

    return list(match_ids)

def get_match_data(match_ids):
    matches = []
    for match_id in match_ids:
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'

        response = requests.get(url, headers=HEADERS)
        time.sleep(0.8)
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
    return reformatted_data

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


def populate_matches():
    for tier in TIERS:
        for i,division in enumerate(DIVISIONS):
            puuids = get_summoner_puuids(f'{PLAYERDIR}{tier}{i}.json')
            start = time.perf_counter()
            match_ids = get_match_ids(puuids)
            matches = get_match_data(match_ids)
            data = get_comp_data(matches)
            with open(f'{GAMESDIR}{tier}/{i}.json','w') as src:
                json.dump(data,src,indent=4)
            print(time.perf_counter()-start)

populate_matches()

# get_untiered()
# get_tiered()
# print(get_summoner_puuids('data/players/IRONI.json'))
# print(get_match_ids(get_summoner_puuids('data/players/IRONI.json')))
# print(get_match_data(get_match_ids(get_summoner_puuids('data/players/IRONI.json'))))
# print(get_comp_data(get_match_data(get_match_ids(get_summoner_puuids('data/players/IRONI.json')))))