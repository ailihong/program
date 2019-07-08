#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 19:59:08 2019

@author: bai
"""
import os
import numpy as np
import time,cv2
#communicate with another process through named pipe
#one for receive command, the other for send command
wfPath = "/tmp/com_p1"
rfPath = "/tmp/com_p2"
bufferSize = 480*640*3#921600

if __name__ == '__main__':
    print('client running')
    wp = os.open(wfPath, os.O_RDWR)
    rp = os.open(rfPath, os.O_RDONLY)
#    img_buf=np.zeros((480,640,3),dtype=np.int8)
    
    state=0
    num_images=0
    cnt=0
    
    while 1:
        now = time.time()
        if state==0:#read nums
            ret = os.read(rp,bufferSize)
            if len(ret) != 0:
                num_images = int(ret)
                print('num_images:',num_images)
                state=1      
        elif state==1:#send ack
            os.write(wp,"1".encode('utf-8'))
            print('send ack')
            state=2
        elif state==2:#receive the images
            ret = os.read(rp,bufferSize)
            if len(ret) != 0:
                if len(ret) == bufferSize:#
                    a = np.fromstring(ret,dtype=np.uint8).reshape((480,640,3))
                    cv2.imshow('img{}'.format(cnt),a)
                    cv2.waitKey(50)
                    cnt+=1
                    print('got a image')
                    if cnt == num_images:
                        print('receive image finished')
                        print('cost time:',time.time() - now)#0.0006239414215087891
                        state=3
                        cnt=0
                else:
                    if len(ret) < bufferSize:
                        print('unknown received info:',ret)
                    os.write(wp,"2".encode('utf-8'))
                    cnt=0
        
        elif state == 3:#send_result
            info='10'*num_images
            os.write(wp,info.encode('utf-8'))
            state=0
            print('send results')
            
#        time.sleep(0.1)

    os.close(wp)
    os.close(rp)


