# -*- coding: utf-8 -*-
"""
need to install dicttoxml
pip install dicttoxml
"""
from dicttoxml import dicttoxml

s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
xml=dicttoxml(s,custom_root='annotation')
fp = open('out.xml','w')
fp.write(xml)
fp.close()
