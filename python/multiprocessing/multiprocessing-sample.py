#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
测试多进程--多进程的类版本
说明：python的多线程是假的多线程，实际上效果和单线程没什么区别，有别于C++的多线程。python的多进程才有异步、并真正利用多核CPU
由于main也是一个进程，进程和进程之间，不能共享资源，比如main程序中有一个全局变量，在main中创建了新的进程，其他进程更改不了main中的全局变量（
有教程说多个进程都获得了资源的一份副本，互相之间不干扰）。如果需要进程间传递数据，那就需要进程间通信了
多进程：有尝试过通过multiprocessing.Pool.apply_async、multiprocessing.Pool.map_async来创建进程，但是不知道为什么，要么不是异步的效果，要么
得不到返回值。
多进程通信简单教程：
https://www.cnblogs.com/PrettyTom/p/6583153.html
Python-multiprocessing进程管理
"""

import multiprocessing
import time
from multiprocessing import Manager

q_mess = Manager().Queue()#创建列队，不传数字表示列队不限数量,进程间通信用
#函数名：人脸检测识别
#输入：一帧图像
#返回：人脸框face_bbox、以及对应的识别姓名recongnize_name
#说明：之前之间通过类方法get_result获得结果，但是一直是[]，应该跟多进程有关系，换成进程间通信获取结果了
class Face_detect_and_recongnize(multiprocessing.Process):
    def __init__(self, frame):
        multiprocessing.Process.__init__(self)
        self.frame = frame
        self.result=[]

    def get_result(self):
        return self.result

    def run(self):
        time.sleep(0.1)
        face_bbox = [0] * 10
        recongnize_name = ['name'] * len(face_bbox)
        self.result = list(zip(face_bbox, recongnize_name))
        print 'face'
        q_mess.put({'face': self.result})

#yolo和deepsort程序合在一起调用
#输入：一帧图像frame
#输出：yolo人形框person_points，deepsort人形框person_bbox
class yolo_and_deepsort(multiprocessing.Process):
    def __init__(self, frame):
        multiprocessing.Process.__init__(self)
        self.frame = frame

    def run(self):
        time.sleep(0.5)
        print 'yolo'
        yolo_list = ['yolo', 'result']
        q_mess.put({'yolo': yolo_list})

    def get_result(self):
        return None


while(1):

    start = time.time()
    #doing something
    pass

    # if ret == False:
    #     break
    #两个进程分别调用人脸检测识别和行人检测
    #创建线程并开
    frame = 0#应该是一帧图片，没用到，暂时代替
    p1 = yolo_and_deepsort(frame)
    p2 = Face_detect_and_recongnize(frame)

    p2.start()
    p1.start()

    p1.join()
    p2.join()
    
    #output:
    #face
    #yolo

    result1 = q_mess.get()#获取队列中的一条消息，然后将其从列队中移除，可传参超时时长
    result2 = q_mess.get()
    print result1
    print result2
    #output:
    #{'face': [(0, 'name'), (0, 'name'), (0, 'name'), (0, 'name'), (0, 'name'), (0, 'name'), (0, 'name'),\
    #(0, 'name'), (0, 'name'), (0, 'name')]}
    #{'yolo': ['yolo', 'result']}
    end = time.time()
    print "detector time:",end-start

    #doing something
    pass

