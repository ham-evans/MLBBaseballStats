# Hamilton Evans
# 7/4/18
# Data from any game on any day, current or past standings 

from pullWebData import pullSoup
import pandas as pd

#Find Names of Leaderboard Sections Given a URL
def findLeaderboardSections ():
    allSections=[]
    
    array = ['https://www.baseball-reference.com/leagues/AL/2018-batting-leaders.shtml', 'https://www.baseball-reference.com/leagues/AL/2018-pitching-leaders.shtml', 'https://www.baseball-reference.com/leagues/AL/2018-batting-leaders.shtml']
    
    for url in array:
        eachSection = []
        soup = pullSoup(url)
        allTables = soup.findAll('table')
        
        for i in range(len(allTables)):
            dataHeader = allTables[i].find('caption')
            dataHeader = str(dataHeader)
            header = dataHeader[dataHeader.find('\">') + 2 : dataHeader.find('</')]
            if (len(header) > 50): 
                header = dataHeader[dataHeader.find("\'>") + 2 : dataHeader.find('</')]
            eachSection.append(header)
        allSections.append(eachSection)
    
    return allSections

#No Section Name: Return all sections and standings for information
#Section Name: Return section name and standings for given section
#Ex input: pullTableLeaderBoard('Batting', 'NL', 'Batting Average')
def pullTableLeaderboard (aspect, league='NL', sectionName='', year='2018'):
    league = league.upper()
    aspect = aspect.lower()
    url = 'https://www.baseball-reference.com/leagues/' + str(league) + '/' + str(year) + '-' + str(aspect) + '-leaders.shtml'
    
    soup = pullSoup(url)
    allTables = soup.findAll('table')
    
    allData=[]
    for i in range(len(allTables)):
        rankOld = 1
        section = []
        dataHeader = allTables[i].find('caption')
        dataHeader = str(dataHeader)
        header = dataHeader[dataHeader.find('">') + 2 : dataHeader.find('</')]
        if (len(header) > 50): 
            header = dataHeader[dataHeader.find("\'>") + 2 : dataHeader.find('</')]
        
        section.append(header)
        people = allTables[i].findAll('tr')

        for person in people:
            player = []
            number = person.find_all('td')
            name = person.find('a')
            number = str(number)
            name = str(name)
            
            for i in range(0,3):
                if (i == 0):
                    rank = number[number.find('rank">') + 6 : number.find('.') ]
                    if (len(rank) > 3):
                        rank = rankOld
                    rankOld = rank
                if (i == 1):
                    playerName = name[name.find('title="') + 7 : name.find('">')]
                if (i == 2): 
                    value = number[number.find('value') + 8 : number.find('<') - 7]
                
            player.append(rank)
            player.append(playerName)
            player.append(value)
            section.append(player)
            
        
        allData.append(section)
    
    if (sectionName!=''): 
        conciseSectionName = ''.join(letter for letter in sectionName if letter.isalnum())
        for section in allData: 
            conciseSection = ''.join(letter for letter in section[0] if letter.isalnum())
            if (conciseSection.lower() == conciseSectionName.lower()):
                section = pd.DataFrame(section)
                return section
    
    allData=pd.DataFrame(allData)
    return allData
    
        



