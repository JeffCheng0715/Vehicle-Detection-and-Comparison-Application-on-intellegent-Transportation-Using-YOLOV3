# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'click.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QProgressBar, QDialog, QLabel, QApplication, QWidget, QVBoxLayout, QListView, QTableWidget, QHBoxLayout, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel,QThread
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        layout = QHBoxLayout()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(50, 30, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        layout.addWidget(self.pushButton,0,Qt.AlignRight)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 140, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        
        # layout.addWidget(QPushButton(str(1)))
        
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(380, 40, 371, 421))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(50, 270, 256, 192))
        self.listView.setObjectName("listView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # self.pushButton.clicked.connect(MainWindow.slot1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "車輛偵測"))
        self.pushButton.setText(_translate("MainWindow", "輸入影片"))
        self.pushButton_2.setText(_translate("MainWindow", "選擇影片"))

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)    
if __name__ == '__main__':
    
    app=QApplication(sys.argv)    
    mainWindows = MyMainWindow()
    palette = QPalette()
    palette.setBrush(QPalette().Background, QBrush(QPixmap('./background.jpg')))
    mainWindows.setPalette(palette)
    mainWindows.show()

    sys.exit(app.exec_())

