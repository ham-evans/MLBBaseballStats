# Hamilton Evans
# 7/4/18
# Data from any game on any day, current or past standings 

from pullWebData import pullTable

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
