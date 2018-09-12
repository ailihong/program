# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:46:07 2018
打印depth异常的xml,并删掉xml,另外检查xml和jpg是否都存在，否则删掉
@author: bai
"""
import argparse
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    
    parser.add_argument('--Annotations','-a', dest='xml_path', help='xml path to read',
                        default='None')
    parser.add_argument('--jpg','-j', dest='jpg_path', help='jpg path to read',
                        default='None')
    args = parser.parse_args()

    return args

def main(args):
    list_xml=os.listdir(args.xml_path)
    
    if len(list_xml)==0:
        return
    
    to_delete=[]
    for xml_name in list_xml:
        tree = ET.ElementTree(file=os.path.join(args.xml_path,xml_name))
        have = False
        if not os.path.exists(os.path.join(args.jpg_path,xml_name[:-3]+'jpg')):
            have = True
        for elem in tree.iter():
            if elem.tag =='depth' and elem.text != '3':
                have = True
            if elem.tag =='width' and elem.text == '0':
                have = True
            if elem.tag =='height' and elem.text == '0':
                have = True
        if have:
            to_delete.append(xml_name)
    for xml_name in to_delete:
        os.system('rm %s'%os.path.join(args.xml_path,xml_name))
        os.system('rm %s'%os.path.join(args.jpg_path,xml_name[:-3]+'jpg'))
        print(xml_name)
    
    list_xml=os.listdir(args.xml_path)
    list_jpg=os.listdir(args.jpg_path)
    to_delete=[]
    for jpg in list_jpg:
        xml_name=jpg.replace('.jpg','.xml')
        if xml_name not in list_xml:
            to_delete.append(jpg)
    for jpg_name in to_delete:
        os.system('rm %s'%os.path.join(args.jpg_path,jpg_name))
        print(jpg_name)
    
                    

if __name__ == '__main__':
    args = parse_args()
    if args.xml_path == 'None':
        exit(0)
    main(args)
    print('end')
