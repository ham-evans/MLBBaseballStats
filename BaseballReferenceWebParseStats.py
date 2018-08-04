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

#Given No Division: Pulls either current standings, or given a year the year end standings 
#Given Division: Pulls either current standings for that division, or given a year the year end standings for that Division 
def pullStandings (year=2018, division='expanded_standings_overall'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standings.shtml'
    league = 0
        
    if (division!='expanded_standings_overall'):
        divisionArray = division.split(' ')
        if (divisionArray[0] == 'NL'): 
            league = 1
            
        if (divisionArray[1] == 'E'): 
            division = 'standings_E'
        elif (divisionArray[1] == 'C'): 
            division = 'standings_C'
        elif (divisionArray[1] == 'W'): 
            division = 'standings_W'
        else: 
            print('That Division is not Avaliable')
    
    standingsTable = pullTable(url, division, league)
    return standingsTable

#No Date Given: Pulls team scores from entire year
#Date Given: Pulls team score from specific date
#Team ex: 'LAD'
#Date ex: '7/23'
def pullGameData (team, year='2018', date=''):
    team = team.upper()
    url = "http://www.baseball-reference.com/teams/" + str(team) + "/" + str(year) + "-schedule-scores.shtml"
    scoreTable = pullTable (url, 'team_schedule')
    gameDate = scoreTable['Date']
    teamSchedule = scoreTable
    
    if (date!=''): 
        allDates = []
        for game in gameDate:
            daySlash = ''
            dateArray = (game.split(' '))
            month = dateArray[1]
            day = dateArray[2]
            
            mapping = {"Mar": "3", "Apr": "4", "May": "5", "Jun": "6", "Jul": "7", "Aug": "8","Sep": "9", "Oct": "10", "Nov":"11"}
            monthNum = mapping[month]
            daySlash = (str(monthNum) + '/' + str(day))
            
            allDates.append(daySlash)
            
        for i in range(len(allDates)):
            if (allDates[i] == date):
                teamSchedule = (scoreTable.iloc[i])
                break
            else: 
                teamSchedule = (str(team) + ' did not play on ' + str(date) + '/' + str(year))
                
    return teamSchedule

#Returns PLayer Batting Data
#Name ex: 'Bryce Harper' 
def pullPlayerBattingData (name, year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-batting.shtml'
    hittersData = pullTable (url, 'players_standard_batting')
    players = hittersData['Name']
    
    for i in range(len(players)):
        concisePlayer = ''.join(letter for letter in players[i] if letter.isalnum())
        conciseName = ''.join(letter for letter in name if letter.isalnum())
        if (concisePlayer.lower() == conciseName.lower()):
            return (hittersData.iloc[i])
    
    return ('Batting data for ' + str(name) + ' in ' + str(year) + ' is not avaliable.')

#Returns Player Pitching Data
def pullPlayerPitchingData (name, year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-pitching.shtml'
    pitchersData = pullTable (url, 'players_standard_pitching')
    players = pitchersData['Name']
    
    for i in range(len(players)):
        concisePlayer = ''.join(letter for letter in players[i] if letter.isalnum())
        conciseName = ''.join(letter for letter in name if letter.isalnum())
        if (concisePlayer.lower() == conciseName.lower()):
            return (pitchersData.iloc[i])
    
    return ('Pitching data for ' + str(name) + ' in ' + str(year) + ' is not avaliable.')

#Returns Player Fielding Data
def pullPlayerFieldingData (name, year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-fielding.shtml'
    fieldersData = pullTable (url, 'players_players_standard_fielding_fielding')
    players = fieldersData['Name']
    
    for i in range(len(players)):
        concisePlayer = ''.join(letter for letter in players[i] if letter.isalnum())
        conciseName = ''.join(letter for letter in name if letter.isalnum())
        if (concisePlayer.lower() == conciseName.lower()):
            return (fieldersData.iloc[i])
    
    return ('Fielding data for ' + str(name) + ' in ' + str(year) + ' is not avaliable.')

#Returns All Player Data
def pullPlayerData (name, year='2018'):
    battingData = pullPlayerBattingData (name, year)
    pitchingData = pullPlayerPitchingData (name, year)
    fieldingData = pullPlayerFieldingData (name, year)
    
    dataPlayer = []
    
    dataPlayer.append(battingData)
    dataPlayer.append(pitchingData)
    dataPlayer.append(fieldingData)
    
    return dataPlayer
    
    
    
#Team Name Given: Returns batting data for that team
#Team Name Not Given: Returns All Teams batting data
def pullTeamBattingData (team='', year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-batting.shtml'
    teamBattingData = pullTable(url, 'teams_standard_batting')
    
    teams = teamBattingData['Tm']
    
    if (team!=''):
        for i in range(len(teams)): 
            if (teams[i] == team):
                return teamBattingData.iloc[i]
    
    return teamBattingData

#Team Name Given: Returns batting data for that team
#Team Name Not Given: Returns All Teams batting data
def pullTeamPitchingData (team='', year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-pitching.shtml'
    teamPitchingData = pullTable(url, 'teams_standard_pitching')
    
    teams = teamPitchingData['Tm']
    
    if (team!=''):
        for i in range(len(teams)): 
            if (teams[i] == team):
                return teamPitchingData.iloc[i]
    
    return teamPitchingData

#Team Name Given: Returns fielding data for that team
#Team Name Not Given: Returns All Teams fielding data       
def pullTeamFieldingData (team='', year='2018'):
    url = 'https://www.baseball-reference.com/leagues/MLB/' + str(year) + '-standard-fielding.shtml'
    teamFieldingData = pullTable(url, 'teams_standard_fielding')
    
    teams = teamFieldingData['Tm']
    
    if (team!=''):
        for i in range(len(teams)): 
            if (teams[i] == team):
                return teamFieldingData.iloc[i]
        
    return teamFieldingData

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
    
        

