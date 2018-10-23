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
    
    def data_classifier(self,_type,batch_size,lmdb_path):
        if _type == 'train':
            phase='TRAIN'
        if _type == 'test':
            phase='TEST'
        print(
"""layer {
    name: "data"
    type: "Data"
    top: "data"
    top: "label"
    data_param{
        source: "%s"
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
    include: { phase: %s }
}"""%(lmdb_path,batch_size,phase))

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
}""" % (_bottom))
        if stage == 'test':
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
            print(
"""layer {
  name: "accuracy"
  type: "Accuracy"
  bottom: "prob"
  bottom: "label"
  top: "accuracy"
  include {
    phase: TEST
  }
}""")
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
    
    def bn(self, name):
      if self.stage == "deploy" and self.nobn:  #deploy does not need bn, you can use merge_bn.py to generate a new caffemodel
         return
      eps_str = ""
      if self.eps != 1e-5:
          eps_str = "\n  batch_norm_param {\n    eps: 0.001\n  }"
      print(
"""layer {
  name: "%s/bn"
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
  name: "%s/scale"
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
}""" % (name,name,name,eps_str,name,name,name))
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
      self.last
      self.last = name
    
    def conv_act(self, name, out, kernel, stride=1, group=1, bias=False, bottom=None):
        self.conv(name, out, kernel, stride, group, bias, bottom)
        self.relu(name)
    def conv_bn_relu(self, name, num, kernel, stride=1,bottom=None,pad=None):
      self.conv(name, num, kernel, stride,bottom=bottom,pad=pad)
      self.bn(name)
      self.relu(name)
    
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

    def generate(self):
        lmdb=FLAGS.lmdb
        stage=FLAGS.stage #'The stage of prototxt, train|test|deploy.'
        nobn=FLAGS.nobn #'for deploy, generate a deploy.prototxt without batchnorm and scale'
        eps=0.00001 #'eps parameter of BatchNorm layers, default is 1e-5'
        input_height=100
        input_width=40
        if lmdb == "":
          if stage == "train":
              self.lmdb = "trainval_lmdb"
          elif stage == "test":
              self.lmdb = "test_lmdb"
        self.stage = stage
        self.nobn = nobn
        self.eps = eps
        self.header("none_person")
        if self.stage == "train":
          assert(self.lmdb is not None)
          self.data_classifier(_type='train',batch_size=256,lmdb_path=self.lmdb)
        elif self.stage == "test":
          self.data_classifier(_type='test',batch_size=64,lmdb_path=self.lmdb)
        else:
          self.data_deploy(input_height,input_width)
      
        self.conv_act(name='conv1', out=8, kernel=3,stride=2)
        self.conv_act(name='conv2', out=8, kernel=3)
        
        self.conv_act(name='dp_conv4', out=16,kernel=3)
        self.conv_act(name='dp_conv5', out=32,kernel=3)
        self.pool(name='pool1', _type='MAX', kernel=3, stride=2)
        self.conv_act(name='conv3', out=32, kernel=1,stride=2,bottom='conv2')
        self.shortcut(name='add_1',bottom1='conv3', bottom2='pool1')
        
        self.conv_act(name='conv6', out=8, kernel=3,stride=2)
        self.ave_global_pool(name='pool5')
        self.fc(name='ip1', output=2)
        self.classifier_loss(self.stage)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-s','--stage',
      type=str,
      default='train',
      help='The stage of prototxt, train|test|deploy.'
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
