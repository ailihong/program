#!/usr/bin/python3
#coding:utf8
'''
批量重命名，会删除原来的文件！！！，使用前注意备份,命名会自动补零
'''
import os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--dir', dest='dir', help='file directory',default='None')
    parser.add_argument('--name', dest='name', help='name',default='bai')
    parser.add_argument('--date', dest='date', help='date',default='None')
    parser.add_argument('--end', dest='end', help='file type',default='None')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.dir=='None' or args.date=='None' or args.end=='None':
        print('input,output directory or data is not given,please add --help')
    else:
        list_name=os.listdir(args.dir)#不是绝对路径，只是文件名file.file

        total=len(list_name)
        len_total=len('%d'%total)
        n=0
        for name in list_name:
            n+=1
            new_name = args.name + args.date + '_%0*d.'%(len_total,n) + args.end
            dir_temp = args.dir
            if args.dir[-1]!='/':
                dir_temp=args.dir+'/'
            os.rename(dir_temp + name,dir_temp +new_name)
            print('doing,%d/%d\n'%(n,total))

