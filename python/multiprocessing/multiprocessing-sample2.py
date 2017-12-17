#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
测试多进程--多进程的非类版本
"""
#多进程部分
import multiprocessing
import time
from multiprocessing import Manager

q_mess = Manager().Queue()#创建列队，不传数字表示列队不限数量,进程间通信用
#函数名：人脸检测识别
#输入：一帧图像
#返回：人脸框face_bbox、以及对应的识别姓名recongnize_name
def Face_detect_and_recongnize(frame):
    time.sleep(0.1)
    face_bbox = [0] * 10
    recongnize_name = ['name'] * len(face_bbox)
    result = list(zip(face_bbox, recongnize_name))
    print 'face'
    q_mess.put({'face': result})

#yolo和deepsort程序合在一起调用
#输入：一帧图像frame
#输出：yolo人形框person_points，deepsort人形框person_bbox
def yolo_and_deepsort(frame):

    time.sleep(0.5)
    print 'yolo'
    yolo_list = ['yolo', 'result']
    q_mess.put({'yolo': yolo_list})

while(1):

    start = time.time()
    #doing something
    pass

    # if ret == False:
    #     break
    #两个进程分别调用人脸检测识别和行人检测
    #创建线程并开
    frame = 0#应该是一帧图片，没用到，暂时代替

    p1 = multiprocessing.Process(target=yolo_and_deepsort,args=(frame,))
    p2 = multiprocessing.Process(target=Face_detect_and_recongnize,args=(frame,))

    p2.start()
    p1.start()

    p1.join()
    p2.join()
    #face_bbox_and_name = Face_detect_and_recongnize(frame)

    result1 = q_mess.get()
    result2 = q_mess.get()
    print result1
    print result2

    end = time.time()
    print "detector time:",end-start

    #doing something
    pass
