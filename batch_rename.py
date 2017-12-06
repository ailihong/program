
#!/usr/bin/python3
'''
批量重命名，会删除原来的文件！！！，使用前注意备份
'''
import os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--input', dest='input', help='input directory',default='None')
    parser.add_argument('--output', dest='output', help='output directory',default='None')
    parser.add_argument('--date', dest='date', help='date',default='None')
    parser.add_argument('--end', dest='end', help='file type',default='None')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.input=='None' or args.output=='None' or args.date=='None' or args.end=='None':
        print('input,output directory or data is not given,please add --help')
    else:
        list_name=os.listdir(args.input)
        n=0
        for name in list_name:
            n+=1
            new_name = 'bai' + args.date + '%d.'%n + args.end
            os.rename(args.input + name,args.output +new_name)
            print('doing,%d\n'%n)
