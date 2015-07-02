import csv
from collections import OrderedDict
reader = csv.reader(open('weeks.csv'))

result = {}
for row in reader:
    key = row[0]
    if key in result:
        pass
    result[key] = row[1:]
print OrderedDict(sorted(result.items()))
print '\n'
print result