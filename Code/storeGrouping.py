#!/usr/bin/python

myFile = open('store.txt', 'r')
data = myFile.readlines()
data = list(set(data))
data = [data[i].replace('\n', '') for i in range(0, len(data))]
dataset = list(set(data))
result = []
for i in range(0, len(dataset)):
	print dataset[i], data.count(dataset[i])




