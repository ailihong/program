#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 20:08:23 2019

@author: bai
"""
import os
import numpy as np
import cv2
import fcntl
#communicate with another process through named pipe
#one for receive command, the other for send command
rfPath = "/tmp/com_p1"
wfPath = "/tmp/com_p2"
bufferSize = 480*640*3

if __name__ == '__main__':
    print('server running')
    try:
        if os.path.exists(rfPath):
            os.system('rm -r {}'.format(rfPath))
        if os.path.exists(wfPath):
            os.system('rm -r {}'.format(wfPath))

        os.mkfifo(wfPath)
        os.mkfifo(rfPath)
    except OSError:
        print(OSError)
        pass
    
    rp = os.open(rfPath, os.O_RDONLY)
    wp = os.open(wfPath, os.O_RDWR)
    
    fcntl.F_SETPIPE_SZ = 1031
    fcntl.fcntl(wp, fcntl.F_SETPIPE_SZ, bufferSize)
    
    img_buf=np.zeros((480,640,3),dtype=np.int8)
#    ss = img_buf.tostring()
#    img_buf2 = np.fromstring(ss,dtype=np.int).reshape((24,480,640,3))
#    
#    print(img_buf.shape,img_buf2.shape)
    state=0
    num_images=12
    while 1:
        if state==0:
#            time.sleep(0.1)
            state=1#some condition
        elif state==1:#send num of images in 1 byte
            os.write(wp,'{}'.format(num_images).encode('utf-8'))
            print('send nums')
            state=2
        elif state==2:#receive ack
            response = os.read(rp,1024)
            response = response.decode('utf-8')
            if response == '1':#receive ack with num of images
                print('got ack')
                state=3
        elif state == 3:#send images
            for i in range(num_images):
                img=cv2.imread('temp.jpg')
                img_buf = cv2.resize(img,(640,480))
                os.write(wp,img_buf.tostring())
            state=4
            print('send images finished')
        elif state == 4:#receive results or resend
            response = os.read(rp,1024)
            if len(response) == 1:
                response = response.decode('utf-8')
                if response == '2':#resend if failed to receive images
                    print('got resend cmd')
                    state=3
            else:
#                print('receive the algorithm results:',response)
                state=0
        
    os.close(rp)    
    os.close(wp)
