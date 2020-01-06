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

class App():
    def read_Csv(self,file):
        Data = []
        with codecs.open(file, 'r','utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reversed(list(reader)):
                Data.append(row)

            an.getalldate_month(Data)

class Figure_Canvas(FigureCanvas):  
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  

        FigureCanvas.__init__(self, fig) 
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def test(self):
        #x = ['第1周','第2周',3,4,5,6,7,8,9]
        x = ['聊天', '支付', '团购', '在线视频']
        idx = np.arange(len(x))
        y=[23,21,32,130]
        width = 0.5
        #y = [23,21,32,13,3,132,13,3,1]
        self.axes.bar([0,1,2,3],y,width,align="center")
        self.axes.set_xticks([0,1,2,3])
        self.axes.set_xticklabels(x)

    
    def test2(self):
        labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
        sizes = [15, 30, 45, 10]
        #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        
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
        dr = Figure_Canvas()
        dr.test()  
        
        dr2 = Figure_Canvas()
        dr2.test2()
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        
        self.ui.graphicsView_tab1.setScene(graphicscene)
        self.ui.graphicsView_tab1.show()

        graphicscene2 = QtWidgets.QGraphicsScene()
        graphicscene2.addWidget(dr2)
        
        self.ui.graphicsView_tab2.setScene(graphicscene2)
        self.ui.graphicsView_tab2.show()


       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
