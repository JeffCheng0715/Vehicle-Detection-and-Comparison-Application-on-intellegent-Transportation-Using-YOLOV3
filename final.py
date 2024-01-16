# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QPushButton,QProgressBar, QDialog, QLabel, QApplication, QWidget, QVBoxLayout, QListView, QTableWidget, QHBoxLayout, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel,QThread
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.models import Model,load_model
import numpy as np
import sys
import os
import func
import re
import cv2
import time
import detect
from PIL import Image
import shutil
import threading

vpath = r'D:/yolov3/source'
cps= 5
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 618)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAutoFillBackground(False)
        pixmap=QtGui.QPixmap("yzu.png")
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont('微軟正黑體')
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont('微軟正黑體')
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem3)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setObjectName("listView")
        self.verticalLayout_3.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        palette = QPalette()
        myPixmap = QtGui.QPixmap('./background.jpg')
        myScaledPixmap = myPixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation)
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(myScaledPixmap))
        self.setPalette(palette)
        
        self.pushButton.clicked.connect(self.b1_click)
        self.pushButton_2.clicked.connect(self.b2_click)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "車輛偵測"))
        self.pushButton.setText(_translate("MainWindow", "輸入影片"))
        self.pushButton_2.setText(_translate("MainWindow", "選擇車輛"))
        
    def b1_click(self):
        
        self.crop_video()
        QMessageBox.about(self,"提示","影片輸入成功")
    
    def crop_video(self) :

        for file in os.listdir(vpath):
            if file.endswith((".mp4" , ".avi")):
                fpath = vpath +'\\'+ os.path.normcase(os.path.normpath(file))
                # cps=5 #設定幾秒取一張
                
                vc = cv2.VideoCapture(fpath) #讀影片
                
                fname = os.path.splitext(os.path.basename(fpath))[0] #影片名稱
                dirpath = os.path.splitext(os.path.normpath(fpath))[0]
                if not os.path.isdir(dirpath): #建立以影片名稱命名的資料夾
                    os.mkdir(dirpath)
                
                if vc.isOpened(): #判斷是否正常打開影片
                    rval , frame = vc.read()
                    cv2.imwrite(os.path.join(dirpath,'{a}_00_00.jpg'.format(a = fname)), frame)
                else:
                    rval = False
                c=1
                i=1
                fps=round(vc.get(cv2.CAP_PROP_FPS))
                timeF = cps*fps #影片禎數間隔頻率
                 
                while rval:   #循環讀取影片禎數
                    rval , frame = vc.read()
                    if(c%timeF == 0): #每隔timeF儲存        
                        time = i * cps
                        seconds = time % 60
                        if seconds < 10:
                            seconds = '0' + str(seconds)
                        else:
                            seconds = str(seconds)
                        minutes = time // 60
                        if minutes == 0:
                            minutes = '00'
                        elif minutes < 10:
                            minute = '0' + str(minutes)
                        else:
                            minutes = str(minutes)
                        # cv2.imwrite(os.path.join(dirpath,'{}.jpg'.format(str(c))), frame)        
                        cv2.imwrite(os.path.join(dirpath,'{a}_{b}_{c}.jpg'.format(a = fname, b = minutes, c = seconds)), frame) #儲存影像
                        print ('{a}_{b}_{c}.jpg saved at '.format(a = fname, b = minutes, c = seconds) + dirpath)
                        i = i + 1
                    c = c + 1
                    if c == 500:
                         break
                vc.release()
        self.detect_crop_video()
    def detect_crop_video(self):
        
        par=True
        output_path=detect.main(par, vpath)
        
        self.cropcar(output_path)
    
    def cropcar(self,output_path):
        
        cropdir=output_path + 'cropcar'
        os.mkdir(cropdir)
        os.mkdir(cropdir + '/_all')
        for root, dirs, files in os.walk(output_path):
            for name in dirs:
                folddir = os.path.join(root, name)           
                for file in os.listdir(folddir):
                    c=0
                    if file.endswith(".txt"):
                        dirname=file[:-4]
                        os.mkdir(cropdir + '/' + dirname)
                        with open(folddir + '/' + file) as f:
                            for line in f:
                                a = line.split()
                                im = Image.open('{}'.format(a[0]))
                                crop=im.crop((int(a[1]), int(a[2]), int(a[3]), int(a[4])))                            
                                crop=crop.resize((300,200))
                                crop.save(cropdir + '/' + dirname + '/' + os.path.basename(f.name)[:-4] + '_{}.jpg'.format(str(c)))
                                print(cropdir + '/' + dirname + '/' + os.path.basename(f.name)[:-4] + '_{}.jpg'.format(str(c)))
                                crop.save(cropdir + '/_all/' + os.path.basename(f.name)[:-4] + '_{}.jpg'.format(str(c)))
                                c=c+1
        
    def b2_click(self):
        slm=QStringListModel();
        files=next(os.walk(vpath))
        self.qlist=files[2]
        slm.setStringList(self.qlist)
        self.listView.setModel(slm)
        self.listView.clicked.connect(self.choosevideo_click)
        
    def choosevideo_click(self,qModelIndex):
        dirs=[]
        for file in os.listdir("./result/cropcar"):
            if file.startswith(str.lower(self.qlist[qModelIndex.row()][:-4])):
                dirs.append(file)
        
        slm=QStringListModel();
        print(dirs)
        self.qlist=dirs
        slm.setStringList(self.qlist)
        self.listView.setModel(slm)
        self.listView.clicked.connect(self.choosetarget_click)

    def choosetarget_click(self, qModelIndex):
        global target_dir
        target_dir=self.qlist[qModelIndex.row()]   
        self.Target_Table=targettable()
        self.Target_Table.show()
        
