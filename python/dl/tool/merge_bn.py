import numpy as np  
import sys
caffe_root = '/home/caffe-ssd/'
sys.path.insert(0, caffe_root + 'python')  
import caffe  
import argparse

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--train_proto','-tp', dest='train_proto',type=str, help='JPEGImages path to read',
                        default='None')
    parser.add_argument('--train_model','-tm', dest='train_model',type=str, help='JPEGImages path to save',
                        default='None')
    parser.add_argument('--deploy_proto','-dp', dest='deploy_proto', help='xml path to read',
                        default='None')
    parser.add_argument('--save_model','-sm', dest='save_model', help='xml path to save',
                        default='None')
    args = parser.parse_args()

    return args
def merge_bn(net, nob):
    '''
    merge the batchnorm, scale layer weights to the conv layer, to  improve the performance
    var = var + scaleFacotr
    rstd = 1. / sqrt(var + eps)
    w = w * rstd * scale
    b = (b - mean) * rstd * scale + shift
    '''
    for key in nob.params.keys():
        if type(nob.params[key]) is caffe._caffe.BlobVec:
            print('key:',key)
            if key.endswith("/bn") or key.endswith("/scale"):
                continue
            else:
                conv = net.params[key]
                if key+'/bn' not in net.params:
                    print('no bn key:',key)
                    for i, w in enumerate(conv):
                        nob.params[key][i].data[...] = w.data
                else:
                    print('bn key:',key)
                    bn = net.params[key + "/bn"]
                    scale = net.params[key + "/scale"]
                    wt = conv[0].data
                    channels = wt.shape[0]
                    bias = np.zeros(wt.shape[0])
                    if len(conv) > 1:
                        bias = conv[1].data
                    mean = bn[0].data
                    var = bn[1].data
                    scalef = bn[2].data

                    scales = scale[0].data
                    shift = scale[1].data

                    if scalef != 0:
                        scalef = 1. / scalef
                    mean = mean * scalef
                    var = var * scalef
                    rstd = 1. / np.sqrt(var + 1e-5)
                    rstd1 = rstd.reshape((channels,1,1,1))
                    scales1 = scales.reshape((channels,1,1,1))
                    wt = wt * rstd1 * scales1
                    bias = (bias - mean) * rstd * scales + shift
                    
                    nob.params[key][0].data[...] = wt
                    #if len(nob.params[key])==2:#bias_term is not false
                    nob.params[key][1].data[...] = bias
  
args = parse_args()
if args.train_proto == 'None' or args.train_model == 'None' \
or args.deploy_proto == 'None' or args.save_model == 'None':
    exit(0)
net = caffe.Net(args.train_proto, args.train_model, caffe.TRAIN)  
net_deploy = caffe.Net(args.deploy_proto, caffe.TEST)  

merge_bn(net, net_deploy)
net_deploy.save(args.save_model)
