import pandas as pd
from xlrd import open_workbook
addressWorkbook = pd.ExcelFile("E:\Datamining\Project\Res.xlsx")
data = addressWorkbook.parse('Sheet1')
addressDF=pd.DataFrame.from_dict(data)
#print(addressDF)

frames = [];
workBook = pd.ExcelFile("E:\Datamining\Project\Data.xlsx", skiprows=3)
for sheet in workBook.sheet_names:
    dataInSheet = workBook.parse(sheet)
    data=dataInSheet.iloc[:, :3]
    dataFrame = pd.DataFrame.from_dict(data)
    frames.append(dataFrame)

allFrames = pd.concat(frames)
storeDataDF=pd.DataFrame.from_dict(allFrames)

#print(storeData)

DFIntersection = storeDataDF.merge(addressDF,on=['StoreNo'])
print(DFIntersection)

from pandas import ExcelWriter
writer = pd.ExcelWriter("E:\Datamining\Project\CompData.xlsx")
#compData = pd.DataFrame.from_dict(add)
DFIntersection.to_excel(writer,'Sheet1')
writer.save()



    


