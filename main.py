import csv
import codecs
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
        with codecs.open(file, 'r','utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reversed(list(reader)):
                #print(row)
                self.Data.append(row)


class Figure_Canvas(FigureCanvas):  
    def __init__(self, parent=None, width=7, height=4, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=100)  
        fig = plt.figure(figsize=(width, height), dpi=100)
        plt.style.use('seaborn-whitegrid')

        FigureCanvas.__init__(self, fig) 
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def chart_bar(self,labellist,sizelist,title):
        x = labellist
        y = sizelist
        width = 0.5
        self.axes.bar(x,y,width,align="center")
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(x)
        self.axes.set_title(title)
    
    def chart_pie(self,labellist,sizelist,title):
        labels = labellist
        sizes = sizelist

        self.axes.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90)
        self.axes.axis('equal')
        self.axes.set_title(title)
        self.axes.legend(title="Months",loc="center left",bbox_to_anchor=(0.9,0.5))

    def chart_donut(self,labellist,sizelist,title):
        labels = labellist
        sizes = sizelist
        
        wedges = self.axes.pie(sizes, wedgeprops=dict(width=0.5),startangle=90)
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
            self.axes.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

        self.axes.set_title(title,y=0.425)

    def chart_plot(self,labellist,sizelist,title):
        self.axes.plot(labellist,sizelist)
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
        
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr_ovDate1)
        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr_ovDate2)
        graphicscene3 = QtWidgets.QGraphicsScene()
        graphicscene3.addWidget(dr_ovDate2)
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
        for key, value in dir.items():
            labellist.append(key)
            sizelist.append(value)

        dr2 = Figure_Canvas()
        dr2.chart_donut(labellist,sizelist,'Total\n84584')
        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr2)
        self.ui.graphicsView_ovCate1.setScene(graphicscene2)
        self.ui.graphicsView_ovCate1.show()


       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
