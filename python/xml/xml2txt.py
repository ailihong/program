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

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--xml-dir', dest='xml_dir', help='xml file directory',default='None')
    parser.add_argument('--jpeg-dir', dest='jpeg_dir', help='jpeg image file directory',default='None')
    parser.add_argument('--path-to-txt-file', dest='txt_file', help='path to save label txt file',default='None')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.xml_dir == 'None' or args.jpeg_dir == 'None' or args.txt_file == 'None':
        print('input,output directory is not given,please add --help')
    else:
        list_name = os.listdir(args.xml_dir)

        total = len(list_name)
        len_total = len('%d' % total)
        n = 0
        #判断保存文件是否存在，不存在则新建

        txt_file = open(args.txt_file, 'w')#直接打开一个文件，如果文件不存在则创建文件

        for name in list_name:
            n += 1
            print('doing,%d/%d\n' % (n, total))
            xml_dir=args.xml_dir
            if args.xml_dir[-1] != '/':
                xml_dir += '/'

            #打开xml文件
            # 使用minidom解析器打开 XML 文档
            DOMTree = xml.dom.minidom.parse(xml_dir+name)
            collection = DOMTree.documentElement
            # 在集合中获取所有name
            class_name_len=len(collection.getElementsByTagName("name"))
            # 格式化每个name的详细信息
            for i in range(class_name_len):
                #文件路径
                path_str = args.jpeg_dir
                if args.jpeg_dir[-1]!='/':
                    path_str +='/'
                path_str += collection.getElementsByTagName("filename")[0].childNodes[0].data
                #坐标
                coor=',%s,%s,%s,%s,'%(collection.getElementsByTagName("xmin")[i].childNodes[0].data, \
                                      collection.getElementsByTagName("ymin")[i].childNodes[0].data, \
                                      collection.getElementsByTagName("xmax")[i].childNodes[0].data, \
                                      collection.getElementsByTagName("ymax")[i].childNodes[0].data)
                #类别
                class_name='%s'%collection.getElementsByTagName("name")[i].childNodes[0].data

                lines_str=path_str+coor+class_name+'\n'
                txt_file.write(lines_str)
        txt_file.close()
