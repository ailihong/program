# -*- coding: utf-8 -*-
'''
读取train_val.txt文件，打乱并生成train.txt,val.txt
'''
import os  
import random
import argparse

parser = argparse.ArgumentParser(description='batch rename')
parser.add_argument('--txt', dest='txt', help='file directory',default='None')
parser.add_argument('--per', dest='per', type = float,help='file directory',default=0.95)
args = parser.parse_args()


if args.txt == 'None':
    print('enter parameters')
    exit(0)  
train_percent = args.per
root_path = os.path.split(args.txt)[0]
fp = open(args.txt,'r')

train_txt = os.path.join(root_path,'train.txt')
val_txt = os.path.join(root_path,'val.txt')
fp_train = open(train_txt,'wb')
fp_val = open(val_txt,'wb')

train_val = fp.readlines()
num=len(train_val)  
list_=range(num)
#print 'list ',list_
tr=int(num*train_percent)

list_random = random.sample(list_,num)
val= list_random[tr+1:]
#print 'val ',val
train=list_random[:tr]
#print 'train ',train

for i in train:  
    fp_train.write(train_val[i])
for i in val: 
    fp_val.write(train_val[i])  
    
fp_train.close()  
fp_val.close()  
fp.close()
