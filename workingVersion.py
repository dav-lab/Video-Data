import json
import uncertainties


data=json.load(open('finalData.json'))
count={}

for i in data['B03dhB-YmMM']['segments']:
    start=i[0]
    end=i[1]
    if (start,end) not in count:
        count[(start,end)]=1
    else:
        count[(start,end)]+=1