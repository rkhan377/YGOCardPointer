import re
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

def banlistHandler():
    print("Updating banlist...")
    banlistPage = requests.get('https://www.yugioh-card.com/en/limited/')
    soup = BeautifulSoup(banlistPage.content, 'html.parser')
    soupString = str(soup)
    #
    # start
    addList = True
    dateEffFirst = soupString.find('Effective from ')
    dateEffSec = soupString.find('<', dateEffFirst)
    dateEff = soupString[dateEffFirst: dateEffSec]
    dateEff = dateEff.replace('Effective from ', '')
    numDateEff = datetime.strptime(dateEff, "%B %d, %Y")
    numDateEff = datetime.date(numDateEff)

    dateNextFirst = soupString.find('The next update after this will be no sooner than  ')
    dateNextSec = soupString.find('.<', dateNextFirst)
    dateNext = soupString[dateNextFirst: dateNextSec]
    dateNext = dateNext.replace('The next update after this will be no sooner than  ', "")
    numDateNext = datetime.strptime(dateNext, "%B %d, %Y")
    numDateNext = datetime.date(numDateNext)
    fileLines = (str(numDateNext) + '\n' + str(numDateEff))

    try:
        f = open("banlist.txt", "x", encoding="utf-8")
        print("No banlist file detected.")
        addList = True
        f.close()
    except:
        print('Banlist file already created.')
        f = open('banlist.txt', 'r', encoding="utf-8")
        nextBanlist = f.read(21)
        dtoNext = datetime.date(datetime.strptime(nextBanlist[0:10], "%Y-%m-%d"))
        dtoEff = datetime.date(datetime.strptime(nextBanlist[11:21], "%Y-%m-%d"))
        today = date.today()
        if today >= dtoNext:  # today is on/after the stored next banlist date
            if dtoEff == numDateEff:  # the new banlist is not availible
                addList = False
                print("Banlist is already up to date.")
            else:
                addList = True
        else:
            print("Banlist is not up to date.")
            addList = False
        f.close()
    finally:
        if addList == True:
            print('Adding cards...')
            forbiddenTxt = '\nForbidden List:\n'
            limimtedTxt = 'Limited List:\n'
            semiTxt = 'Semi-Limited List:\n'
            forbiddenTable = soup.find(text="Card Name").find_parent("table")
            for row in forbiddenTable.find_all("tr")[1:]:
                listF = [cell.get_text(strip=True) for cell in row.find_all("td")]
                forbiddenTxt = forbiddenTxt + re.sub(' +', ' ', listF[1]) + '\n'
            limitedTable = soup.find(text="LEFT ARM OF THE FORBIDDEN ONE").find_parent(
                "table")  # exodia cards are always limited
            for row in limitedTable.find_all("tr")[1:]:
                listL = [cell.get_text(strip=True) for cell in row.find_all("td")]
                limimtedTxt = limimtedTxt + re.sub(' +', ' ', listL[1]) + '\n'
            semiTable = soup.find(text="DESTINY HERO - MALICIOUS").find_parent(
                "table")  # the only cards listed as semi limited are on this table
            for row in semiTable.find_all("tr")[1:]:
                listS = [cell.get_text(strip=True) for cell in row.find_all("td")]
                semiTxt = semiTxt + re.sub(' +', ' ', listS[1]) + '\n'
            banlistOutput = forbiddenTxt + '\n' + limimtedTxt + '\n' + semiTxt
            f = open("banlist.txt", "w", encoding="utf-8")
            f.write(fileLines + str(banlistOutput))
            f.close()
            print('Banlist is now updated.')
        else:
            print('Banlist is up to date.')
        blTxt = open("banlist.txt", "r", encoding="utf-8")
        blList = []
        for line in blTxt:
            stripped_line = line.strip()
            blList.append(stripped_line)
        blTxt.close()
        return blList