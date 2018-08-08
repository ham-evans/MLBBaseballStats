# Hamilton Evans
# 8/7/2018
# Returns head to head stats for a game preview 

from pullWebData import pullSoup
import pandas as pd
    
def pullPreviewStats (url):
    head2head = []
    tables = []
    
    soup = pullSoup(url)
    allTables = soup.findAll('table')
    
    for z in range(len(allTables)):
        matchup = []
        
        tr = allTables[z].findAll('tr')
        
        for i in range(len(tr)): 
            line = []
            
            if (i == 0):
                stats = tr[i].findAll('th')
                if (z == 2 or z == 5): 
                    stats = stats[1:]
                if (len(stats) == 0): 
                    stats = tr[i].findAll('td')
                    
                for element in stats:
                    line.append(element.getText())
                matchup.append(line)    
            else:
                stats = tr[i].findAll('td')
                
                for element in stats:
                    
                    line.append(element.getText())
                    
                matchup.append(line)
    
        tables.append(matchup)

    for element in tables: 
        element = pd.DataFrame (element)
        head2head.append(element)
    
    return head2head
        
    