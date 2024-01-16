# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:12:58 2020

@author: jeffc
"""


import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from click import Ui_MainWindow, choosevideo, choosetarget
import cv2

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