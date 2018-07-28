import sys
sys.path.append('.')
sys.path.append('/home/caffe-ssd/python')
import caffe
import argparse

parser = argparse.ArgumentParser(description='Caffe init')
parser.add_argument('--prototxt','-p',dest='prototxt', type=str, default='None')
parser.add_argument('--caffemodel','-c',dest='model', type=str, default='None')
args = parser.parse_args()

if args.prototxt == 'None' or args.model == 'None':
    exit(0)
deploy = args.prototxt
caffemodel = args.model
caffe.Net(deploy,caffemodel,caffe.TEST)
