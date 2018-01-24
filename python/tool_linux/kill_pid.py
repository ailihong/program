
# -*- coding: utf-8 -*-
"""
备注:杀死进程kill ,需要root权限
功能:通过查找得到对应的pid,然后kill
需要杀死的进程的描述:
wpa_supplicant
dhclient
python
"""
import os
import argparse
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='kill pid by task')
    parser.add_argument('--task','-t', dest='task', help='task description',default=None)
    args = parser.parse_args()
    return args

def main(args):
    str_out = os.popen('ps -C %s -o pid='%args.task)
    str_ = str_out.read()
    str_ = str_[:-1]#去掉最后一个\n
    id_ = str_.split('\n')
    #print id_
    #print len(id_)
    for i in range(len(id_)):
        id_[i] = id_[i].replace(' ','')
        cmd = "kill -9 %s"%id_[i]
        print cmd
        os.system(cmd)

if __name__ == '__main__':
    args = parse_args()
    if args.task == None:
        print 'please enter task description'
    else:
        main(args)
