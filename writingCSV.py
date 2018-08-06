import csv

def csvWriter (filename, data):
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(data)
        for i in range(len(data)):
            csvwriter.writerow(data.iloc[i])
        print('Data sucessfully written')
        
