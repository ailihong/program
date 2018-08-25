#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#将没有统一命名的图片和标注文件进行修改
import os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    
    parser.add_argument('--image','-i', dest='image_path', help='xml path to read',
                        default='None')
    parser.add_argument('--xml','-x', dest='xml_path', help='xml path to read',
                        default='None')
    parser.add_argument('--prefix','-p', dest='prefix', help='prefix_nn.xx',
                        default='None')
    args = parser.parse_args()

    return args
args = parse_args()
if args.image_path == 'None' or args.xml_path == 'None':
    exit(0)
JPEGdir = args.image_path#输入图片文件夹
XMLdir = args.xml_path#输入标注文件夹

jpgslist = os.listdir(JPEGdir)
jpgsNameList = [i.split('.')[0] for i in jpgslist]#去掉文件扩展名
xmlslist = os.listdir(XMLdir)
xmlsName = [i.split('.')[0] for i in xmlslist]#去掉文件扩展名

orderList=[args.prefix+str(i) for i in range(1,len(jpgslist)+1)]#不带后缀名

for i in range(len(jpgslist)):
    jpg=jpgslist[i]
    temp=jpg.split('.')[-1]#获取该文件的扩展名
    newName=orderList[i]
    print jpg,newName
    os.rename(JPEGdir+jpg,JPEGdir+newName+'.'+temp)#改图片名称,不更改成统一的后缀名
    xml=jpg.split('.')[0]+'.xml'
    print xml
    if xml in xmlslist:
        os.rename(XMLdir+xml,XMLdir+newName+'.xml')
