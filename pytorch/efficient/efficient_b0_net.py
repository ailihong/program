import numpy as np

import torch
from torch import nn
from model import EfficientNet
        
if __name__ == '__main__':

    import argparse
#    from efficientnet_pytorch import EfficientNet

    parser = argparse.ArgumentParser(
        description='Convert TF model to PyTorch model and save for easier future loading')
    parser.add_argument('--model_name', type=str, default='efficientnet-b0',
                        help='efficientnet-b{N}, where N is an integer 0 <= N <= 7')
    parser.add_argument('--pth_file', type=str, default='efficientnet-b0.pth',
                        help='input PyTorch model file name')
    args = parser.parse_args()

    # Build model
    model = EfficientNet.from_name(args.model_name)
                                
    pretrained_weights = torch.load(args.pth_file)
    #    model.load_state_dict(pretrained_weights)#error,key mismatched
#    print(type(pretrained_weights),dir(pretrained_weights))#<class 'collections.OrderedDict'>
#    for key in pretrained_weights.keys():
#        print(key)
    del pretrained_weights['_fc.weight']#delete unuseful weights
    del pretrained_weights['_fc.bias']
#    for key in pretrained_weights.keys():
#        print(key)
    model.load_state_dict(pretrained_weights)
    
#    from torchsummary import summary
#    summary(model.cuda(), input_size=(3, 320, 320))
    
#    dummy_input = torch.randn(1, 3, 320, 320)
#    outs = model.model.forward(dummy_input)
#    for out in outs:
#        print(out.shape)
#    outs = model.bifpn.forward(outs)
#    for out in outs:
#        print(out.shape)
#    torch.Size([1, 40, 40, 40])
#    torch.Size([1, 112, 20, 20])
#    torch.Size([1, 1280, 10, 10])
#    torch.Size([1, 88, 40, 40])
#    torch.Size([1, 88, 20, 20])
#    torch.Size([1, 88, 10, 10])
    
    # Save PyTorch file
#    torch.save(model.state_dict(), args.output_file)
#    torch.save(model, args.output_file)
    #to onnx
    model.model.set_swish(memory_efficient=False)
    dummy_input = torch.randn(1, 3, 320, 320)

    torch.onnx.export(model, dummy_input, "test-b0.onnx", verbose=True)
