# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 08:27:56 2018

@author: bai
"""

#encoding=utf8
'''
@author: bai
'''

import os
import argparse
import random

def main(args):
    '''main '''
    test_percent = args.test
    
    fin = open(args.list_file,'r')
    lines = fin.readlines()
    fin.close()
    
    total = len(lines)
    random_index = random.sample(range(total), total)
    
    test = int(total*test_percent)
    
    trainIndex = random_index[:total-test]
    testIndex = random_index[total-test:]
    
    ftest = open(os.path.join(args.txt_path , 'val.txt'), 'w')  
    ftrain = open(os.path.join(args.txt_path , 'train.txt'), 'w')  
    
    for i  in trainIndex:
        name=lines[i].replace('\n','')+'\n'
        ftrain.write(name)
    for i  in testIndex:
        name=lines[i].replace('\n','')+'\n'
        ftest.write(name)
            
            
    ftest.close()
    ftrain.close()
    print('end')
    
def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--list_file','-lf', dest='list_file', help='list file to read',default='None')
    parser.add_argument('--txt_path','-tp', dest='txt_path', help='file directory to save',default='None')
    parser.add_argument('--test','-t', dest='test', help='test percent',type=float,default=0.05)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.list_file == 'None' or args.txt_path == 'None':
        exit(0)
    main(args)
