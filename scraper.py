from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv

map = {}

############ Selecting Table #################
source = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight').text
soup = BeautifulSoup(source, 'lxml')
table_data = soup.find('table', class_='wikitable')

#contains number of successful satelite in a launch
count=0
curr_date = ""
for row in table_data.find_all('tr'):
    tds = row.find_all('td')
    if len(tds) > 0:
        rowspan = tds[0].get('rowspan',0)
        if int(rowspan) > 1:
            if curr_date is not "":
                if count > 0:
                    map[curr_date] += 1 
                    count = 0
            
            s = tds[0].span.contents[0].strip()+", 2019"
            curr_date = datetime.strptime(s, "%d %B, %Y").isoformat()

            #initialize the new key to 0
            if curr_date not in map:
                map[curr_date] = 0
        
        result = tds[-1].text.strip()
        if result == "Operational" or result == "Successful" or result == "En Route" :
            count += 1


##################   GENERATING CSV FILE ########### 
csv_file = open('result.csv', '+w')
csv_writter = csv.writer(csv_file)
csv_writter.writerow(["date", "value"])

days = [31,28,31,30,31,30,31,31,30,31,30,31]
months = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']

for i in range(12):
    month = months[i]
    for day in range(1,days[i]+1):
        s = str(day)+" "+month+", 2019"
        date = datetime.strptime(s, "%d %B, %Y").isoformat()
        value = map.get(date, 0)
        csv_writter.writerow([date, value])
csv_file.close()
print("OUTPUT is generated in ./results.csv")