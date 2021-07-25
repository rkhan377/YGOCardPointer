import os

import requests
from bs4 import BeautifulSoup
import banlistHandler as blH
import deckIO as dIO

deckList = dIO.deckInput()
blList = blH.banlistHandler()

def checkBL(card):
    if card.upper in blList:
        i = 0
        while i < len(blList):
            if blList[i] == card.upper():
                if blList.index("Semi-Limited List:") < i:
                    return 25 #"semi"
                elif blList.index("Limited List:") < i:
                    return 50 #"limited"
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

def point():
    print("Pointing cards...")
    i = 0
    while i < len(deckList):
        card = soupString(deckList[i])
        priceRaw = scrapePrice(card)
        rarity = scrapeRarity(card)
        priceAdj = rarityConv(rarity, priceRaw)
        priceAdj = priceAdj*checkBL(card)
        finalPoints = round((priceAdj/.2)/10)
        deckList[i] = deckList[i]+" - "+str(finalPoints)
        i+=1

def txtGen():
    title = ""
    while title == "":
        title = input("Set name for pointed deck file (include file extension .txt): ")
        try:
            f = open(title, "x", encoding="utf-8")
            txt = ""
            for x in deckList:
                txt = txt + x+"\n"
            f.write(txt)
            print("Deck pointing is done.")
            f.close()
            #print("File found at " + os.path.splitext(title))
        except:
            if ".txt" in title:
                print("File already exists, choose another name.")
            else:
                print("Please include .txt in your title.")
            title = ""

point()
txtGen()