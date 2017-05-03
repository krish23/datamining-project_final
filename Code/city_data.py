import csv
with open('city_data.csv', 'rb') as f:
    reader = csv.reader(f)
    city_data_list = list(reader)

print your_list[1][0]