#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:26:35 2017
pycaffe multiprocessin 错误：子进程只能在该进程中进行相关资源的使用，初始化
Caffe fails to use GPU in a new thread #4178 https://github.com/BVLC/caffe/issues/4178
"""
import numpy as np
import facep
import cv2
#多线程部分
import multiprocessing
import time
from multiprocessing import Queue
#创建列队，不传数字表示列队不限数量,进程间通信用
q_frame_main2face_detect = Queue()#传递图片,主进程传给人脸检测
q_frame_face_detect2face_recognize = Queue()#传递图片,人脸检测进程传给人脸识别
q_face_bbox= Queue()#传递检测到的脸部坐标
q_person_name= Queue()#传递检测到的人脸姓名

videoCapture = cv2.VideoCapture("./video/12105.mp4")
#videoCapture = cv2.VideoCapture(1)

##人脸检测识别部分
#face = facep.Face()
#face.init('faceData.db', 1280, 720, 0.5)
font = cv2.FONT_HERSHEY_SIMPLEX
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#opencv 人脸检测
def face_opencv_detect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_bbox = []
    for i in range(len(faces)):
        ix,iy,w,h = int(faces[i][0]),int(faces[i][1]),int(faces[i][2]),int(faces[i][3])
#        cv2.rectangle(frame,(ix,iy),(ix+w,iy+h),(0,0,255),2)
        face_bbox.append([ix,iy,ix+w,iy+h])
    return face_bbox

#函数名：人脸检测识别
#输入：通过一帧图像
#返回：人脸框、以及对应的识别姓名
class Face_recongnize(multiprocessing.Process):
    
    def __init__(self):
        multiprocessing.Process.__init__(self)
        #人脸检测识别部分,该初始化会在主进程中执行,子进程相关的资源只能完全在子进程中实现
#        self.face = facep.Face()
#        self.face.init('faceData.db', 1280, 720, 0.5)

    def run(self):
        self.face = facep.Face()
        self.face.init('faceData.db', 1280, 720, 0.5)
        while(1):
               if not q_face_bbox.empty():#非空
                   face_bbox = q_face_bbox.get()
                   frame = q_frame_face_detect2face_recognize.get()
                   recongnize_name_list=[]
                   #依次识别多个人脸
                   for j in range(len(face_bbox)):
                       fx1 = face_bbox[j][0]
                       fy1 = face_bbox[j][1]
                       fx2 = face_bbox[j][2]
                       fy2 = face_bbox[j][3]
                       # 虹软的人脸识别
                       face_name = self.face.recognize(frame, fx1, fy1, fx2 - fx1, fy2 - fy1)  # 进行识别
                       recongnize_name_list.append(face_name)
                       q_person_name.put(recongnize_name_list)
               else:
                   time.sleep(0.02)

#函数名：人脸检测
#输入：通过queue输入一帧图像
#返回：通过queue输出人脸框坐标,对应frame
def Face_detect():
    while True:
        if not q_frame_main2face_detect.empty():#非空
            frame = q_frame_main2face_detect.get()#get()后,大小减1
            # 使用opencv的人脸检测
            face_bbox = face_opencv_detect(frame)
            if(len(face_bbox)>0):
                q_frame_face_detect2face_recognize.put(frame)
                q_face_bbox.put(face_bbox)
                print 'detected'
            else:
                print 'not detected'
        else:
            time.sleep(0.02)#空,sleep 20ms
import ft2
ft = ft2.put_chinese_text('simhei.ttf')
id_more =[]
count = 0
#创建进程
p1 = multiprocessing.Process(target=Face_detect)
p2 = Face_recongnize()
p1.daemon=True#设置为守护进程,主进程结束,子进程强制结束
p2.daemon=True

p2.start()#开始
p1.start()
    
while(1):
    start = time.time()
    ret,frame = videoCapture.read()
    
    if ret == False:
        break
    #输入queue图片
    q_frame_main2face_detect.put(frame)
    
    time.sleep(0.02)
    
    if not q_person_name.empty():
        name_list = q_person_name.get()
        print 'name:',name_list
    
    end = time.time()
    print "main thread use time:",end-start
          
    cv2.imshow("Image", frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
