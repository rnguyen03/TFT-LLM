from typing import List
import requests
import json

# Replace with your actual API key
API_KEY = 'RGAPI-3258e945-4209-4704-aa52-23b14778b3e7'
region = 'na1'

# Endpoint URL for fetching match history
baseURL = f"https://{region}.api.riotgames.com"

def get_challengers():
    url = f'{baseURL}/tft/league/v1/challenger'
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        summoners_data = response.json()
        print("Successfully fetched challenger data!")
    else:
        print(f"Error fetching challenger data: {response.status_code}")
        return []

    # Extract summoner IDs from the data
    summoner_ids = [entry['summonerId'] for entry in summoners_data.get('entries', [])]
    return summoner_ids

def get_summoner_puuids(summoner_ids: List[str]):
    puuids = []

    for summoner_id in summoner_ids:
        url = f'{baseURL}/tft/league/v1/entries/by-summoner/{summoner_id}'
        headers = {
            "X-Riot-Token": API_KEY
        }

        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            summoner_data = response.json()
            puuids.append(summoner_data[0]['puuid'])
            print(f"Successfully fetched summoner data for ID {summoner_id}!")
        else:
            print(f"Error fetching summoner data for ID {summoner_id}: {response.status_code}")

        break # Only fetch data for the first summoner for now

    return puuids

def get_match_ids(puuids: List[str]):
    match_ids = set()

    for puuid in puuids:
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=100'
        headers = {
            "X-Riot-Token": API_KEY
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            match_data = response.json()
            match_ids.update(match_data)
            print(f"Successfully fetched match data for puuid {puuid}!")
        else:
            print(f"Error fetching match data for puuid {puuid}: {response.status_code}")
            print(response.json())

    return list(match_ids)

def get_match_data(match_ids: List[str]):
    matches = []

    for match_id in match_ids:
        url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'
        headers = {
            "X-Riot-Token": API_KEY
        }

        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            match_data = response.json()
            matches.append(match_data)
            print(f"Successfully fetched match data for ID {match_id}!")
        else:
            print(f"Error fetching match data for ID {match_id}: {response.status_code}")

    return matches

ids = get_challengers()
puuids = get_summoner_puuids(ids)
match_ids = get_match_ids(puuids)
matches = get_match_data(match_ids)

# Save matches into .JSON file
with open('matches.json', 'w') as matches_file:
    json.dump(matches, matches_file, indent=4)
