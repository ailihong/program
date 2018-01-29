#!/usr/bin/python
#coding:utf8
'''
批处理，将xml文件转换为simple label txt，其格式为/path/to/img.jpg,x1,y1,x2,y2,class_name
需要指定xml、jpg、以及保存txt的path
'''
from __future__ import print_function
import os
import argparse
from xml.dom.minidom import parse
import xml.dom.minidom

if __name__ == '__main__':
        #打开xml文件
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse('./1.xml')
        collection = DOMTree.documentElement
        # 在集合中获取所有name
        print(collection.getElementsByTagName("name"))
        #names = collection.getElementsByTagName("name")
        # 格式化每个name的详细信息
        #for name_ in names:

        print(collection.getElementsByTagName("name")[0].childNodes[0].data)#person
        print(collection.getElementsByTagName("name")[1].childNodes[0].data)#hand

        print(collection.getElementsByTagName("xmin")[0].childNodes[0].data)  # person
        print(collection.getElementsByTagName("ymin")[1].childNodes[0].data)  # hand
