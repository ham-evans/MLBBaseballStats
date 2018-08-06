# Hamilton Evans
# 7/4/18
# Data for any MLB player from any year

from pullWebData import pullTable


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
    