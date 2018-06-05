# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 15:29:48 2018
对prototxt中num_output进行减半操作
@author: bai
"""
import argparse,re

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--prototxt1','-p1', dest='prototxt1',type=str, help='path to read',
                        default='None')
    parser.add_argument('--prototxt2','-p2', dest='prototxt2',type=str, help='path to save',
                        default='None')
    parser.add_argument('--start_top','-st', dest='start_top',type=str, help='start top',
                        default='None')
    parser.add_argument('--end_top','-et', dest='end_top',type=str, help='end top,not including',
                        default='None')
    parser.add_argument('--type','-t', dest='type',type=str, help='double or half',
                        default='half')
    args = parser.parse_args()

    return args
    
if __name__ == '__main__':
    args = parse_args()
    if args.prototxt1 == 'None' or args.prototxt2 == 'None':
        exit(0)
    
    fp_rd = open(args.prototxt1,'r')
    
    start_top = False
    end_top = False
    file_data = ''
    for line in fp_rd:
        new_line = line
        if args.start_top in line and 'top:' in line:
            start_top = True
            
        if args.end_top in line and 'top:' in line:
            end_top = True
            
        if start_top and end_top == False and 'num_output' in line:
            num = re.findall('\d+',line)[0]
            num = int(num)
            num_change = num
            if args.type == 'half':
                num_change /= 2
            else:
                num_change *= 2
            if num > 9 and num < 100:
                new_line = new_line[:-3]+str(num_change)+'\n'
            elif num > 99:
                new_line = new_line[:-4]+str(num_change)+'\n'
            else:
                new_line = new_line[:-2]+str(num_change)+'\n'
        file_data += new_line
    fp_wd = open(args.prototxt2,'w')
    fp_wd.write(file_data)
    
    fp_wd.close()
    fp_rd.close()
    print('end')
