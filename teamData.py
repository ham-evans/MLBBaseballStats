# Hamilton Evans
# 7/4/18
# Data from any team from any year

from pullWebData import pullTable    
    
#Team Name Given: Returns batting data for that team
#Team Name Not Given: Returns All Teams batting data
def pullTeamBattingData (team='', year='2018'):
    team = team.upper()
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