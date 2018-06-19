#encoding=utf8
'''
Detection with SSD
In this example, we will load a SSD model and use it to detect objects.
'''

import os
import sys
import argparse,time
import numpy as np
import cv2
# Make sure that caffe is on the python path:
caffe_root = '../../caffe-ssd'
sys.path.insert(0, os.path.join(caffe_root, 'python'))
os.environ['GLOG_minloglevel'] = '2' # 将caffe的输出log信息不显示，必须放到import caffe前
import caffe

from google.protobuf import text_format
from caffe.proto import caffe_pb2

dim=(96,112)#width,height

class CaffeDetection:
    def __init__(self, model_def, model_weights):
        caffe.set_mode_cpu()
        # Load the net in the test phase for inference, and configure input preprocessing.
        self.net = caffe.Net(model_def,      # defines the structure of the model
                             model_weights,  # contains the trained weights
                             caffe.TEST)     # use test mode (e.g., don't perform dropout)
         # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        # load PASCAL VOC labels
    
    def detect(self, image_file, conf_thresh=0.5, topn=5):
        '''
        SSD detection
        '''
        # set net to batch size of 1
        # image_resize = 300
        self.net.blobs['data'].reshape(1, 3, dim[1],dim[0] )
        src = cv2.imread(image_file)
        #Run the net and examine the top_k results
        image = cv2.resize(src, dim)
        image = image - [127.5]
        image = image * 0.0078125
        #[high,weight,channels] --> [channels,high,weight]
        image = image.transpose(2,0,1)
        now = time.time()
        self.net.blobs['data'].data[...] = image

        # Forward pass.
        detections = self.net.forward()['fc5']
        print('inference time:',time.time() - now)
        print('num:%s',len(detections[0]),detections)
        

def main(args):
    '''main '''
    detection = CaffeDetection(
                               args.model_def, args.model_weights
                        )
    detection.detect(args.image_file,conf_thresh=0.4)


def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_def','-MD',
                        default='examples/Pelee/model/pelee/VOC0712/SSD_304x304/deploy.prototxt')
    parser.add_argument('--model_weights','-MW',
                        default='examples/Pelee/model/pelee/VOC0712/SSD_304x304/pelee_SSD_304x304_iter_28000.caffemodel')
    parser.add_argument('--image_file', '-IF',default='examples/images/fish-bike.jpg')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
