import urllib2
import re
import csv
from lxml import html
import requests
from BeautifulSoup import BeautifulSoup

baseURL = "https://www.indeed.com/"
urlList = []


req = urllib2.Request("https://www.indeed.com/cmp/Safeway/salaries", headers={'User-Agent' : "Magic Browser"})
con = urllib2.urlopen(req)
soup = BeautifulSoup(con.read())
#print soup.prettify()


for anchor in soup.findAll('select', id="cmp-salary-loc-select"):
    string = str(anchor)

soup2 = BeautifulSoup(string)
tree = html.fromstring(str(soup2.findAll('option')))

cities_state_value = tree.xpath('//option/@value')

#Get URL for each city

for city_Salary in cities_state_value:
    getUrl = baseURL+str(city_Salary)
    urlList.append(getUrl)

urlList.pop(0)
#print urlList

city_set = []
actual_city = []


with open('city_data.csv', 'rb') as f:
    reader = csv.reader(f)
    city_data_list = list(reader)

    for city_name in city_data_list:
        city_set.append(city_name[0])

def getSalaryByCity(urlName):

    #url = "https://www.indeed.com/cmp/Safeway/salaries?location=US%2FAZ%2FChandler"
    url = urlName
    req2 = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    con2 = urllib2.urlopen(req2)
    soup3 = BeautifulSoup(con2.read())

    #Get the title(city and state)
    tree_title = html.fromstring(str(soup3.findAll('h1', { "class" : "cmp-salary-header-text" })))
    get_city_info = tree_title.xpath('//h1/text()')
    city_title_array = get_city_info[0].split(" ")

    if(len(city_title_array) == 4):
        city = ' '
        state = city_title_array[3]
        #print state
    else:
        city_ = city_title_array[3]
        state_ = city_title_array[4]
        city_and_state = city_

        city_and_state = re.sub(",", "", city_)

        cashier_string = "Cashier"
        cashier_string2 = "Customer Service Associate / Cashier"

        #Get the Salary Description
        tree_salary_dsc = html.fromstring(str(soup3.findAll('div', { "class" : "cmp-sal-description" })))
        get_salary_desc = tree_salary_dsc.xpath('//a/text()')


        '''if (cashier_string in get_salary_desc):
            cashier_string_index = get_salary_desc.index(cashier_string)

            #Get the salary
            print city_and_state
            #print cashier_string

            tree_salary_value = html.fromstring(str(soup3.findAll('div', { "class" : "cmp-sal-summary" })))
            get_salary_value = tree_salary_value.xpath('//span/text()')
            #print get_salary_value[cashier_string_index]

        if (cashier_string2 in get_salary_desc):
            cashier_string2_index = get_salary_desc.index(cashier_string2)

            # Get the salary
            print city_and_state
            #print cashier_string2

            tree_salary_value = html.fromstring(str(soup3.findAll('div', {"class": "cmp-sal-summary"})))
            get_salary_value = tree_salary_value.xpath('//span/text()')
            #print get_salary_value[cashier_string2_index]'''

        # Get the salary
        #print city_and_state
        # print cashier_string

        tree_salary_value = html.fromstring(str(soup3.findAll('div', {"class": "cmp-sal-summary"})))
        get_salary_value = tree_salary_value.xpath('//span/text()')
        print get_salary_value
        #print get_salary_desc

#For each city get all the salary information

for url in urlList:
    getSalaryByCity(url)




