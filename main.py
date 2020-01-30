import csv
import codecs
import random
import numpy as np
import analysis as an
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from mainUI import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
#myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

class App():
    Data = []

    def read_Csv(self,file):
        with codecs.open(file, 'r','utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reversed(list(reader)):
                #print(row)
                self.Data.append(row)


class Figure_Canvas(FigureCanvas):  
    cmap = plt.get_cmap('Spectral')
    #colors = [cmap(i) for i in np.linspace(0, 1, 8)]
    
    color = ['#2964BA', '#F0FFBD', '#F2C029', '#6ECC7B', '#FF8335', '#3FC211',
    '#6E94CC', '#FFADA2', '#B82240', '#C0A3FF', '#88F3FE', '#FF8AC4', '#A53CC2']
    
    def __init__(self, parent=None, width=8.5, height=5, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=100)  
        fig = plt.figure(figsize=(width, height), dpi=100)
        plt.style.use('seaborn-whitegrid')

        FigureCanvas.__init__(self, fig) 
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def func(self,pct,sizelist):
        absolute = int(pct/100.*np.sum(sizelist))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    def chart_bar(self,labellist,sizelist,title):
        x = labellist
        y = sizelist
        width = 0.5
        self.axes.bar(x,y,width,align="center")
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(x ,rotation=60)
        self.axes.set_title(title)
    
    def chart_pie(self,labellist,sizelist,title):
        labels = labellist
        sizes = sizelist

        self.axes.pie(sizes, labels=labels, autopct=lambda pct: self.func(pct,sizes),shadow=False, startangle=90, pctdistance=0.75, colors = self.color)
        self.axes.axis('equal')
        self.axes.set_title(title)
        self.axes.legend(title="Months",loc="center left",bbox_to_anchor=(0.9,0.5))

    def chart_donut(self,labellist,sizelist,title):
        labels = labellist
        sizes = sizelist
        
        wedges = self.axes.pie(sizes, wedgeprops=dict(width=0.5), autopct='%1.1f%%', startangle=180, pctdistance=0.8, colors = self.color)
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

        for i,p in enumerate(wedges[0]):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            self.axes.annotate("{label} ({size})".format(label=labels[i],size=sizes[i]), xy=(x, y), xytext=(1.4*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

        self.axes.set_title(title,y=0.425)

    def chart_plot(self,labellist,sizelist,title):
        self.axes.plot(labellist,sizelist)
        
        total = 0
        for s in sizelist:
            total += s

        avg = total / len(sizelist)
        avglist = []
        for i in range(len(sizelist)):
            avglist.append(avg)

        avglegend = 'avg: ' + str(int(avglist[0]))

        self.axes.plot(labellist,sizelist)
        self.axes.plot(labellist,avglist,label=avglegend,linestyle='--')

        x = labellist
        y = sizelist
        width = 0.2
        self.axes.legend(loc='upper right', borderaxespad=2)
        self.axes.bar(x,y,width,align="center")
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(x, rotation=60)
        for i, val in enumerate(sizelist):
            self.axes.text(i,val, val, horizontalalignment='center',verticalalignment='bottom', fontdict={'fontweight':500, 'size':8})

        self.axes.set_title(title)

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

    def eventBrowseData(self):
        data = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',os.getcwd(),"All Files(*csv *xls)")
        if data:
            self.ui.pathlineEdit.setText(data[0])
            App.read_Csv(App,data[0])
            self.drawChart_ovDate()
            self.drawChart_ovCate()
            self.addTable_list()
    
    def drawChart_ovDate(self):
        dir = an.getalldateAmount_month(App.Data)
        labellist = []
        sizelist = []
        for key, value in dir.items():
            labellist.append(key)
            sizelist.append(value)

        dr_ovDate1 = Figure_Canvas()
        dr_ovDate1.chart_pie(labellist, sizelist,'hi\n')
        dr_ovDate2 = Figure_Canvas()
        dr_ovDate2.chart_plot(labellist,sizelist,'ff\n')
        dr_ovDate3 = Figure_Canvas()
        dr_ovDate3.chart_bar(labellist,sizelist,'ff\n')
        
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr_ovDate1)
        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr_ovDate2)
        graphicscene3 = QtWidgets.QGraphicsScene()
        graphicscene3.addWidget(dr_ovDate3)
        self.ui.graphicsView_ovDate1.setScene(graphicscene)
        self.ui.graphicsView_ovDate1.show()
        self.ui.graphicsView_ovDate2.setScene(graphicscene2)
        self.ui.graphicsView_ovDate2.show()
        self.ui.graphicsView_ovDate3.setScene(graphicscene3)
        self.ui.graphicsView_ovDate3.show()
        
    def drawChart_ovCate(self):
        # tab 2
        dir = an.getallCategoryAmount(App.Data)
        labellist = []
        sizelist = []
        labellist_sa = []
        sizelist_sa = []
        total = 0
        total_sa = 0

        for v in dir.values():
            total += v

        for key, value in dir.items():
            if value < total *0.019:
                labellist_sa.append(key)
                sizelist_sa.append(value)
                total_sa += value
            else:
                labellist.append(key)
                sizelist.append(value)

        if total_sa > 0:
            labellist.append('Small Amounts')
            sizelist.append(total_sa)

        title_total = 'Total\n%i'%(total)
        title_sa = 'Small Amounts\n%i'%(total_sa)
        dr_ovCate1 = Figure_Canvas()
        dr_ovCate1.chart_donut(labellist,sizelist,title_total)
        dr_ovCate2 = Figure_Canvas()
        dr_ovCate2.chart_donut(labellist_sa,sizelist_sa,title_sa)

        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr_ovCate1)
        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr_ovCate2)
        self.ui.graphicsView_ovCate1.setScene(graphicscene)
        self.ui.graphicsView_ovCate1.show()
        self.ui.graphicsView_ovCate2.setScene(graphicscene2)
        self.ui.graphicsView_ovCate2.show()

    def addTable_list(self):
        # tab 3
        Data_keys = list(App.Data[0].keys())
        
        # columns
        self.ui.tableWidget_list.setColumnCount(len(Data_keys))
        self.ui.tableWidget_list.setHorizontalHeaderLabels(Data_keys)

        # rows
        self.ui.tableWidget_list.setRowCount(len(App.Data)-1)

        for x in range(self.ui.tableWidget_list.rowCount()):
            if x == 0:
                pass
            dir = App.Data[x]
            for y in range(self.ui.tableWidget_list.columnCount()):
                key = Data_keys[y]
                c = dir.get(key)
                self.ui.tableWidget_list.setItem(x,y,QtWidgets.QTableWidgetItem(c))
        
        self.ui.tableWidget_list.resizeColumnsToContents()
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
