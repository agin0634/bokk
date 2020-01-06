#
#
#
import datetime

#----get all date in data
def getalldate_year(datalist):
    years = []

    for d in datalist:
        date = d['\ufeffDate']
        y = datetime.datetime.strptime(date,'%Y-%m-%d')

        if y.year not in years:
            years.append(y.year)
            print(y.year)
    return years

def getalldate_month(datalist):
    months = []

    for  d in datalist:
        date = d['\ufeffDate']
        m = datetime.datetime.strptime(date,'%Y-%m-%d')

        if m.month not in months:
            months.append(m.month)
            print(m.month)
    return months

#----get all categories in data
def getallCategory(datalist):
    categories = []

    for d in datalist:
        c = d['Category']

        if c not in categories:
            categories.append(c)
            print(c)
    return categories