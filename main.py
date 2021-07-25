import scraper
import banlistHandler as blH
import deckIO as dIO

def YGOPointer():
    deckList = dIO.deckInput()
    blList = blH.banlistHandler()
    dIO.txtGen(scraper.point(deckList, blList))

YGOPointer()

isDone = False
while isDone == False:
    response = input("\nDo you want to point more decks? ")
    if (response.upper()[0] == "N"):
        print("\nBye!")
        isDone = True
    else:
        isDone = False
        YGOPointer()
