import requests,json

# simple word leven tokenizer

CURRENTVERSION = '14.16.1'
BASE = f'https://ddragon.leagueoflegends.com/cdn/{CURRENTVERSION}/data/en_US/tft-'
SOURCES = ['champion.json','item.json','augments.json']
VOCABDIR = 'vocabulary/'

def construct_vocabulary():
    vocabulary_encode = {}
    vocabulary_decode = {}

    things = [vocabulary_encode,vocabulary_decode]
    other_things =['encode','decode',]
    for source in SOURCES:
        response = requests.get(f'{BASE}{source}').json()
        
        for key,value in response['data'].items():
            
            id = value['id']
            vocabulary_encode[id] = [len(vocabulary_encode)+1,source[:-5]]
            vocabulary_decode[len(vocabulary_decode)+1] = id
    
    for thing,name in zip(things,other_things):
        with open(f'{VOCABDIR}{name}.json','w') as src:
            json.dump(thing,src,indent=4)



construct_vocabulary()
