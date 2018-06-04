# -*- coding:utf-8 -*-
'''
python3 feature_extraction.py --caffe_weights snapshot/0526_iter_25000.caffemodel \
--caffe_def prototxt/deploy.prototxt --mean mean.npy --image1 image/aaron_harnik/aaron_harnik_0001.jpg \
--image2 image/elizabeth_hurley/elizabeth_hurley_0001.jpg 2>&1 |tee log.log
'''
# 提取中间层作为特征，看是否能把不同于数据库里的人分开
import sys,os
caffe_root = '/home/caffe-ssd/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')
os.environ['GLOG_minloglevel'] = '2' # 将caffe的输出log信息不显示，必须放到import caffe前
import caffe
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
    parser.add_argument('--mean','-m', dest='mean', help='xml path to save',
                        default='None')
    parser.add_argument('--image1','-i1', dest='image1', help='xml path to save',
                        default='None')
    parser.add_argument('--image2','-i2', dest='image2', help='xml path to save',
                        default='None')
    args = parser.parse_args()

    return args

#Manhattan distance
def distance(vec1,vec2):
#    return np.linalg.norm(vec1-vec2)#欧式距离
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*(np.linalg.norm(vec2)))#余弦夹角
#    return sum(abs(vec1-vec2))#Manhattan distance

    
args = parse_args()
if args.weights == 'None' or args.caffe_def == 'None' \
or args.image1 == 'None' or args.mean == 'None':
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

# 网络实施分类
net = caffe.Net(deploy,  # 定义模型结构
                caffemodel,  # 包含了模型的训练权值
                caffe.TEST)  # 使用测试模式(不执行dropout)

# 加载ImageNet图像均值 (随着Caffe一起发布的)
mu = np.load(args.mean)
mu = mu.mean(1).mean(1)  # 对所有像素值取平均以此获取BGR的均值像素值
# 图像预处理,训练网络时是先减均值，然后缩放到0-1，以下预处理能得到正确的结果
#装载的图像为RGB，HWC，【0-1】的图像
# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# move image channels to outermost dimension   HWC变为CHW
transformer.set_transpose('data', (2,0,1))
# subtract the dataset-mean value in each channel
transformer.set_mean('data', mu)
# rescale from [0, 1] to [0, 255]
transformer.set_raw_scale('data', 255)
# swap channels from RGB to BGR
transformer.set_channel_swap('data', (2,1,0))
#提取特征
im=caffe.io.load_image(args.image1)
# 导入输入图像
net.blobs['data'].data[...] = transformer.preprocess('data', im)
# 执行测试
net.forward()

f1 = net.blobs['fc5'].data
#print('shape1: ',f1.shape)#(1, 25, 1, 1)
f1_npy=np.array(f1).flatten()

im=caffe.io.load_image(args.image2)
# 导入输入图像
net.blobs['data'].data[...] = transformer.preprocess('data', im)
# 执行测试
net.forward()

f2 = net.blobs['fc5'].data
f2_npy=np.array(f2).flatten()
#print('shape2: ',f2.shape)
out = distance(f1_npy,f2_npy)

#print('feature1:%s'%f1_npy)
#print('feature2:%s'%f2_npy)
print('out:',out)
#time.sleep(2)
#os.system('echo %s > predict.txt'%out)
