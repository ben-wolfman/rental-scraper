from bs4 import BeautifulSoup as soup
import requests
import json
import csv

urls = ['https://www.kijiji.ca/b-apartments-condos/calgary/apartment__condo/c37l1700199a29276001']
rentArr = []
master = []

i = 1
while i <= 2:
    urls.append('https://www.kijiji.ca/b-apartments-condos/calgary/apartment__condo/page-' + str(i+1) + '/c37l1700199a29276001')
    i += 1


#gets a response from the url
for url in urls:
    response = requests.get(url, timeout = 5)
    content = soup(response.content, "html.parser")
    for prop in content.findAll('div', attrs={"class": "search-item"}):
        for e in prop.findAll('a', href=True):
            link = 'https://www.kijiji.ca' + e['href']
        rentArr.append(link)

print(rentArr)

for url in rentArr:
    response = requests.get(url, timeout = 10)
    content = soup(response.content, "html.parser")
    #***********************************************************************
    if content.find('span', attrs={"class": "address-3617944557"}) != None:
        location = content.find('span', attrs={"class": "address-3617944557"}).text
    else:
        location = "";
    #***********************************************************************
    if content.findAll('dd', attrs={"class": "twoLinesValue-2815147826"})[1] != None:
        beds = content.findAll('dd', attrs={"class": "twoLinesValue-2815147826"})[1].text
    else:
        beds = "";
    #***********************************************************************
    if content.findAll('dd', attrs={"class": "twoLinesValue-2815147826"})[2] != None:
        baths = content.findAll('dd', attrs={"class": "twoLinesValue-2815147826"})[2].text
    else:
        baths = "";
    #***********************************************************************
    if content.find('span', attrs={"class": "currentPrice-2842943473"}) != None:
        rent = content.find('span', attrs={"class": "currentPrice-2842943473"}).text
    else:
        rent = "";
    #***********************************************************************
    if content.find('div', attrs={"class": "description"}) != None:
        phone = content.find('div', attrs={"class": "description"}).text
    else:
        phone = "";
    #***********************************************************************
    masterObject = {
    "link" : url,
    "location" : location,
    "beds" : beds,
    "baths" : baths,
    "rent" : rent,
    "phone" : phone
    }
    master.append(masterObject)

print(master)

with open('rentData.json', 'w') as file:
    json.dump(master, file)

choice = input("Do you want to print out a list? (y): ")
if choice == 'y':
    with open('rentData.json') as json_data:
        jsonData = json.load(json_data)
        csvData = csv.writer(open("rentData.csv", "w+"))
        csvData.writerow(["link","location","beds","baths","rent","phone"])
        for e in jsonData:
            csvData.writerow([e['link'],e['location'],e['beds'],e['baths'],e['rent'],e['phone']])
