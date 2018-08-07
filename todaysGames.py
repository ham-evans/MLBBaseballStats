# Hamilton Evans 
# 8/6/2018
# Returns today's games, pitching matchups, and lineups 

from pullWebData import pullSoup
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
            homeTeamName = gameStats[0][gameStats[0].find('teams/') + 6:gameStats[0].find('/2018')]
            awayTeamName = gameStats[3][gameStats[3].find('teams/') + 6:gameStats[3].find('/2018')]
            
            homeTeamRecord = gameStats[0][gameStats[0].find('span') + 24:gameStats[0].find('</span') - 2]
            awayTeamRecord = gameStats[3][gameStats[3].find('span') + 24:gameStats[3].find('</span') - 2]

            homeTeam = [homeTeamName, homeTeamRecord]
            awayTeam = [awayTeamName, awayTeamRecord]

        else:
            homePitcher = gameStats[1][gameStats[1].find('">') + 2:gameStats[1].find('</a>')]
            awayPitcher = gameStats[7][gameStats[7].find('">') + 2:gameStats[7].find('</a>')]

            homeTeam.append(homePitcher)
            awayTeam.append(awayPitcher)
    
            homePitcherStats = pitcherStats(gameStats[1:])
            awayPitcherStats = pitcherStats(gameStats[7:])
            
            homeTeam.append(homePitcherStats)
            awayTeam.append(awayPitcherStats)

            game = [homeTeam, awayTeam]
            games.append(game)

    games = pd.DataFrame(games)
    games.columns = ['Home', 'Away']
    
    return games


def pitcherStats (gameStats):
    pitcherStats = ''
    pitcherStats += gameStats[0][gameStats[0].find('(') + 1:]
    pitcherStats += gameStats[1][gameStats[1].find(' '):]
    pitcherStats += gameStats[2][gameStats[2].find(' '):]
    pitcherStats += gameStats[3][gameStats[3].find(' '):]
    pitcherStats += gameStats[4][gameStats[4].find(' '):gameStats[4].find('</') - 1]
    
    return pitcherStats 