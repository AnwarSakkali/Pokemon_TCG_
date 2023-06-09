# Look up which expansions exist within a pokemon generation
from bs4 import BeautifulSoup
from Dicts import SwShDict
import requests

# obtain the expansions that an generation has
def GetExpansionInfo():
    # get website info
    URL = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # get to the part where the expansions are shown
    body = soup.find("body")
    container = body.find_all("div")
    div = container[19]
    fieldsets = div.find_all("fieldset")

    # Variables
    ExpansionScarletViolet = fieldsets[8]
    ExpansionSwordShield = fieldsets[9]
    ExpansionSunMoon = fieldsets[10]
    ExpansionXY = fieldsets[11]
    ExpansionBlackWhite = fieldsets[12]
    ExpansionCallOfLegendsAndHGSS = fieldsets[13]
    ExpansionPlatinum = fieldsets[14]
    ExpansionDiamondAndPearl = fieldsets[15]
    ExpensionEX = fieldsets[16]
    TCGset = ExpansionSwordShield
    count = 0

    # print every set within an expansion
    print("####### Get expansion pack from official Pokemon website TCG Database:")
    spans = TCGset.find_all("span")
    for span in spans:
        count += 1
        print(SwShDict.get(span.text.strip()))
    print("####### Length of current expansion is: " + str(count))

# search a pokemon through the official pokemon website's database
def useSearchEngine(pokemon):
    allPokemonUrls = []
    # url structure
    base = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/"
    cardInfo = "?cardName=" + pokemon + "&cardText="
    evolution = "&evolvesFrom="
    format = "&format="
    hp = "&hitPointsMin=0&hitPointsMax=340"
    retreatCost = "&retreatCostMin=0&retreatCostMax=5"
    attackCost = "&totalAttackCostMin=0&totalAttackCostMax=5"
    artist = "&particularArtist="
    submit = "&advancedSubmit="

    URL = base + cardInfo + evolution + format + hp + retreatCost + attackCost + artist + submit

    # get information from the website
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    ul = soup.find("ul", class_="cards-grid clear")
    lis = ul.find_all("li")
    for a in lis:
        a = a.find("a")
        pokemonUrl = "https://www.pokemon.com" + a['href']
        allPokemonUrls.append(pokemonUrl)

    # get info on how many pages the search result has
    button = soup.find(id="cards-load-more")
    pages = button.find_all("span")
    text = pages[1].text
    pagenumber = text.split(" ")[2]

    # go through the different pages and get those urls too
    i = 2
    while i <= int(pagenumber):
        cardInfo = str(i) + "?cardName=" + pokemon + "&cardText="
        URL = base + cardInfo + evolution + format + hp + retreatCost + attackCost + artist + submit
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        ul = soup.find("ul", class_="cards-grid clear")
        lis = ul.find_all("li")
        for a in lis:
            a = a.find("a")
            pokemonUrl = "https://www.pokemon.com" + a['href']
            allPokemonUrls.append(pokemonUrl)
        i += 1
    return allPokemonUrls


from ReturnPokemonCardFromUrl import ReturnPokemonCardWithUrl
print("Write down the Pokémon you want to look up:")
string = input()
print("loading...")
list = useSearchEngine(string)
for url in list:
    ReturnPokemonCardWithUrl(url)
input()