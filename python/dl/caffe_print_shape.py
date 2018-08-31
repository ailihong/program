import numpy as np  
import sys
caffe_root = '/home/caffe-ssd/'
sys.path.insert(0, caffe_root + 'python')  
import caffe  
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--proto','-p', dest='proto',type=str, help='prototxt path to read',
                        default='None')
    parser.add_argument('--model','-m', dest='model',type=str, help='caffemodel path to read',
                        default='None')
    args = parser.parse_args()

    return args
def print_shape(net):
    for key in net.params.keys():
        print('key:',key)
        if type(net.params[key]) is caffe._caffe.BlobVec:
            for i, element in enumerate(net.params[key]):
#                print(i, element)
                print(net.params[key][i].data.shape)
            
args = parse_args()
if args.proto == 'None' or args.model == 'None':
    exit(0)
net = caffe.Net(args.proto, args.model, caffe.TRAIN)   

print_shape(net)

