#!/usr/bin/python

from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt


myFile = open('trainingData.txt','r')
X = myFile.readlines()

for i in range(0, len(X)):
	X[i] = X[i].replace('\n','').split('\t')
	X[i] = [int(X[i][j]) for j in range(0, len(X[i]))]

myFile.close()

myFile = open('trainingClass.txt', 'r')
Y = myFile.readlines()
for i in range(0, len(X)):
    Y[i] = int(Y[i].replace('\n',''))
    
myFile.close()

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,Y)

#with open('graph.dot','w') as f:
#	f = tree.export_graphviz(clf, out_file=f)

myFile = open('testdata.txt', 'r')
testData = myFile.readlines()

for i in range(0, len(testData)):
	testData[i] = testData[i].replace('\n','').split('\t')
	testData[i] = [int(testData[i][j]) for j in range(0, len(testData[i]))]

result =  clf.predict(testData)
correct = 0
for i in range(0, len(result)):
	if result[i] == Y[i]:
		correct += 1

print float(correct)/len(result)
