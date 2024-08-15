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

def get_summoner_puuids():
    pass

def get_match_ids():
    pass 

def get_match_data():
    pass


get_untiered()
get_tiered()
