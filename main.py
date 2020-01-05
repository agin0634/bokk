import csv
import codecs
import os
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from mainUI import Ui_MainWindow
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

with codecs.open('test-utf8.csv', 'r','utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
