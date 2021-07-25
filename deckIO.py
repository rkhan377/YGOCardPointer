import os
import re


def numDupes(cardTxt):
    for letter in cardTxt:
        if letter.isdigit():
            return (int(letter))

def deckInput():
    deckName = ''
    while deckName == '':
        print('Type cancel to quit.')
        print("Note: The .txt files that are supported are the https://yugiohdeck.github.io/ and the https://ygoprodeck.com/ converters.")
        deckName = input("Enter your deck's file path. " + r"(Example: C:\Users\Yugi\Decks\myDeck.txt): ")
        if deckName != 'cancel':
            try:
                deckFile = open(deckName, 'r')
                listTxt = []
                for line in deckFile:
                    stripped_line = line.strip()
                    listTxt.append(stripped_line)
                deckFile.close()
            except:
                print(deckName + " does not exist.")
                deckName = ''

    i = 0
    while i < len(listTxt):
        if any(char.isdigit() for char in listTxt[i][0:4])==False:
            listTxt[i] = "REMOVE"
        i += 1
    listTxt = list(dict.fromkeys(listTxt))
    del listTxt[0]
    index = len(listTxt)
    i=0
    while i < index:
        j=1
        if numDupes(listTxt[i]) > 1:
            while j < numDupes(listTxt[i]):
                listTxt.append(listTxt[i])
                j+=1
        i += 1
    i=0
    while i < len(listTxt):
        listTxt[i] = re.sub(r'^.*?x', 'x', listTxt[i])
        listTxt[i]=listTxt[i][2:]
        i+=1
    listTxt.sort()
    return listTxt

def txtGen(deckList):
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
            print("Deck is located in "+os.path.dirname(os.path.abspath(__file__)))
        except:
            if ".txt" in title:
                print("File already exists, choose another name.")
            else:
                print("Please include .txt in your title.")
            title = ""
