#! /usr/bin/env python
import requests
import bs4
import locale
import os
from multiprocessing import Pool

#declare cost and date as lists
cost= []
date= []

#initialize locale for currency interpretation
locale.setlocale(locale.LC_ALL, '')

#looking for st martin, 7 nights
url = "http://www.moorings.com/vacation-options/bareboat-yacht-charter/destinations/caribbean/st-martin/st-martin/availability?sort_by=price&f[0]=nights%3A7&f[1]=date%3Aduring%7C2015-"

more_url = "&redir=1#lb-content-tabs"

target=open("output.txt", 'w')
target.truncate()

def lets_go():
    #run within a pool of 8 simultaneous processes
    pool = Pool(8)
    #run results(x), with x being range(1,32)
    resulting=pool.map(results, range(1,32))
    #print "----------------------------"
    #print "The Cheapest Travel Day is:"
    #print str(month)+"/"+ str(resulting.index(min(resulting))+1)+": "+ str(min(resulting))
    
    for i in range(1, len(resulting)):
        if resulting[i] != None:
            start_date = resulting[i][0]
            end_price = resulting[i][1]
            full_date = start_date.split()
            day_of_week = full_date[0]
            day_number = full_date[1]
            month_name = full_date[2]
            target.write(month_name + " " + day_number +", " + str(end_price)+"\n") 

#2 digit month, single or two digit day
def set_url(month, day):
   return url +  str(month)+"-"+str(day)+more_url
   
def find_price(url): 
    #default declaration for if there is no available boat
    start_date="Unavailable Unavailable Unavailable"
    prices = "$99999"

    #call url
    response = requests.get(url)
    soup=bs4.BeautifulSoup(response.text)

    #43 footer
    for div in soup.select('#node-boat-23'):
        prices = div.find(attrs={"data-label": "Price for 7 nights"}).text
        start_date=div.find(attrs={"class":"date-display-single"}).text

    #change $ string to float
    endprice=locale.atof(prices[1:])
    full_date = start_date.split()
    day_of_week = full_date[0]
    day_number = full_date[1]
    month_name = full_date[2]

    if prices != "$99999":
        print month_name + " " + day_number +": " + prices             
        return start_date, endprice
    
def results(i):
    use_url=set_url(month, i)
    value=find_price(use_url)
    day = str(month)+"/"+str(i) 
    return value


#clear screen    
os.system('cls' if os.name == 'nt' else 'clear')

#run on each month
null = "0"
for i in range (1,10):
    month = null+str(i) 
    lets_go()

for i in range(10,13):
    month = str(i) 
    lets_go()
  
target.close()
