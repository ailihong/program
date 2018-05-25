# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:20:54 2018

@author: bai
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


tree = ET.ElementTree(file='000021.xml')
for elem in tree.iter():
    print elem.tag, elem.text
#annotation 
#	
#folder VOC2007
#filename 000021.jpg
#source 
#		
#database The VOC2007 Database
#annotation PASCAL VOC2007
#image flickr
#flickrid 326914724
#owner 
#		
#flickrid Apple Crisp
#name Layne Russell
#size 
#		
#width 336
#height 500
#depth 3
#segmented 0
#object 
#		
#name dog
#pose Right
#truncated 1
#difficult 0
#bndbox 
#			
#xmin 1
#ymin 235
#xmax 182
#ymax 388
#object 
#		
#name person
#pose Unspecified
#truncated 0
#difficult 0
#bndbox 
#			
#xmin 210
#ymin 36
#xmax 336
#ymax 482
#part 
#			
#name head
#bndbox 
#				
#xmin 238
#ymin 37
#xmax 287
#ymax 104
#part 
#			
#name foot
#bndbox 
#				
#xmin 220
#ymin 411
#xmax 278
#ymax 444
#part 
#			
#name foot
#bndbox 
#				
#xmin 245
#ymin 441
#xmax 314
#ymax 479
#object 
#		
#name person
#pose Unspecified
#truncated 0
#difficult 0
#bndbox 
#			
#xmin 46
#ymin 82
#xmax 170
#ymax 365
#part 
#			
#name foot
#bndbox 
#				
#xmin 133
#ymin 340
#xmax 154
#ymax 360
#part 
#			
#name head
#bndbox 
#				
#xmin 93
#ymin 84
#xmax 132
#ymax 142
#part 
#			
#name hand
#bndbox 
#				
#xmin 110
#ymin 228
#xmax 131
#ymax 245
#object 
#		
#name person
#pose Unspecified
#truncated 0
#difficult 0
#bndbox 
#			
#xmin 11
#ymin 181
#xmax 142
#ymax 419
#part 
#			
#name hand
#bndbox 
#				
#xmin 113
#ymin 245
#xmax 128
#ymax 268
#part 
#			
#name foot
#bndbox 
#				
#xmin 50
#ymin 396
#xmax 102
#ymax 417
#part 
#			
#name foot
#bndbox 
#				
#xmin 26
#ymin 372
#xmax 52
#ymax 405
#part 
#			
#name head
#bndbox 
#				
#xmin 66
#ymin 185
#xmax 109
#ymax 239
