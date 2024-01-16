# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './click.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QProgressBar, QDialog, QLabel, QApplication, QWidget, QVBoxLayout, QListView, QTableWidget, QHBoxLayout, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel,QThread
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import func
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import sys
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
import re
import cv2
import time

vpath = r'D:/yolov3/source'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 618)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        layout = QHBoxLayout()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 350, 191, 81))        
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 450, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.b1_click)
        self.pushButton_2.clicked.connect(self.b2_click)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "車輛偵測"))
        self.pushButton.setText(_translate("MainWindow", "輸入影片"))
        self.pushButton_2.setText(_translate("MainWindow", "選擇影片"))
        self.widget = list()
    def b1_click(self):
        
        func.main()
        
    def b2_click(self):
        widget = choosevideo(self)
        self.widget.append(widget)
        widget.show()
        

class choosevideo(QWidget):
    def __init__(self,QWidget):
        super().__init__()
        self.setupUi(self)
    def setupUi(self,parent=None):
        self.setWindowTitle("選擇影片")
        self.resize(300,270)
        print (self)
        layout=QVBoxLayout()       
        listView= QListView()
        slm=QStringListModel();
        files=next(os.walk(vpath))
        self.qlist=files[2]
        slm.setStringList(self.qlist)
        listView.setModel(slm)
        listView.clicked.connect(self.listview_click)
        # listView.clicked.connect(choosetarget.setupUi)
        layout.addWidget(listView)
        self.setLayout(layout)
        self.widget = list()
    def listview_click(self,qModelIndex):
        self.deleteLater()
        global dirs
        dirs=[]
        for file in os.listdir("./result/cropcar"):
            if file.startswith(str.lower(self.qlist[qModelIndex.row()][:-4])):
                dirs.append(file)
        Target_Widget=choosetarget(self)
        self.widget.append(Target_Widget)
        Target_Widget.show()
        # Target_Widget.exec_()
        
class choosetarget(QWidget):    
    def __init__(self,QWidget):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        self.setWindowTitle("選擇秒數")
        self.resize(300,270)
        layout=QVBoxLayout()       
        listView= QListView()
        slm=QStringListModel();
        print(dirs)
        self.qlist=dirs
        slm.setStringList(self.qlist)
        listView.setModel(slm)
        listView.clicked.connect(self.listview_click)
        layout.addWidget(listView)
        self.setLayout(layout)
        self.widget=list()
    def listview_click(self, qModelIndex):
        global target_dir
        target_dir=self.qlist[qModelIndex.row()]
        self.deleteLater()
        Target_Table=targettable(self)
        self.widget.append(Target_Table)
        Target_Table.show()

class targettable(QWidget):
    def __init__(self,QWidget):
        super().__init__()
        self.initUi()
        
    def initUi(self):
        DIR='./result/cropcar/'
        files_num=len([name for name in os.listdir(DIR + target_dir) if os.path.isfile(os.path.join(DIR + target_dir, name))])
        print(files_num)
        self.setWindowTitle("選擇目標車輛")
        self.resize(1550,1000)
        conLayout = QHBoxLayout()
        
        table=QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(files_num//5+1)
        
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setIconSize(QSize(300,200));
        
        for i in range(5):
            table.setColumnWidth(i, 300)
        for j in range(files_num//5+1):
            table.setRowHeight(j, 200) 
            
        for k in range(files_num):
            i=k/5
            j=k%5
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)
            icon=QIcon(DIR+'_all/' + target_dir +'_%d.jpg'%k)
            item.setIcon(QIcon(icon))
            item.text=DIR+'_all/' + target_dir +'_%d.jpg'%k
            
            table.setItem(i,j,item)
        conLayout.addWidget(table)
        self.setLayout(conLayout)
        table.itemClicked.connect(self.sort)
        self.widget=list()
        
    def sort(self, item):
        self.deleteLater()


        text=item.text
        x_test=[image.img_to_array(image.load_img(text,target_size=(299,299)))]
        
        global y_test
        y_test=[text]
        imgDB_size=0
        for file in os.listdir('./result/cropcar/_all'):
            img_path='./result/cropcar/_all/'+file
            print(img_path)
            img=image.load_img(img_path,target_size=(299,299))
            x=image.img_to_array(img)
            x=np.expand_dims(x,axis=0)
            if img_path != text:
                x_test=np.concatenate((x_test,x))
                y_test.append(img_path)
            imgDB_size += 1
                    
        x_test=preprocess_input(x_test)
        model=InceptionResNetV2(weights='imagenet',include_top=False)
        features=model.predict(x_test)
        features = np.array(features)
        print(features.shape)
        features_db=features.reshape(imgDB_size,8*8*1536)
        print(features_db.shape)
        fea = []
        for i in range(imgDB_size):
            fe = sum(abs(features_db[i, :] - features_db[0, :]))
            find = list(np.where(fea == fe))
            flag = 0
            for j in fea:
                if j == fe:
                    flag = 1
            if flag == 0:
                fea.append(fe)
            else:
                fea.append(10000)
            print(fe)
        print(fea)
        global result_index
        result_index = np.argsort(fea)
        print(result_index)

        Result_Table=resulttable(self)
        self.widget.append(Result_Table)
        Result_Table.show()
        self.deleteLater()
class resulttable(QWidget):
    def __init__(self,QWidget):
        super().__init__()
        self.initUi()
        
    def initUi(self):

        self.setWindowTitle("選擇目標車輛")
        self.resize(1550,400)
        conLayout = QHBoxLayout()
        
        table=QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(2)
        
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setIconSize(QSize(300,200));
        
        for i in range(5):
            table.setColumnWidth(i, 300)
        for j in range(2):
            table.setRowHeight(j, 200) 
            
        for k in range(10):
            i=k/5
            j=k%5
            item = QTableWidgetItem(y_test[result_index[k]])
            item.setFlags(Qt.ItemIsEnabled)
            icon=QIcon(y_test[result_index[k]])
            item.setIcon(QIcon(icon))
            item.text=y_test[result_index[k]]
            table.setItem(i,j,item)
        conLayout.addWidget(table)
        self.setLayout(conLayout)
        table.itemClicked.connect(self.showvideo)
        self.widget=list()
    def showvideo(self, item):
        text=item.text
        index=[m.start() for m in re.finditer('/', text)]
        text=text[index[-1]+1:]
        index=[m.start() for m in re.finditer('_', text)]
        minutes=int(text[index[-3]+1:index[-2]])*60
        seconds=minutes+int(text[index[-2]+1:index[-1]])-5
        if seconds<0:
            seconds=0
        video_name=text[:index[-3]]
        
        
        for file in os.listdir("./source"):
            if file.startswith(video_name+'.'):
                
                fpath='./source/'+os.path.normcase(os.path.normpath(file))   
                print(fpath)
                vc = cv2.VideoCapture(fpath) #讀影片
                   
                if vc.isOpened(): #判斷是否正常打開影片
                    rval , frame = vc.read()                    
                else:
                    rval = False
            
                fps=round(vc.get(cv2.CAP_PROP_FPS))
                timeF = seconds*fps #影片禎數間隔頻率
                vc.set(cv2.CAP_PROP_POS_FRAMES, timeF)
                while(vc.isOpened()):
                    ret, frame = vc.read()
                    time.sleep(1/fps) 
                    cv2.imshow(os.path.normcase(os.path.normpath(file))  ,frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                vc.release()
                cv2.destroyAllWindows()
                
        
    

        
        