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
    parser.add_argument('--proto2','-p2', dest='proto2',type=str, help='prototxt path to read',
                        default='None')
    parser.add_argument('--model2','-m2', dest='model2',type=str, help='caffemodel path to read',
                        default='None')
    args = parser.parse_args()

    return args
def copy(net,net_copy):
    for key in net_copy.params.keys():
        print('key:',key)
        if type(net_copy.params[key]) is caffe._caffe.BlobVec:
            for i, element in enumerate(net_copy.params[key]):
                print(i,net_copy.params[key][i].data.shape)
                net_copy.params[key][i].data[...] = net_copy.params[key][i].data

args = parse_args()
if args.proto == 'None' or args.model == 'None':
    exit(0)

net = caffe.Net(args.proto, args.model, caffe.TRAIN)  
net_copy = caffe.Net(args.proto2, caffe.TEST)  

copy(net,net_copy)
net_copy.save(args.model2)
