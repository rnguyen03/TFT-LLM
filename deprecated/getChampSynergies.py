import json

# Load champion data
with open('tft_champions.json', 'r') as file:
    champData = json.load(file)

# Load trait data
with open('tft_traits.json', 'r') as file:
    traitData = json.load(file)

# Define the champion list and initialize dictionaries
champList = ["Aatrox", "Riven", "Sylas", "Sivir", "Zoe"]
traitFreq = {}
commonSynergies = []

# Calculate the frequency of each trait in the given champion list
for champ in champList:
    champ_traits = champData[champ][
        'traits']  # Assuming champData[champ] is a dictionary with 'traits' key
    for trait in champ_traits:
        if trait not in traitFreq:
            traitFreq[trait] = 0
        traitFreq[trait] += 1

# Print trait frequency
print("Trait frequencies:", traitFreq)

# Collect common synergies based on trait frequency
for trait, count in traitFreq.items():
    print(f"Processing trait: {trait}")
    trait_levels = sorted(
        traitData[trait].keys(), key=int,
        reverse=True)  # Get available trait levels sorted in descending order
    print(f"Available levels for {trait}: {trait_levels}")
    for level in trait_levels:
        if int(
                level
        ) <= count:  # Find the highest possible tier that is less than or equal to the count
            commonSynergies.append(traitData[trait][level])
            break

# Print common synergies
print("Common synergies:")
for synergy in commonSynergies:
    print(synergy)
