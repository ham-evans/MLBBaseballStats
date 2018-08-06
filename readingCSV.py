import csv

def csvReader (filename):
    fileInfo = []
    with open(filename, 'rt') as csvfile: 
        data = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
        for row in data:
            fileInfo.append(row)
    print('Data sucessfully read')
    return fileInfo