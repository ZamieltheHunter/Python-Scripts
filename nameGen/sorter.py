import csv

sortedTable = [[0 for x in range(20)] for y in range(15)]
with open("unsorted.csv","r") as csvfile:
    tableReader = csv.reader(csvfile)
    for i in range(0,20):
        x = next(tableReader)
        for j in range(0,5):
            sortedTable[j][i] = x[j]
    for i in range(20,40):
        x = next(tableReader)
        for j in range(5,10):
            sortedTable[j][i - 20] = x[j - 5]
    for i in range(40,60):
        x = next(tableReader)
        for j in range(10,15):
            sortedTable[j][i - 40] = x[j - 10]
with open("sorted.csv", "w") as csvfile:
    tableWriter = csv.writer(csvfile)
    [tableWriter.writerow(r) for r in sortedTable]
for x in sortedTable:
    print(x)
