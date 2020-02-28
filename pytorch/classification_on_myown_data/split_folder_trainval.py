# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:53:41 2020

@author: baijun
根据图片文件夹按比例分成train val两部分,文件名可以任意命名，不用1,2数字也可以
输入图片目录结构:
glasses_class_data/
├── 1
│   └── test1.jpg
└── 2
    └── test1.jpg
输出图片目录结构:
glasses_class_data/
├── train
│   ├── 1
│   │   └── test1.jpg
│   └── 2
│       └── test1.jpg
└── val
    ├── 1
    │   └── test1.jpg
    └── 2
        └── test1.jpg

"""
import argparse
import os
import random

parser = argparse.ArgumentParser(description='Train PNet',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--image_path',dest='image_path',help='image path',
                        default='./',required=True, type=str)
parser.add_argument('-t','--train_path', dest='train_path', help='training image path',
                        default='train_data',type=str)
parser.add_argument('-v','--val_path', dest='val_path', help='val image path',
                        default='val_data', type=str)
parser.add_argument('-p','--train_percent', dest='train_percent', help='train image percent,default:0.8',
                        default=0.8,type=float)
args = parser.parse_args()

image_path = args.image_path
train_path = args.train_path
val_path = args.val_path
train_percent = args.train_percent


if not os.path.exists(val_path):
    os.system("mkdir -p {}".format(val_path))

class_folder = os.listdir(image_path)
for folder in class_folder:
    name_list = os.listdir(os.path.join(image_path,folder))
    random.shuffle(name_list)
    train_data_num = int(len(name_list)*train_percent)
    train_list = name_list[:train_data_num]
    val_list = name_list[train_data_num:]
    
    phase = ['train','val']
    filelist = {'train':train_list,'val':val_list}
    savelist = {'train':train_path,'val':val_path}
    
    for pha in phase:
        if not os.path.exists(os.path.join(savelist[pha],folder)):
            os.system("mkdir -p {}".format(os.path.join(savelist[pha],folder)))
        
        for name in filelist[pha]:
            src_filename = os.path.join(image_path,folder,name)
            dst_filename = os.path.join(savelist[pha],folder,name)
            os.system("cp {} {}".format(src_filename,dst_filename))
            
print("done")
