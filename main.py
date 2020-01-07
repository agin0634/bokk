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
    def __init__(self, parent=None, width=6, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  

        FigureCanvas.__init__(self, fig) 
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def chart_bar(self,labellist,sizelist):
        x = labellist
        y = sizelist
        width = 0.5
        self.axes.bar(x,y,width,align="center")
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(x)
    
    def chart_pie(self,labellist,sizelist):
        labels = labellist
        sizes = sizelist
        self.axes.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90)
        self.axes.axis('equal')
    

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
            self.drawChart()
    
    def drawChart(self):
        # tab 1
        dir = an.getalldateAmount_month(App.Data)
        labellist = []
        sizelist = []
        for key, value in dir.items():
            labellist.append(key)
            sizelist.append(value)

        dr = Figure_Canvas()
        dr.chart_pie(labellist, sizelist) 
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.ui.graphicsView_tab1.setScene(graphicscene)
        self.ui.graphicsView_tab1.show()
        
        # tab 2
        dir = an.getalldateAmount_month(App.Data)
        labellist = []
        sizelist = []
        for key, value in dir.items():
            labellist.append(key)
            sizelist.append(value)

        dr2 = Figure_Canvas()
        dr2.chart_bar(labellist, sizelist)
        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr2)
        self.ui.graphicsView_tab2.setScene(graphicscene2)
        self.ui.graphicsView_tab2.show()


       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
