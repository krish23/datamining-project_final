
# coding: utf-8

# In[1]:

from lxml import html
import requests
from bs4 import BeautifulSoup


# In[2]:

page = requests.get('http://local.safeway.com/')
tree = html.fromstring(page.content)
tree


# In[3]:

states = tree.xpath('//a[@class="data_list"]/text()')
states


# In[4]:

def toAd(taddress):
    d = {}
    (d["streetnum"],d["street"],d["city"],d["state"],d["zip"]) = (str(item) for item in taddress)
    return d


# In[5]:

import re
#The store number is located between the dash (-) and the .html
storePattern = re.compile('\-([0-9]+).html$')
#the address is broken down using commas (,) -- let's grab the 5-tuple 
#we'll assign each component to a part of the address using the toAd function
addressPattern = re.compile('^([^\s]+)\s+([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)$')

#we should store all of our stores somewhere
storeLookup = {}
miss = []
for state in states:
    statepage = 'http://local.safeway.com/'+state[2:4].lower()+'/'
    page = requests.get(statepage)
    print (page.status_code)
    print (statepage)
    
    statesoup = BeautifulSoup(page.text, "html")
    #print ("Cities")
    #itterate over each city in the state page
    #cities are located in the a tag, with class type st_item
    for link in statesoup.findAll("a" , "st_item"):
        
        #print (link)
        citypage =  requests.get(link.get("href"))
        citysoup = BeautifulSoup(citypage.text, "html")
        
        #for each store on the state page scrape the list <li> item
        for item in citysoup.findAll("li"):
            if(addressPattern.findall(item.find("a").contents[0])):
                addressList = addressPattern.findall(item.find("a").contents[0])[0]
                #print (addressList)
                storenum = int(storePattern.findall(item.find("a").get("href"))[0])
                
                #print (storenum, addressList)
                #make sure we have a valid address?
                if(len(addressList)==5):
                    storeLookup[storenum]= toAd(addressList)
                else:
                    storeLookup[storenum]= toAd(("error",)*5)
            else:
                miss.append(item.find("a").contents[0])

import pandas as pd
writer = pd.ExcelWriter("E:\Datamining\Project\Res.xlsx")
safewayDF = pd.DataFrame.from_dict(storeLookup).T
safewayDF.to_excel(writer,"Sheet1")
writer.save()

frames = [];
from xlrd import open_workbook
workBook = pd.ExcelFile("E:\Datamining\Project\Data.xlsx", skiprows=3)
for sheet in workBook.sheet_names:
    dataInSheet = workBook.parse(sheet)
    data=dataInSheet.iloc[:, :3]
    dataFrame = pd.DataFrame.from_dict(data)
    frames.append(dataFrame)

allFrames = pd.concat(frames)
storeData=pd.DataFrame.from_dict(allFrames)
#print(storeData)


from pandas import ExcelWriter
#writer = pd.ExcelWriter("E:\Datamining\Project\Res.xlsx")
storeNos=[]
for index, rows in storeData.iterrows():
    #cashierNos.append(rows[0])
    storeNos.append(rows[1])
    #riskFactors.append(rows[2])

add ={}     
for storeNo in storeNos:      
    if storeNo in safewayDF.index:
        try:
            add[storeNo] = {'streetnum' : safewayDF.at[storeNo,'streetnum'],
                        'street' : safewayDF.at[storeNo,'street'],
                        'city' : safewayDF.at[storeNo,'city'],
                        'state' : safewayDF.at[storeNo,'state'],
                        'zip' : safewayDF.at[storeNo,'zip'],
                        'Risk Factor': storeData.at[storeNo,'Total Risk Factor']
                        }
        
        except KeyError as exc:
            print ("Store No "+str(storeNo)+" Not Found")
compData = pd.DataFrame.from_dict(add).T
regionDF.to_excel(writer,Sheet1)
writer.save()
    


