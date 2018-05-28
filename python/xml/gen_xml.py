# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:30:24 2018

@author: bai
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

fp = open('out.xml','w')
root = ET.Element('annotation')
b = ET.SubElement(root, 'filename')
b.text = "000009.jpg"
b = ET.SubElement(root, 'folder')
b.text = "VOC2007"
b = ET.SubElement(root, 'size')
c = ET.SubElement(b, 'width')
c.text = '500'
c = ET.SubElement(b, 'height')
c.text = '375'
c = ET.SubElement(b, 'depth')
c.text = '3'
b = ET.SubElement(root, 'object')
c = ET.SubElement(b, 'name')
c.text = 'horse'
c = ET.SubElement(b, 'bndbox')
d = ET.SubElement(c, 'xmin')
d.text = '69'
d = ET.SubElement(c, 'ymin')
d.text = '172'
d = ET.SubElement(c, 'xmax')
d.text = '270'
d = ET.SubElement(c, 'ymax')
d.text = '330'

tree = ET.ElementTree(root)
tree.write(fp)
fp.close()
