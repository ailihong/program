#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 16:14:41 2018
从文本文件中复制指定的行数到另一个文件
@author: bai
"""
import os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--file1','-f1', dest='f1', type=str,help='file one to copy',default='None')
    parser.add_argument('--file2','-f2', dest='f2', type=str,help='file two to save',default='None')
    parser.add_argument('--start','-s', dest='s', type=int,help='start line to copy',default=0)
    parser.add_argument('--end','-e', dest='e', type=int,help='end line to copy',default=0)
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.s >= 0 and args.e >args.s: 
        fp_save = open(args.f2,'wb+')
        cnt_line = 0
        with open(args.f1,'rb') as fp:
            while cnt_line < args.e:
                line = fp.readline()#读一行，以'\n'结束，如果是readlines()，则将文件全部内容读入，以list的形式
#                print line
                cnt_line += 1
                if cnt_line >= args.s:
#                    pass
                    fp_save.write(line)
            fp_save.close()
            fp.close()
