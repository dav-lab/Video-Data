import csv
import natsort

reader = csv.reader(open('/Users/emustafa-local/Video-Data/videoTranscripts/weeks.csv'))

result = {}
for row in reader:
    key = row[0]
    if key in result:
        pass
    result[key] = row[1:]

sorted_result = natsort.natsorted(result.items(), key=lambda y: y)

print sorted_result