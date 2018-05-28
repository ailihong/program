# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:30:24 2018

@author: bai
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

fp = open('out.txt','w')
a = ET.Element('annotation')
b1 = ET.SubElement(a, 'filename')
b1.text = "000009.jpg"
b2 = ET.SubElement(a, 'size')
b2_1 = ET.SubElement(b2, 'width')
b2_1.text = '500'
b2_2 = ET.SubElement(b2, 'height')
b2_2.text = '375'
b2_3 = ET.SubElement(b2, 'depth')
b2_3.text = '3'
b3 = ET.SubElement(a, 'object')
b3_1 = ET.SubElement(b3, 'name')
b3_1.text = 'horse'
b3_2 = ET.SubElement(b3, 'bndbox')
b3_2_1 = ET.SubElement(b3_2, 'xmin')
b3_2_1.text = '69'
b3_2_2 = ET.SubElement(b3_2, 'ymin')
b3_2_2.text = '172'
b3_2_3 = ET.SubElement(b3_2, 'xmax')
b3_2_3.text = '270'
b3_2_4 = ET.SubElement(b3_2, 'ymax')
b3_2_4.text = '330'

tree = ET.ElementTree(a)
tree.write(fp)
fp.close()
#产生的xml可以被imglabel正确解析
