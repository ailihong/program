#!/usr/bin/python3
'''
python程序的主程序例程
'''
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--net', dest='demo_net',type=str, help='Network to use [vgg16 res101]',
                        default='res101')
    parser.add_argument('--dataset','-d',required = True, dest='dataset', help='Trained dataset [pascal_voc pascal_voc_0712]',
                        default='pascal_voc_0712')#required = True 表示必须的参数
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    
