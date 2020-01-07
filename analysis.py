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

def getalldateAmount_month(datalist):
    months = []
    monthsDir = {}

    for  d in datalist:
        date = d.get('\ufeffDate')
        m = datetime.datetime.strptime(date,'%Y-%m-%d')
        # add month key
        ym = str(m.year) + "/" + str(m.month)
        if ym not in months:
            months.append(ym)
            monthsDir.update({ym : 0})
        # add amount value
        ## TODO check income or expenses
        a = int(d.get('Amount').replace('-',''))
        total = int(monthsDir.get(ym)) + a
        monthsDir.update({ym : total})

    for (key, value) in monthsDir.items():
        print(key," ::", value)

    return monthsDir

#----get all categories' amount  in data
def getallCategoryAmount(datalist):
    categories = []
    categoriesDir = {}

    for d in datalist:
        c = d.get('Category')
        # add category key
        if c not in categories:
            categories.append(c)
            categoriesDir.update({c : 0})
        # add amount value
        ## TODO check income or expenses
        a = int(d.get('Amount').replace('-',''))
        total = int(categoriesDir.get(c)) + a
        categoriesDir.update({c : total})
     
    for (key, value) in categoriesDir.items():
        print(key," ::", value)
    
    return categoriesDir
