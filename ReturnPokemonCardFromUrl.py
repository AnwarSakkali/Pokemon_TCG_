# https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/
# https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/series/sv01/1/
# https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/series/swsh1/1/

from bs4 import BeautifulSoup
import requests

# Main function to retrieve information about a specific card
# parameters: | language | the expansion a card comes from | the cardsID within the expansion
def ReturnPokemonCardWithDeckAndCardID(language, TCGset, card):
    match language:
        case "en":
            URL = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/series/" + TCGset + "/" + str(card) + "/"
        case "fr":
            URL = "https://www.pokemon.com/fr/jcc-pokemon/cartes-pokemon/series/" + TCGset + "/" + str(card) + "/"
        case "es":
            URL = "https://www.pokemon.com/es/jcc-pokemon/cartas-pokemon/series/" + TCGset + "/" + str(card) + "/"

    ReturnPokemonCardWithUrl(URL)
    

def ReturnPokemonCardWithUrl(URL):
    print("--------------------------------------")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    section = soup.find("section", class_="mosaic section card-detail")

    ## basic Pokémon information
    getBasicPokemonInfo(section)
    
    # Ruleboxes and moveset
    getAbilities(section)
    
    ## Pokemon Stats
    getPokemonStats(section)

    ## Illustrator
    illustrator = section.find("h4", class_="highlight")
    name = illustrator.find("a").text.strip()
    print("illustrator: " + name)


# get basic information about a pokemon, this includes:
# name | cardtype | (potential) evolution | HP
def getBasicPokemonInfo(section):
    card_description = section.find("div", class_="card-description")
    PokemonName = card_description.find("h1").text.strip()
    cardType = card_description.find("div", class_="card-type")
    Type = cardType.find("h2").text
    
    evolution = ""
    string = ""
    try:
        evolution = cardType.find("h4").text.split()
        for e in evolution:
            string += e + " "
    except:
        pass

    cardHP = card_description.find("span", class_="card-hp").text.strip()

    print("\nThis pokemon has the following information: ")
    if evolution != "":
        print("Name: " + PokemonName + ", cardType: " + Type + ", Evolution: " + string + ", cardHP: " + cardHP + "\n")
    else:
        print("Name: " + PokemonName + ", cardType: " + Type + ", cardHP: + " + cardHP + "\n")

#Get abilities from the pokemon, this includes:
# Ability | ruleboxes | moves
def getAbilities(section):
    pokemonAbilities = section.find("div", class_="pokemon-abilities")
    EachAbility = pokemonAbilities.find_all("div", class_="ability")

    for ability in EachAbility:
        abilityArray = ability.text.split("\n")
        abilityArray = list([x.strip() for x in abilityArray])
        abilityArray = [i for i in abilityArray if not (i == '')]
                        
        if abilityArray[0] == "V rule":
            print("V Rule: " + abilityArray[1])
        elif abilityArray[0] == 'Ability':
            print("Ability: " + abilityArray[1] + ": " + abilityArray[2])
        elif len(abilityArray) == 1:
            print(abilityArray[0])
        elif abilityArray[0] == 'VSTAR Power':
            print("VSTAR Power | " + abilityArray[1] + ": " + abilityArray[2] + ": " + abilityArray[3])
        else:
            title = abilityArray[0]
            description = abilityArray[1]
            damage = ""
            if len(abilityArray) == 2:
                print(title + " : " + description)
            else:
                damage = abilityArray[2]
                print(title + " | " + damage + " : " + description)

# get Pokemon stats, this includes: 
# expansion name | card ID within expansion
def getPokemonStats(section):
    pokemonStats = section.find("div", class_="pokemon-stats")
    divs = pokemonStats.find_all("div")
    # weakness = divs[0].text.strip() | resistance = divs[1].text.strip() | retreatCost = divs[2].text.strip()
    expansion = divs[3]
    expansionName = expansion.find("a").text
    cardId = expansion.find("span").text
    print("Expansion name: " + expansionName + ", cardId: " + cardId)

# GetPokemonInfo()
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "swsh1", 1)  # Celebi
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("fr", "swsh1", 1)  # Celebi
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("es", "swsh1", 1)  # Celebi
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "swsh1", 2) # Roselia
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "sv01", 1) # Pineco
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "swsh10", 18) # Husuian Lilligant VSTAR
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "cel25c", "97_A") # Xerneas-EX
# print("--------------------------------------")
# ReturnPokemonCardWithDeckAndCardID("en", "swsh12tg", "TG05") # Gardevoir
# print("--------------------------------------")