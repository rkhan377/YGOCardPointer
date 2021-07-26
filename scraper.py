import requests
from bs4 import BeautifulSoup


def checkBL(card, blList):
    if str(card).upper() in blList:
        i = 0
        while i < len(blList):
            if blList[i] == str(card).upper():
                if blList.index("Semi-Limited List:") < i:
                    return 5 #"semi"
                elif blList.index("Limited List:") < i:
                    return 10 #"limited"
                else:
                    return 100 #"forbidden"
            i += 1
    return 1 #unlimited

def rarityConv(rarity, price):
    if rarity == 'Common':
        factor = 1
    elif rarity == 'Rare':
        factor = 1
    elif rarity == 'Super Rare':
        factor = 2
    elif rarity == 'Ultra Rare' or "Premium Gold Rare":
        factor = 6
    elif rarity == 'Secret Rare':
        factor = 20
    else:
        factor = 15
    return price/factor


def soupString(cardName):
    nameInput = str(cardName)
    nameInput = nameInput.replace(' ', '%20')
    URL = 'https://yugiohprices.com/api/get_card_prices/'+nameInput
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    soupString = str(soup)
    return soupString

def scrapeRarity(soupString):
    rarityFirst = soupString.find("rarity")
    raritySec = soupString.find("price_data")
    rarityClean = soupString[rarityFirst:raritySec]
    rarityClean = rarityClean.replace('"', '')
    rarityClean = rarityClean.replace(',', '')
    rarityClean = rarityClean.replace('rarity:', '')
    rarityVal = rarityClean
    return rarityVal

def scrapePrice(soupString):
    priceFirst = soupString.find("low")
    priceSec = soupString.find("average")
    priceClean = soupString[priceFirst:priceSec]
    priceClean = priceClean.replace('"', '')
    priceClean = priceClean.replace(',', '')
    priceClean = priceClean.replace('low:', '')
    priceVal = float(priceClean)
    return priceVal

def point(deckList, blList):
    print("Pointing cards...")
    i = 0
    while i < len(deckList):
        card = soupString(deckList[i])
        priceAdj = rarityConv(scrapeRarity(card), scrapePrice(card))*checkBL(deckList[i], blList)
        finalPoints = round((priceAdj/.2)/10)
        deckList[i] = deckList[i]+" - "+str(finalPoints)
        i+=1
    return deckList
