def construct_vocabulary(sources):
    vocabulary_encode = {}
    vocabulary_decode = {}
    for source in sources:
        with open(source) as src:
            lines = src.readlines()
        for line in lines:
            print(line.split())
            isolated = line.split()[0]
            

            vocabulary_encode[isolated] = len(vocabulary_encode)
            vocabulary_decode[len(vocabulary_decode)] = isolated
    return vocabulary_encode,vocabulary_decode

def construct_composition(sentence,vocabulary):
    pass

def encode_composition(composition,vocabulary_encode):
    sentence = []
    for augment in composition['augments']:
        sentence.append(vocabulary_encode.get(augment,0))
    for champion in composition['champions']:
        sentence.append(vocabulary_encode.get(champion,0))
        for item in vocabulary_encode[champion]['items']:
            sentence.append(vocabulary_encode.get(item,0))
    return sentence

def split():
    pass


sample_comp = {
    'augments':[
        'augment1',
        'augment2',
        'augment3'
    ],
    'champions':{
        'akali':{
            'items':[

            ]
        },
        'ahri':{
            'items':[

            ]
        }
        }
}
sources = [
    'vocabulary/augments.txt',
    'vocabulary/champions.txt',
    'vocabulary/augments.txt']
enc,dec = construct_vocabulary(sources)

sentence = encode_composition(sample_comp,enc)
print(sentence)
