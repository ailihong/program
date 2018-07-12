#!/usr/bin/env python
import os
import random
import argparse

parser = argparse.ArgumentParser(description='batch rename')
parser.add_argument('--xml', dest='xml', help='file directory',default='None')
parser.add_argument('--txt', dest='txt', help='file directory',default='None')
parser.add_argument('--test', dest='test', help='test percent',type=float,default=0.05)
args = parser.parse_args()

test_percent = args.test
if args.xml != 'None' or args.txt != 'None':
    xmlfilepath = args.xml
    txtsavepath = args.txt
else:
    print('enter parameters')
    exit(0)
total_xml = os.listdir(xmlfilepath) 
allNum = len(total_xml)
test = int(allNum*test_percent)

trainIndex = range(allNum)
testIndex = random.sample(trainIndex, test)

ftest = open(os.path.join(txtsavepath , 'val.txt'), 'w')  
ftrain = open(os.path.join(txtsavepath , 'train.txt'), 'w')  

for i  in trainIndex:  
    name=total_xml[i][:-4]+'\n'
    if i in testIndex:
        ftest.write(name)
    else:
        ftrain.write(name)
        
ftest.close()
ftrain.close()
