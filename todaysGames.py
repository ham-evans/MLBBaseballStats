# Hamilton Evans 
# 8/6/2018
# Returns today's games and pitching matchups

from pullWebData import pullSoup
from todaysPreviewStats import pullPreviewStats
import pandas as pd

def todaysGames ():
    url = 'https://www.baseball-reference.com/previews/'
    soup = pullSoup(url)
    
    allTables = soup.findAll('div', {"class": "game_summaries"})
    gameTables = allTables[0].findAll('table')
    games = []

    for i in range(len(gameTables)):
        gameStats = str(gameTables[i].findAll('td')).split(',')
        
        if(i%2 == 0):
            game = []
            awayTeamName = gameStats[0][gameStats[0].find('teams/') + 6:gameStats[0].find('/2018')]
            homeTeamName = gameStats[3][gameStats[3].find('teams/') + 6:gameStats[3].find('/2018')]
            
            awayTeamRecord = gameStats[0][gameStats[0].find('span') + 24:gameStats[0].find('</span') - 2]
            homeTeamRecord = gameStats[3][gameStats[3].find('span') + 24:gameStats[3].find('</span') - 2]
            
            gameUrl = 'https://www.baseball-reference.com/' + str(gameStats[2][gameStats[2].find('/previews'):gameStats[2].find('">Preview')])
            game.append(gameUrl)
            
            awayTeam = [awayTeamName, awayTeamRecord]
            homeTeam = [homeTeamName, homeTeamRecord]

        else:
            index2 = 7 # Dealing with case where Home pitcher doesn't have a jersey number yet
            if (len(gameStats) < 12): 
                index2 = 6
                
            awayPitcher = gameStats[1][gameStats[1].find('">') + 2:gameStats[1].find('</a>')]
            homePitcher = gameStats[index2][gameStats[index2].find('">') + 2:gameStats[index2].find('</a>')]

            awayTeam.append(awayPitcher)
            homeTeam.append(homePitcher)
            
            awayTeam = pitcherStats(gameStats[index2:], awayTeam)
            homeTeam = pitcherStats(gameStats[1:(index2-1)], homeTeam)
            
            for element in homeTeam: 
                game.append(element)
            for element in awayTeam: 
                game.append(element)
                
            games.append(game)

    games = pd.DataFrame(games)
    games.columns = ['Game Url', 'Home Team', 'Home Record', 'Home Starter', 'HS #', 'HS Age', 'HS Hand', 'HS Record', 'HS ERA', 'Away Team', 'Away Record', 'Away Starter', 'AS #', 'AS Age', 'AS Hand', 'AS Record', 'AS ERA']
    
    return games

def pitcherStats (gameStats, array):
    if (len(gameStats)<5):
        array.append('None')
    array.append(gameStats[0][gameStats[0].find('(') + 1:])
    array.append(gameStats[1][gameStats[1].find(' '):])
    array.append(gameStats[2][gameStats[2].find(' '):])
    if (len(gameStats)>4):
        array.append(gameStats[3][gameStats[3].find(' '):])
        array.append(gameStats[4][gameStats[4].find(' '):gameStats[4].find('</') - 1])
    else: 
        array.append(gameStats[3][gameStats[3].find(' '):gameStats[3].find('</') - 1])
    
    return array 

def matchupURL (i):
    todaysGamesDF = todaysGames ()
    return todaysGamesDF.iloc[i, 0]


    