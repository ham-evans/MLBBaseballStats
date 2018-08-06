import pandas as pd 
import requests
from bs4 import BeautifulSoup
import re

#Pulls HTML fom url
def pullSoup (url): 
    request = requests.get(url)
    commentSkip = re.compile('<!--|-->')
    soup = BeautifulSoup(commentSkip.sub('', request.text), 'lxml')
    return soup

#Returns Table Titles from URL
def findTableNames (url):
    soup = pullSoup(url)
    allDiv = soup.findAll('div', id = 'content')
    allDiv = allDiv[0].findAll("div", id=re.compile("^all"))
    
    ids = []
    for div in allDiv: 
        findTable = str(div.findAll('table'))
        temp = findTable[findTable.find('id=') + 3: findTable.find('>')]
        temp = temp.replace('\"', '')
        if len(temp) > 0:
            ids.append(temp)
    
    return ids

#Given a URL and tableID, returns the data in the table as a DataFrame
def pullTable (url, tableId, league=0):
    soup = pullSoup(url)
    
    allTables = soup.findAll('table', id=str(tableId))
    dataRows = allTables[league].findAll('tr')
    dataHeader = allTables[0].findAll('thead')
    dataHeader = dataHeader[0].findAll("tr")
    dataHeader = dataHeader[0].findAll("th")
    
    gameData = [[td.getText() for td in dataRows[i].findAll(['th','td'])]
        for i in range(len(dataRows))
        ]
    data = pd.DataFrame(gameData)
    
    header = []
    for i in range(len(data.columns)):
        header.append(dataHeader[i].getText())
        
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    
    return data
