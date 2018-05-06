import os  
import random
import argparse

parser = argparse.ArgumentParser(description='batch rename')
parser.add_argument('--xml', dest='xml', help='file directory',default='None')
parser.add_argument('--txt', dest='txt', help='name',default='None')
args = parser.parse_args()

trainval_percent = 0.5
train_percent = 0.5
if args.xml != 'None' or args.txt != 'None':
    xmlfilepath = args.xml
    txtsavepath = args.txt
else:
    print('enter parameters')
    exit(0)
total_xml = os.listdir(xmlfilepath)  

num=len(total_xml)  
list=range(num)  
tv=int(num*trainval_percent)  
tr=int(tv*train_percent)  
trainval= random.sample(list,tv)  
train=random.sample(trainval,tr)  
  
ftrainval = open(os.path.join(txtsavepath , 'trainval.txt'), 'w')  
ftest = open(os.path.join(txtsavepath , 'test.txt'), 'w')  
ftrain = open(os.path.join(txtsavepath , 'train.txt'), 'w')  
fval = open(os.path.join(txtsavepath , 'val.txt'), 'w')  
  
for i  in list:  
    name=total_xml[i][:-4]+'\n'  
    if i in trainval:  
        ftrainval.write(name)  
        if i in train:  
            ftrain.write(name)  
        else:  
            fval.write(name)  
    else:  
        ftest.write(name)  
  
ftrainval.close()  
ftrain.close()  
fval.close()  
ftest .close()
