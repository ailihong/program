#!/usr/bin/python3
'''
批量替代文件中的JPG，JPEG为jpg，输入old_dir,new_dir
'''
import os
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--old_dir', dest='old', help='old file directory',default='None')
    parser.add_argument('--new_dir', dest='new', help='new file directory',default='None')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.old=='None' or args.new=='None':
        print('directory is not given,please add --help')
    else:
        old_list=os.listdir(args.old)

        total=len(old_list)
        len_total=len('%d'%total)
        n=0
        for old_name in old_list:
            n+=1
            # 打开旧文件
            f = open(args.old+old_name,'r',encoding='utf-8')
            # 打开新文件
            f_new = open(args.new+old_name,'w',encoding='utf-8')

            # 循环读取旧文件
            for line in f:
                # 进行判断
                if "JPG" in line:
                    line = line.replace("JPG", 'jpg')
                if 'JPEG' in line:
                    line = line.replace('JPEG', 'jpg')
                # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
                f_new.write(line)

            f.close()
            f_new.close()

            print('doing,%d/%d\n'%(n,total))
