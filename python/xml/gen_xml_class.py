# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:30:24 2018

@author: bai
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



class gen_xml():
    def __init__(self,root='annotation'):
        '''
        最多3层
        '''
        self.root_a = ET.Element(root)
        
        self.sub_root_a = None
        self.sub_sub_root_a = None
        
    def set_sub_node(self,last,sub_node,val):#last = root','sub_root' or 'sub_sub_root'
        if last == 'root':
            b = ET.SubElement(self.root_a, sub_node)
            b.text = val
        elif last == 'sub_root':
            b = ET.SubElement(self.sub_root_a, sub_node)
            b.text = val
        elif last == 'sub_sub_root':
            b = ET.SubElement(self.sub_sub_root_a, sub_node)
            b.text = val
            
    def set_sub_root(self,last,sub_root):#last = root','sub_root'
        if last == 'root':
            self.sub_root_a = ET.SubElement(self.root_a, sub_root)
        elif last == 'sub_root':
            self.sub_sub_root_a = ET.SubElement(self.sub_root_a, sub_root)
    def out(self,filename):
        fp = open(filename,'w')
        tree = ET.ElementTree(self.root_a)
        tree.write(fp)
        fp.close()
        
my_xml = gen_xml('annotation')

my_xml.set_sub_node('root','filename','000009.jpg')

my_xml.set_sub_node('root','folder','VOC2007')

my_xml.set_sub_root('root','size')

my_xml.set_sub_node('sub_root','width','500')

my_xml.set_sub_node('sub_root','height','375')

my_xml.set_sub_node('sub_root','depth','3')

my_xml.set_sub_root('root','object')

my_xml.set_sub_node('sub_root','name','horse')

my_xml.set_sub_root('sub_root','bndbox')

my_xml.set_sub_node('sub_sub_root','xmin','69')

my_xml.set_sub_node('sub_sub_root','ymin','172')

my_xml.set_sub_node('sub_sub_root','xmax','270')

my_xml.set_sub_node('sub_sub_root','ymax','330')

my_xml.set_sub_root('root','object')

my_xml.set_sub_node('sub_root','name','person')

my_xml.set_sub_root('sub_root','bndbox')

my_xml.set_sub_node('sub_sub_root','xmin','285')

my_xml.set_sub_node('sub_sub_root','ymin','201')

my_xml.set_sub_node('sub_sub_root','xmax','327')

my_xml.set_sub_node('sub_sub_root','ymax','331')
my_xml.out('out.xml')
#产生的xml能被labelimg解析识别
