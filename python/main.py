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
    #args = parser.parse_args()
    args, unparsed = parser.parse_known_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    args.demo_net
    args.dataset
    
##----sample2--------------
FLAGS = None
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-s','--stage',
      type=str,
      default='train',
      help='The stage of prototxt, train|test|deploy.'
  )
  parser.add_argument(
      '-n','--nobn',
      action='store_true',
      help='for deploy, generate a deploy.prototxt without batchnorm and scale.'
  )
  parser.add_argument(
      '-lmdb','-l',
      type=str,
      default='train_lmdb',
      help='lmdb path'
  )
  FLAGS, unparsed = parser.parse_known_args()
  FLAGS.stage
