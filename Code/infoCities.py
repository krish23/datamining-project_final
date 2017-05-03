#!/usr/bin/env python


from lxml import html
import requests
from bs4 import BeautifulSoup


cannotFind = []
populationStart = 110
incomeStart = 126
cityData = []

stateDict = {'Fl':'Florida','Wy':'Wyoming','Sd':'South-Dakota','Ne':'Nebraska','Mt':'Montana','Co':'Colorado','Va':'Virginia','Md':'Maryland','De':'Delaware','Dc':'District-of-Columbia','Nm':'New-Mexico','Az':'Arizona','Wa':'Washington', 'Ak':'Alaska', 'Or':'Oregon', 'Ca':'California', 'Hi':'Hawaii'}

with open("cityData.txt", 'r') as myFile:
	cities = myFile.readlines()

cities = list(set(cities))
for cityData in cities:
	cityData = cityData.split('\t')
	city = cityData[0].replace(' ', '-')
	state = stateDict[cityData[1][:-1]]
	cityPage = 'http://www.city-data.com/city/' + city+ '-' + state + '.html'
	page = requests.get(cityPage)
	if page.status_code == 404:
		cannotFind.append(city)
	else:	
		citySoup = BeautifulSoup(page.text, "lxml")
		populationData = str(citySoup.find("section", "city-population"))
		incomeData = str(citySoup.find("section", "median-income"))
		index = 0
		while populationData[populationStart + index] in  [str(i) for i in range(0,10)] or populationData[populationStart + index] == ',':
			index += 1
		
		incomeIndex = 0
		while incomeData[incomeStart + incomeIndex] in  [str(i) for i in range(0,10)] or incomeData[incomeStart + incomeIndex] == ',':
			incomeIndex += 1
		cityPopulationData = city + " " + state + " " + populationData[populationStart:populationStart + index] + " "  + incomeData[incomeStart:incomeStart + incomeIndex]
		cityData.append(cityPopulationData)

		print cityPopulationData
print cannotFind			

