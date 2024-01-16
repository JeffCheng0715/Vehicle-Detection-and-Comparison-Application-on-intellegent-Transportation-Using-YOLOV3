import detect
import cv2
import os
import time
import numpy as np
import numpy as np
from PIL import Image
import shutil

vpath = r'D:/yolov3/source'#放影片的檔案夾位置

def crop_video(vpath) :

    for file in os.listdir(vpath):
        if file.endswith((".mp4" , ".avi")):
            fpath = vpath +'\\'+ os.path.normcase(os.path.normpath(file))
            cps=5 #設定幾秒取一張
            
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
                if c == 1000:
                     break
            vc.release()
def detect_crop_video(vpath):
    
    par=True
    output_path=detect.main(par, vpath)
    
    return output_path

def cropcar(output_path):
    
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
def main():
    crop_video(vpath)
    a=detect_crop_video(vpath)
    cropcar('result/')
    

if __name__ == '__main__':
    main()
    