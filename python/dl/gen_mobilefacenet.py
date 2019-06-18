'''
python3
v0.2
'''
import argparse
FLAGS = None

class Generator():

    def __init__(self):
      self.last = "data"

    def header(self, name):
      print("name: \"%s\"" % name)
    
    def data_deploy(self,input_height,input_width):
      print(
"""input: "data"
input_shape {
  dim: 1
  dim: 3
  dim: %d
  dim: %d
}""" % (input_height, input_width))
    
    def data_classifier(self,batch_size,lmdb_path):
        print(
"""layer {
    name: "data"
    type: "Data"
    top: "data"
    top: "label"
    data_param{
        source: "train_lmdb"
        backend: LMDB
        batch_size: %d
    }
    transform_param {
        scale: 0.007843
        mirror: true
        mean_value: 127.5
        mean_value: 127.5
        mean_value: 127.5
    }
    include: { phase: TRAIN }
}
layer {
    name: "data"
    type: "Data"
    top: "data"
    top: "label"
    data_param{
        source: "test_lmdb"
        backend: LMDB
        batch_size: %d
    }
    transform_param {
        scale: 0.007843
        mirror: true
        mean_value: 127.5
        mean_value: 127.5
        mean_value: 127.5
    }
    include: { phase: TEST }
}"""%(batch_size,batch_size/4))

    def classifier_loss(self,stage,bottom=None):
        if stage == 'train':
            _bottom=self.last
            if bottom is not None:
                _bottom=bottom
            print(
"""layer{
  name: "loss"
  type: "SoftmaxWithLoss"
  bottom: "%s"
  bottom: "label"
  loss_weight: 1 
}
layer {
  name: "accuracy"
  type: "Accuracy"
  bottom: "%s"
  bottom: "label"
  top: "accuracy"
  include {
    phase: TEST
  }
}""" % (_bottom,_bottom))
        if stage == 'deploy':
            _bottom=self.last
            if bottom is not None:
                _bottom=bottom
            print(
"""layer {
  name: "prob"
  type: "Softmax"
  bottom: "%s"
  top: "prob"
}"""%_bottom)

    def conv(self, name, out, kernel, stride=1, group=1, bias=False, bottom=None,pad=None):

      if self.stage == "deploy" and self.nobn: #for deploy, merge bn to bias, so bias must be true
          bias = True

      if bottom is None:
          bottom = self.last
      padstr = ""
      if kernel > 1:
          padstr = "\n    pad: %d" % (int(kernel / 2))
      if pad is not None:
          padstr = "\n    pad: %d" % (pad)
      groupstr = ""
      if group > 1:
          groupstr = "\n    group: %d\n    engine: CAFFE" % group
      stridestr = ""
      if stride > 1:
          stridestr = "\n    stride: %d" % stride 
      bias_lr_mult = ""
      bias_filler = ""
      if bias == True:
          bias_filler = """
    bias_filler {
      type: "constant"
      value: 0.0
    }"""
          bias_lr_mult = """
  param {
    lr_mult: 2.0
    decay_mult: 0.0
  }"""
      biasstr = ""
      if bias == False:
          biasstr = "\n    bias_term: false"
      print(
"""layer {
  name: "%s"
  type: "Convolution"
  bottom: "%s"
  top: "%s"
  param {
    lr_mult: 1.0
    decay_mult: 1.0
  }%s
  convolution_param {
    num_output: %d%s%s
    kernel_size: %d%s%s
    weight_filler {
      type: "msra"
    }%s
  }
}""" % (name, bottom, name, bias_lr_mult, out, biasstr, padstr, kernel, stridestr, groupstr, bias_filler))
      self.last = name
    
    def bn(self, name,bottom=None):
      _bottom=self.last
      if bottom is not None:
          _bottom=bottom
      if self.stage == "deploy" and self.nobn:  #deploy does not need bn, you can use merge_bn.py to generate a new caffemodel
         return
      eps_str = ""
      if self.eps != 1e-5:
          eps_str = "\n  batch_norm_param {\n    eps: 0.001\n  }"
      print(
"""layer {
  name: "%s"
  type: "BatchNorm"
  bottom: "%s"
  top: "%s"%s
  param {
    lr_mult: 0
    decay_mult: 0
  }
  param {
    lr_mult: 0
    decay_mult: 0
  }
  param {
    lr_mult: 0
    decay_mult: 0
  }
}
layer {
  name: "%s_scale"
  type: "Scale"
  bottom: "%s"
  top: "%s"
  param {
    lr_mult: 1.0
    decay_mult: 0.0
  }
  param {
    lr_mult: 2.0
    decay_mult: 0.0
  }
  scale_param {
    filler {
      value: 1
    }
    bias_term: true
    bias_filler {
      value: 0
    }
  }
}""" % (name,_bottom,name,eps_str,name,name,name))
      self.last = name

    def relu(self, name):
      relu_str = "ReLU"
      print(
"""layer {
  name: "%s/relu"
  type: "%s"
  bottom: "%s"
  top: "%s"
}""" % (name, relu_str, name, name))
      self.last = name
    def prelu(self, name,bottom=None):
      _bottom=self.last
      if bottom is not None:
          _bottom=bottom
      print(
"""layer {
  bottom: "%s"
  top: "%s"
  name: "%s"
  type: "PReLU"
  param {
    lr_mult: 1.0
    decay_mult: 1.0
  }
}""" % (_bottom, name, name))
      self.last = name
    def conv_act(self, name, out, kernel, stride=1, group=1, bias=False, bottom=None):
        self.conv(name, out, kernel, stride, group, bias, bottom)
        self.relu(name)
    def conv_bn_relu(self, name, num, kernel, stride=1,bottom=None,pad=None):
      self.conv(name, num, kernel, stride,bottom=bottom,pad=pad)
      self.bn(name)
      self.relu(name)
    def conv_bn(self, name, num, kernel, stride=1,bottom=None,pad=None):
      self.conv(name, num, kernel, stride,bottom=bottom,pad=pad)
      self.bn(name)#top=bottom=name
    def conv_depthwise(self, name, inp, stride=1,bottom=None):
      self.conv(name, inp, 3, stride, inp,bottom=bottom)
      self.bn(name)
      self.relu(name)

    def conv_expand(self, name, inp, outp,bottom=None):
      self.conv(name, outp, 1,bottom=bottom)
      self.bn(name)
      self.relu(name)

    def conv_project(self, name, inp, outp,bottom=None):
      self.conv(name, outp, 1,bottom=bottom)
      self.bn(name)

    def conv_dw_pw(self, name, inp, outp, stride=1,bottom=None):
      name1 = name + "/depthwise"
      self.conv(name1, inp, 3, stride, inp,bottom=bottom)
      self.bn(name1)
      self.relu(name1)
      name2 = name 
      self.conv(name2, outp, 1)
      self.bn(name2)
      self.relu(name2)
    
    def shortcut(self, name,bottom1, bottom2):
      print(
"""layer {
  name: "%s"
  type: "Eltwise"
  bottom: "%s"
  bottom: "%s"
  top: "%s"
}""" % (name, bottom1, bottom2, name))
      self.last = name
    def shortcut_relu(self, name,bottom1, bottom2):
        self.shortcut(name,bottom1, bottom2)
        self.relu(name)
    def ave_global_pool(self, name,bottom=None):
        _bottom=self.last
        if bottom is not None:
            _bottom=bottom
        print(
"""layer {
  name: "%s"
  type: "Pooling"
  bottom: "%s"
  top: "%s"
  pooling_param {
    pool: AVE
    global_pooling: true
  }
}""" % (name, _bottom, name))
        self.last = name
    def pool(self, name, _type, kernel, stride,bottom=None):
        _bottom=self.last
        if bottom is not None:
            _bottom=bottom
        print(
"""layer {
  name: "%s"
  type: "Pooling"
  bottom: "%s"
  top: "%s"
  pooling_param {
    pool: %s
    kernel_size: %d
    stride: %d
  }
}""" % (name, _bottom, name, _type, kernel, stride))
        self.last = name
      
    def fc(self, name, output,bottom=None):
        _bottom=self.last
        if bottom is not None:
            _bottom=bottom
        print(
"""layer {
  name: "%s"
  type: "InnerProduct"
  bottom: "%s"
  top: "%s"
  param { lr_mult: 1  decay_mult: 1 }
  param { lr_mult: 2  decay_mult: 0 }
  inner_product_param {
    num_output: %d
    weight_filler { type: "msra" }
    bias_filler { type: "constant"  value: 0 }
  }
}""" % (name, _bottom, name, output))
        self.last = name
    
    def reshape(self, name, output,bottom=None):
        _bottom=self.last
        if bottom is not None:
            _bottom=bottom
        print(
"""layer {
    name: "%s"
    type: "Reshape"
    bottom: "%s"
    top: "%s"
    reshape_param { shape { dim: -1 dim: %s dim: 1 dim: 1 } }
}""" % ( name, _bottom, name, output))
        self.last = name
    def conv_block(self,name,num,kernel,stride,group=1,prelu_have=True,bottom=None,pad=None):
        self.conv(name=name+"_conv2d", out=num, kernel=kernel, stride=stride,group=group,bottom=bottom,pad=pad)
        self.bn(name=name+"_batchnorm")
        if prelu_have:
          self.prelu(name=name+"_relu")
    def conv_res_block(self,name,input_num,bottom=None):
        last_bottom = self.last
        if bottom != None:
            last_bottom=bottom
        self.conv_block(name=name+"_conv_sep", num=input_num*2, kernel=1, stride=1,group=1,bottom=last_bottom)
        self.conv_block(name=name+"_conv_dw", num=input_num*2, kernel=3, stride=1,group=input_num*2)
        self.conv_block(name=name+"_conv_proj", num=input_num, kernel=1, stride=1,group=1,prelu_have=False)
        self.shortcut(name=name+"_plus",bottom1=self.last, bottom2=last_bottom)
        
    def generate(self):
        lmdb=FLAGS.lmdb
        stage=FLAGS.stage #'The stage of prototxt, train|test|deploy.'
        nobn=FLAGS.nobn #'for deploy, generate a deploy.prototxt without batchnorm and scale'
        eps=0.00001 #'eps parameter of BatchNorm layers, default is 1e-5'
        input_height=112
        input_width=112
        self.lmdb=lmdb
        if lmdb == "":
          if stage == "train":
              self.lmdb = "trainval_lmdb"
        self.stage = stage
        self.nobn = nobn
        self.eps = eps
        self.header("fastnet")
        if self.stage == "train":
          assert(self.lmdb is not None)
          self.data_classifier(batch_size=32,lmdb_path=self.lmdb)
        else:
          self.data_deploy(input_height,input_width)
        
        self.conv_block(name='conv_1',num=64,kernel=3,stride=2)#56
        self.conv_block(name='conv_2_dw',num=64,kernel=3,stride=1,group=64)
        self.conv_block(name='dconv_23_conv_sep',num=128,kernel=1,stride=1)
        self.conv_block(name='dconv_23_conv_dw',num=128,kernel=3,stride=2,group=128)#28
        self.conv_block(name='dconv_23_conv_proj',num=64,kernel=1,stride=1,prelu_have=False)
        
        for i in range(4):
            self.conv_res_block(name='res_3_block%d'%i,input_num=64)
        
        self.conv_block(name='dconv_34_conv_sep',num=256,kernel=1,stride=1)
        self.conv_block(name='dconv_34_conv_dw',num=256,kernel=3,stride=2,group=256)#14
        self.conv_block(name='dconv_34_conv_proj',num=128,kernel=1,stride=1,prelu_have=False)
        
        for i in range(6):
            self.conv_res_block(name='res_4_block%d'%i,input_num=128)
        
        self.conv_block(name='dconv_45_conv_sep',num=512,kernel=1,stride=1)
        self.conv_block(name='dconv_45_conv_dw',num=512,kernel=3,stride=2,group=512)#7
        self.conv_block(name='dconv_45_conv_proj',num=128,kernel=1,stride=1,prelu_have=False)
        
        self.conv_res_block(name='res_5_block0',input_num=128)
        self.conv_res_block(name='res_5_block1',input_num=128)
        
        
        self.conv_block(name='conv_6sep',num=512,kernel=1,stride=1)
        self.conv_block(name='conv_6dw7_7',num=512,kernel=7,stride=1,pad=0,group=512,prelu_have=False)#1
        
        self.fc(name='pre_fc1', output=128)
        self.bn(name='fc1')#top=bottom=name
        self.fc(name='fc2', output=2)
        self.classifier_loss(self.stage)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-s','--stage',
      type=str,
      default='train',
      help='The stage of prototxt, train|deploy.'
  )
  parser.add_argument(
      '-n','--nobn',
      action='store_true',
      help='for deploy, generate a deploy.prototxt without batchnorm and scale.'
  )
  parser.add_argument(
      '-lmdb','-l',
      type=str,
      default='train_lmdb',
      help='lmdb path'
  )
  FLAGS, unparsed = parser.parse_known_args()
  gen = Generator()
  gen.generate()
