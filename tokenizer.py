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
            vocabulary_encode[id] = [len(vocabulary_encode),source[:-5]]
            vocabulary_decode[len(vocabulary_decode)] = id
    
    for thing,name in zip(things,other_things):
        with open(f'{VOCABDIR}{name}.json','w') as src:
            json.dump(thing,src,indent=4)


def encode_composition(comp,encode):
    sentence = []
    for augment in comp['augments']:
        sentence.append(encode[augment][0])
    
    for champion in comp['champions']:
        sentence.append(encode[champion][0])
        for item in comp['champions'][champion]['items']:
            sentence.append(encode[item][0])
    
    return sentence

def decode_composition(sentence,decode):
    result = []
    for word in sentence:
        result.append(decode[word])
    return result

# construct_vocabulary()
