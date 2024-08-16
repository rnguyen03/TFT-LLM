import torch, torch.nn as nn

# IMPLEMENTED FROM SCRATCH FOR LEARNING PURPOSES
TIERS = ['DIAMOND','EMERALD','PLATINUM','GOLD','SILVER','BRONZE','IRON']
UNTIERED = ['challenger','grandmaster','master']
DIVISIONS = ['I','II','III','IV']

def batch

def encode_composition(comp,encode,max_length):
    sentence = []
    for augment in comp['augments']:
        sentence.append(encode[augment][0])
    
    for champion in comp['champions']:
        sentence.append(encode[champion][0])
        for item in comp['champions'][champion]['items']:
            sentence.append(encode[item][0])
    return 

def decode_composition(sentence,decode):
    result = []
    for word in sentence:
        result.append(decode[word])
    return result



