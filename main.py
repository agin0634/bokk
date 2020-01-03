import csv
import codecs

with codecs.open('test-utf8.csv', 'r','utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
