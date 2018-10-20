#encoding=utf8
'''
@author: bai
追加模式
'''

import os
import argparse

def main(args):
    '''main '''
    file_list = os.listdir(args.file_path)
    fout=open(args.list_file,'a')
    for file_name in file_list:
        path=os.path.join(args.file_path,file_name)
        fout.write(path+' %d\n'%args.label)
    print('end')
def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', '-fp',default='None', type=str)
    parser.add_argument('--label','-l', default=-1, type=int)
    parser.add_argument('--list_file','-lf',type=str, default='None',help='append mode')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.file_path == 'None' or args.label == -1 or args.list_file == 'None':
        exit(0)
    main(args)
