# https://www.serebii.net/card/english.shtml
# https://www.serebii.net/card/scarletviolet/ (scarlet/violet set)
# https://www.serebii.net/card/scarletviolet/001.shtml (Pineco, first card in set)
# https://www.serebii.net/card/japanese.shtml
# https://www.serebii.net/card/clayburst/ (clayburst set)
# https://www.serebii.net/card/clayburst/001.shtml (Hoppip, first card in set)

# website used: https://realpython.com/beautiful-soup-web-scraper-python/

import requests
from bs4 import BeautifulSoup

# get info from a pokemon card
# parameters: expansion the card comes from | card ID of card within the expansion
def getPokemonInfo(TCGset, cardnumber):
    URL = "https://www.serebii.net/card/" + TCGset + "/" + cardnumber + ".shtml"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="content")
    main = results.find("main")
    div = main.find("div")
    table_tags = div.find_all("table")

    headerTable = table_tags[1]
    a = headerTable.find("table")
    cardIndex = headerTable.find("b")
    
    contentTable = table_tags[3]
    a = contentTable.find_all("table")
    contentTable1 = a[0]
    pokemonName = contentTable1.find("td", class_="main")
    b = contentTable1.find_all("td", class_="medium")
    pokemonHP = b[0]
    pokemonMove = b[2]

    print("ID: " + cardIndex.text.strip())
    print("Name: " + pokemonName.text.strip())
    print("HP: " + pokemonHP.text.strip())
    print("Move: " + pokemonMove.text.strip())

# testfunction to get all cards from clayburst (not finished)
def getAllClayBurstPokemon():
    x = 1
    y = 98      
    while x < y:
        try:
            getPokemonInfo("clayburst", '{:03}'.format(x))    
        except:
            print("this is not a pokemon card")
        print("------------------------------------")
        x += 1

getPokemonInfo("clayburst", '{:03}'.format(1))