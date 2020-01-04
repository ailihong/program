# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:51:04 2020

@author: bai
"""
import argparse,time,os
def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--xy','-x',default="105 142 200 200",help='split by space,format x1 y1 x2 y2')
    parser.add_argument('--ms','-m',type=int,default=20)
    parser.add_argument('--interval','-i',type=int,default=500)
    return parser.parse_args()
    
if __name__ == '__main__':
    args = parse_args()
    xy=[int(float(x)) for x in args.xy.split(' ')]
    ms = args.ms
    val = args.interval
    print(xy)
    while 1:
        time.sleep(val/1000)
        os.system("adb shell input swipe {} {} {} {} {}".format(xy[0],xy[1],xy[2],xy[3],ms))
        
