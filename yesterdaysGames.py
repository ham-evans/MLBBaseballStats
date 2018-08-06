"""
Gray Goolsby
8/5/2018

Pulls all MLB game results from previous day
"""
import pandas as pd
from pullWebData import pullSoup

def yesterdaysGames():
    url = 'https://www.baseball-reference.com/boxes/'
    soup = pullSoup(url)
    
    allTables = soup.findAll('div', {"class": "game_summaries"})
    gameTables = allTables[0].findAll('table')
    games = []

    for i in range(len(gameTables)):
        gameStats = str(gameTables[i].findAll('td')).split(',')
        
        if(i%2 == 0):
            team1 = gameStats[0][gameStats[0].find('>', 6)+1:len(gameStats[0])-9]
            team2 = gameStats[3][gameStats[3].find('>', 6)+1:len(gameStats[3])-9]
            
            team1Score = int(gameStats[1][gameStats[1].find('>')+1:gameStats[1].rfind('<')])
            team2Score = int(gameStats[4][gameStats[4].find('>')+1:gameStats[4].rfind('<')])
            
            if(team1Score>team2Score):
                winningTeam = [team1, team1Score]
                losingTeam = [team2, team2Score]
            else:
                winningTeam = [team2, team2Score]
                losingTeam = [team1, team1Score]

        else:
            winningPitcher = gameStats[1][5:gameStats[1].rfind(')')+1]
            losingPitcher = gameStats[3][5:gameStats[3].rfind(')')+1]
            winningTeam.append(winningPitcher)
            losingTeam.append(losingPitcher)

            game = [winningTeam,losingTeam]
            games.append(game)

    games = pd.DataFrame(games)
    games.columns = ['W', 'L']
    return games