class targettable(QWidget):
    def __init__(self):
        super(targettable,self).__init__()
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
            print(DIR+'_all/' + target_dir +'_%d.jpg'%k)
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)
            icon=QIcon(DIR+'_all/' + target_dir +'_%d.jpg'%k)
            item.setIcon(QIcon(icon))
            item.text=DIR+'_all/' + target_dir +'_%d.jpg'%k
            
            table.setItem(i,j,item)
        table.itemClicked.connect(self.sort)
        self.setLayout(conLayout)
        conLayout.addWidget(table)
        self.widget=list()
        
    def cosine_similarity(self,ratings):
        sim = ratings.dot(ratings.T)
        if not isinstance(sim, np.ndarray):
            sim = sim.toarray()
        norms = np.array([np.sqrt(np.diagonal(sim))])
        return (sim / norms / norms.T)
    
    def sort(self, item):
        self.deleteLater()

        text=item.text
        # x_test=[image.img_to_array(image.load_img(text,target_size=(316,316)))]
        x_test=[image.img_to_array(image.load_img(text,target_size=(299,299)))]
        
        global y_test
        y_test=[text]
        imgDB_size=0
        for file in os.listdir('./result/cropcar/_all'):
            img_path='./result/cropcar/_all/'+file
            print(img_path)
            # img=image.load_img(img_path,target_size=(316,316))
            img=image.load_img(img_path,target_size=(299,299))
            x=image.img_to_array(img)
            x=np.expand_dims(x,axis=0)
            if img_path != text:
                x_test=np.concatenate((x_test,x))
                y_test.append(img_path)
            imgDB_size += 1
                    
        x_test=preprocess_input(x_test)
        # model = load_model('convAE_encoder.h5')
        model=InceptionResNetV2(weights='imagenet',include_top=False)
        features=model.predict(x_test)
        features = np.array(features)
        print(features.shape)
        # features_db=features.reshape(imgDB_size,40*40*8)
        features_db=features.reshape(imgDB_size,8*8*1536)
        print(features_db.shape)
        fea = []
        # sim = self.cosine_similarity(features_db)
        # print(sim[0])
        # global result_index
        # result_index = np.argsort(-sim[0])
        # print(result_index)
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
       
             

class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        
if __name__ == '__main__':
    
    app=QApplication(sys.argv)    
    mainWindows = MyMainWindow()
    mainWindows.show()

    sys.exit(app.exec_())
        

