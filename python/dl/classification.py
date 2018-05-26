# -*- coding:utf-8 -*-
# 用于模型的单张图像分类操作
import sys,os
caffe_root = '/home/caffe-ssd/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')
os.environ['GLOG_minloglevel'] = '2' # 将caffe的输出log信息不显示，必须放到import caffe前
import caffe,cv2
import numpy as np
import time
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--caffe_weights','-cw', dest='weights',type=str, help='JPEGImages path to read',
                        default='None')
    parser.add_argument('--caffe_def','-cd', dest='caffe_def',type=str, help='JPEGImages path to save',
                        default='None')
    parser.add_argument('--labels','-l', dest='labels', help='xml path to read',
                        default='None')
    parser.add_argument('--mean','-m', dest='mean', help='xml path to save',
                        default='None')
    parser.add_argument('--image','-i', dest='image', help='xml path to save',
                        default='None')
    args = parser.parse_args()

    return args
    
args = parse_args()
if args.weights == 'None' or args.caffe_def == 'None' \
or args.labels == 'None' or args.mean == 'None':
    print('please enter parameter')
    exit(0)
#CPU或GPU模型转换
#caffe.set_mode_cpu()
caffe.set_mode_gpu()
caffe.set_device(0)
# 网络参数（权重）文件
caffemodel = args.weights
# 网络实施结构配置文件
deploy = args.caffe_def
#标签
synset_words = args.labels

# 网络实施分类
net = caffe.Net(deploy,  # 定义模型结构
                caffemodel,  # 包含了模型的训练权值
                caffe.TEST)  # 使用测试模式(不执行dropout)

# 加载ImageNet图像均值 (随着Caffe一起发布的)
mu = np.load(args.mean)
mu = mu.mean(1).mean(1)  # 对所有像素值取平均以此获取BGR的均值像素值
# 图像预处理
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', mu)
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))
#预测
img = cv2.imread(args.image)

im = cv2.resize(img,(112,112))
# 导入输入图像
net.blobs['data'].data[...] = transformer.preprocess('data', im)

start = time.time()
# 执行测试
net.forward()
end = time.time()
print('classification time: %s s' % (end - start))
# 查看目标检测结果
labels = np.loadtxt(synset_words, str, delimiter='\n')

category = net.blobs['prob'].data[0].argmax()
print('category:',category)
class_str = labels[int(category)].split(',')
class_name = class_str[0]
print('predict:'+class_name)
os.system('echo %s > predict.txt'%class_name)
