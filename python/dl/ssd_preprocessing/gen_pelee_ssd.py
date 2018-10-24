'''
python3
v0.2
'''
import argparse,math
FLAGS = None

def create_ssd_anchors(input_size=304,num_layers=6,
                       min_scale=0.2,
                       max_scale=0.9):
    min_dim=input_size
    min_ratio = int(min_scale*100)
    max_ratio = int(max_scale*100)
    step = int(math.floor((max_ratio - min_ratio) / (num_layers - 2)))
    min_sizes = []
    max_sizes = []
    for ratio in range(min_ratio, max_ratio + 1, step):
      min_sizes.append(min_dim * ratio / 100.)
      max_sizes.append(min_dim * (ratio + step) / 100.)
    min_sizes = [min_dim * 10 / 100.] + min_sizes
    max_sizes = [min_dim * 20 / 100.] + max_sizes
    return zip(min_sizes, max_sizes)
  
class Generator():

    def __init__(self):
      self.first_prior = True
      self.anchors = list(create_ssd_anchors())
      
      self.last = "data"
    def header(self, name):
      print("name: \"%s\"" % name)
    
    def data_deploy(self):
      print(
"""input: "data"
input_shape {
  dim: 1
  dim: 3
  dim: %d
  dim: %d
}""" % (self.input_height, self.input_width))
    def data_train_ssd(self):
      print(
"""layer {
  name: "data"
  type: "AnnotatedData"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  transform_param {
    scale: 0.007843
    mirror: true
    mean_value: 127.5
    mean_value: 127.5
    mean_value: 127.5
    resize_param {
      prob: 1.0
      resize_mode: WARP
      height: %d
      width: %d
      interp_mode: LINEAR
      interp_mode: AREA
      interp_mode: NEAREST
      interp_mode: CUBIC
      interp_mode: LANCZOS4
    }
    emit_constraint {
      emit_type: CENTER
    }
    distort_param {
      brightness_prob: 0.5
      brightness_delta: 32.0
      contrast_prob: 0.5
      contrast_lower: 0.5
      contrast_upper: 1.5
      hue_prob: 0.5
      hue_delta: 18.0
      saturation_prob: 0.5
      saturation_lower: 0.5
      saturation_upper: 1.5
      random_order_prob: 0.0
    }
    expand_param {
      prob: 0.5
      max_expand_ratio: 4.0
    }
  }
  data_param {
    source: "%s"
    batch_size: 24
    backend: LMDB
  }
  annotated_data_param {
    batch_sampler {
      max_sample: 1
      max_trials: 1
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        min_jaccard_overlap: 0.1
      }
      max_sample: 1
      max_trials: 50
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        min_jaccard_overlap: 0.3
      }
      max_sample: 1
      max_trials: 50
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        min_jaccard_overlap: 0.5
      }
      max_sample: 1
      max_trials: 50
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        min_jaccard_overlap: 0.7
      }
      max_sample: 1
      max_trials: 50
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        min_jaccard_overlap: 0.9
      }
      max_sample: 1
      max_trials: 50
    }
    batch_sampler {
      sampler {
        min_scale: 0.3
        max_scale: 1.0
        min_aspect_ratio: 0.5
        max_aspect_ratio: 2.0
      }
      sample_constraint {
        max_jaccard_overlap: 1.0
      }
      max_sample: 1
      max_trials: 50
    }
    label_map_file: "%s"
  }
}"""  % (self.input_height,self.input_width, self.lmdb,  self.label_map))
    
    def data_test_ssd(self):
      print(
"""layer {
  name: "data"
  type: "AnnotatedData"
  top: "data"
  top: "label"
  include {
    phase: TEST
  }
  transform_param {
    scale: 0.007843
    mean_value: 127.5
    mean_value: 127.5
    mean_value: 127.5
    resize_param {
      prob: 1.0
      resize_mode: WARP
      height: %d
      width: %d
      interp_mode: LINEAR
    }
  }
  data_param {
    source: "%s"
    batch_size: 8
    backend: LMDB
  }
  annotated_data_param {
    batch_sampler {
    }
    label_map_file: "%s"
  }
}""" %  (self.input_height, self.input_width, self.lmdb,  self.label_map))
    def ssd_predict(self):
      print(
"""layer {
  name: "mbox_conf_reshape"
  type: "Reshape"
  bottom: "mbox_conf"
  top: "mbox_conf_reshape"
  reshape_param {
    shape {
      dim: 0
      dim: -1
      dim: %d
    }
  }
}
layer {
  name: "mbox_conf_sigmoid"
  type: "Sigmoid"
  bottom: "mbox_conf_reshape"
  top: "mbox_conf_sigmoid"
}
layer {
  name: "mbox_conf_flatten"
  type: "Flatten"
  bottom: "mbox_conf_sigmoid"
  top: "mbox_conf_flatten"
  flatten_param {
    axis: 1
  }
}
layer {
  name: "detection_out"
  type: "DetectionOutput"
  bottom: "mbox_loc"
  bottom: "mbox_conf_flatten"
  bottom: "mbox_priorbox"
  top: "detection_out"
  include {
    phase: TEST
  }
  detection_output_param {
    num_classes: %d
    share_location: true
    background_label_id: 0
    nms_param {
      nms_threshold: 0.45
      top_k: 100
    }
    code_type: CENTER_SIZE
    keep_top_k: 100
    confidence_threshold: 0.35
  }
}""" % (self.class_num, self.class_num))
    
    def ssd_test(self):
      print(
"""layer {
  name: "mbox_conf_reshape"
  type: "Reshape"
  bottom: "mbox_conf"
  top: "mbox_conf_reshape"
  reshape_param {
    shape {
      dim: 0
      dim: -1
      dim: %d
    }
  }
}
layer {
  name: "mbox_conf_sigmoid"
  type: "Sigmoid"
  bottom: "mbox_conf_reshape"
  top: "mbox_conf_sigmoid"
}
layer {
  name: "mbox_conf_flatten"
  type: "Flatten"
  bottom: "mbox_conf_sigmoid"
  top: "mbox_conf_flatten"
  flatten_param {
    axis: 1
  }
}
layer {
  name: "detection_out"
  type: "DetectionOutput"
  bottom: "mbox_loc"
  bottom: "mbox_conf_flatten"
  bottom: "mbox_priorbox"
  top: "detection_out"
  include {
    phase: TEST
  }
  detection_output_param {
    num_classes: %d
    share_location: true
    background_label_id: 0
    nms_param {
      nms_threshold: 0.45
      top_k: 400
    }
    code_type: CENTER_SIZE
    keep_top_k: 200
    confidence_threshold: 0.01
  }
}
layer {
  name: "detection_eval"
  type: "DetectionEvaluate"
  bottom: "detection_out"
  bottom: "label"
  top: "detection_eval"
  include {
    phase: TEST
  }
  detection_evaluate_param {
    num_classes: %d
    background_label_id: 0
    overlap_threshold: 0.5
    evaluate_difficult_gt: false
  }
}""" % (self.class_num, self.class_num, self.class_num))
    def ssd_loss(self):
      print(
"""layer {
  name: "mbox_loss"
  type: "MultiBoxLoss"
  bottom: "mbox_loc"
  bottom: "mbox_conf"
  bottom: "mbox_priorbox"
  bottom: "label"
  top: "mbox_loss"
  include {
    phase: TRAIN
  }
  propagate_down: true
  propagate_down: true
  propagate_down: false
  propagate_down: false
  loss_param {
    normalization: VALID
  }
  multibox_loss_param {
    loc_loss_type: SMOOTH_L1
    conf_loss_type: SOFTMAX
    loc_weight: 1.0
    num_classes: %d
    share_location: true
    match_type: PER_PREDICTION
    overlap_threshold: 0.5
    use_prior_for_matching: true
    background_label_id: 0
    use_difficult_gt: true
    neg_pos_ratio: 3.0
    neg_overlap: 0.5
    code_type: CENTER_SIZE
    ignore_cross_boundary_bbox: false
    mining_type: MAX_NEGATIVE
  }
}""" % self.class_num)
    def concat(self, name,bottoms):
        bottom_str =""
        for bottom in bottoms:
          bottom_str += "\n  bottom: \"%s\"" % (bottom)
        print(
"""layer {
  name: "%s"
  type: "Concat"%s
  top: "%s"
  concat_param {
    axis: 1
  }
}""" % (name, bottom_str, name))
        self.last = name
    def concat_boxes(self, convs):
      for layer in ["loc", "conf"]:
        bottom =""
        for cnv in convs:
          bottom += "\n  bottom: \"%s_mbox_%s_flat\"" % (cnv, layer)
        print(
"""layer {
  name: "mbox_%s"
  type: "Concat"%s
  top: "mbox_%s"
  concat_param {
    axis: 1
  }
}""" % (layer, bottom, layer))

      bottom =""
      for cnv in convs:
        bottom += "\n  bottom: \"%s_mbox_priorbox\"" % cnv
      print(
"""layer {
  name: "mbox_priorbox"
  type: "Concat"%s
  top: "mbox_priorbox"
  concat_param {
    axis: 2
  }
}""" % bottom)
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
      eps_str = "\n  batch_norm_param {\n    eps: %f\n  }"%self.eps
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
    def conv_bn(self, name, num, kernel, stride=1,bottom=None,pad=None):
      num = int(num * self.size)
      self.conv(name, num, kernel, stride,bottom=bottom,pad=pad)
      self.bn(name)
    def conv_bn_relu_with_factor(self, name, outp, kernel, stride,bottom=None):
      outp = int(outp * self.size)
      self.conv(name, outp, kernel, stride,bottom=bottom)
      self.bn(name)
      self.relu(name)
    def conv_ssd(self, name, stage, inp, outp,bottom=None):
      stage = str(stage)
      self.conv_expand(name + '_1_' + stage, inp, int(outp / 2), bottom=bottom)
      self.conv_depthwise(name + '_2_' + stage + '/depthwise', int(outp / 2),kernel=3,stride= 2)
      self.conv_expand(name + '_2_' + stage, int(outp / 2), outp)
    def conv_pelee_block(self, name, outp,expand_factor,bottom):
        self.conv_bn_relu_with_factor(name="%s/branch2a"%name, outp=outp, kernel=1, stride=1,bottom=bottom)
        self.conv_bn_relu_with_factor(name="%s/branch2b"%name, outp=int(outp*expand_factor), kernel=3, stride=1)
        self.conv_bn_relu_with_factor(name="%s/branch2c"%name, outp=int(outp*expand_factor), kernel=3, stride=1)
        self.conv_bn_relu_with_factor(name="%s/branch1a"%name, outp=outp, kernel=1, stride=1,bottom=bottom)
        self.conv_bn_relu_with_factor(name="%s/branch1b"%name, outp=int(outp*expand_factor), kernel=3, stride=1)
        self.concat(name='%s/concat'%name,bottoms=[bottom,'%s/branch2c'%name,'%s/branch1b'%name])
    def conv_block(self, name, inp, expand_factor, outp, stride, shortcut,bottom=None):
      if bottom is not None:
          self.last=bottom
      last_block = self.last
      t=expand_factor
      
      self.conv_expand(name + '/expand', inp, t * inp)
      
      self.conv_depthwise(name + '/depthwise', t * inp, kernel=3,stride=stride)
      
      if shortcut:
         self.conv_project(name + '/project', outp)
         self.shortcut(name=name,bottom1=last_block)
      else:
         self.conv_project(name + '/project', outp)
      
    def conv_depthwise(self, name, inp, kernel=3,stride=1,bottom=None):
      inp = int(inp * self.size)
      self.conv(name, inp, kernel, stride, group=inp,bottom=bottom)
      self.bn(name)
      self.relu(name)

    def conv_expand(self, name, inp, outp,bottom=None):
      inp = int(inp * self.size)
      outp = int(outp * self.size)
      self.conv(name, outp, 1,bottom=bottom)
      self.bn(name)
      self.relu(name)

    def conv_project(self, name, outp,bottom=None):
      outp = int(outp * self.size)
      self.conv(name, outp, 1,bottom=bottom)
      self.bn(name)

    def conv_dw_pw(self, name, inp, outp, stride=1,bottom=None):
      inp = int(inp * self.size)
      outp = int(outp * self.size)
      name1 = name + "/depthwise"
      self.conv(name1, inp, 3, stride, group=inp,bottom=bottom)
      self.bn(name1)
      self.relu(name1)
      name2 = name 
      self.conv(name2, outp, 1)
      self.bn(name2)
      self.relu(name2)
    def shortcut_relu(self, name,bottom1, bottom2=None):
      _bottom=self.last
      if bottom2 is not None:
        _bottom=bottom2
      print(
"""layer {
  name: "%s"
  type: "Eltwise"
  bottom: "%s"
  bottom: "%s"
  top: "%s"
}
layer {
  name: "%s/relu"
  type: "%s"
  bottom: "%s"
  top: "%s"
}
""" % (name, bottom1, _bottom, name,name,'Relu',name,name))
      self.last = name
    def shortcut(self, name,bottom1, bottom2=None):
      _bottom=self.last
      if bottom2 is not None:
        _bottom=bottom2
      print(
"""layer {
  name: "%s"
  type: "Eltwise"
  bottom: "%s"
  bottom: "%s"
  top: "%s"
}""" % (name, bottom1, _bottom, name))
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
    def permute(self, name):
        print(
"""layer {
  name: "%s_perm"
  type: "Permute"
  bottom: "%s"
  top: "%s_perm"
  permute_param {
    order: 0
    order: 2
    order: 3
    order: 1
  }
}""" % (name, name, name))
        self.last = name + "_perm"
    def flatten(self, name):
        print(
"""layer {
  name: "%s_flat"
  type: "Flatten"
  bottom: "%s_perm"
  top: "%s_flat"
  flatten_param {
    axis: 1
  }
}""" % (name, name, name))
        self.last = name + "_flat"
    def mbox_prior(self, name, bottom,min_size, max_size, aspect_ratio):
        min_box = min_size
        max_box_str = ""
        aspect_ratio_str = ""
        if max_size is not None:
            max_box = max_size
            max_box_str = "\n    max_size: %.1f" % max_box
        for ar in aspect_ratio:
            aspect_ratio_str += "\n    aspect_ratio: %.1f" % ar
      
        print(
"""layer {
  name: "%s"
  type: "PriorBox"
  bottom: "%s"
  bottom: "data"
  top: "%s"
  prior_box_param {
    min_size: %.1f%s%s
    flip: true
    clip: false
    variance: 0.1
    variance: 0.1
    variance: 0.2
    variance: 0.2
    offset: 0.5
  }
}"""% (name, bottom, name, float(min_box), max_box_str, aspect_ratio_str))
    def mbox_conf(self,name, bottom, num):
       self.conv(name, num, 3, bias=True, bottom=bottom)
       self.permute(name)
       self.flatten(name)
    def mbox_loc(self, name,bottom, num):
       self.conv(name, num, 3, bias=True, bottom=bottom)
       self.permute(name)
       self.flatten(name)
    def mbox(self, name,bottom, anchors_num):
       self.mbox_loc(name+'_mbox_loc',bottom, anchors_num * 4)
       self.mbox_conf(name+'_mbox_conf',bottom, anchors_num * self.class_num)
       min_size, max_size = self.anchors[0]
       if self.first_prior:
           self.mbox_prior(name+'_mbox_priorbox',bottom, min_size, max_size, [2.0,3.0])
           self.first_prior = False
       else:
           self.mbox_prior(name+'_mbox_priorbox',bottom, min_size, max_size,[2.0,3.0])
       self.anchors.pop(0)
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
        self.lmdb=FLAGS.lmdb
        self.class_num = FLAGS.class_num
        self.label_map = 'label_map.prototxt'
        stage=FLAGS.stage #'The stage of prototxt, train|test|deploy.'
        nobn=FLAGS.nobn #'for deploy, generate a deploy.prototxt without batchnorm and scale'
        eps=0.001
        self.input_height=304
        self.input_width=304
        self.input_size = 304
        self.size=1.0
        if self.lmdb == "":
          if stage == "train":
              self.lmdb = "trainval_lmdb"
          elif stage == "test":
              self.lmdb = "test_lmdb"
        self.stage = stage
        self.nobn = nobn
        self.eps = eps
        self.header("pelee-ssd")
        if self.stage == "train":
          assert(self.lmdb is not None)
          self.data_train_ssd()
        elif self.stage == "test":
          self.data_test_ssd()
        else:
          self.data_deploy()
        
        self.conv_bn_relu_with_factor(name="stem1", outp=32, kernel=3, stride=2)
        self.pool(name='stem/pool',_type='MAX',kernel=2,stride=2)       
        self.conv_bn_relu_with_factor(name="stem2a", outp=16, kernel=1, stride=1,bottom="stem1")
        self.conv_bn_relu_with_factor(name="stem2b", outp=32, kernel=3, stride=2)
        self.concat(name='stem/concat',bottoms=['stem/pool','stem2b'])
        
        self.conv_bn_relu_with_factor(name="stem3", outp=32, kernel=1, stride=1)
        self.conv_pelee_block(name='stage1_1', outp=16,expand_factor=1.0,bottom='stem3')
        self.conv_pelee_block(name='stage1_2', outp=16,expand_factor=1.0,bottom='stage1_1/concat')
        self.conv_pelee_block(name='stage1_3', outp=16,expand_factor=1.0,bottom='stage1_2/concat')
        
        self.conv_bn_relu_with_factor(name="stage1_tb", outp=128, kernel=1, stride=1)
        self.pool(name='stage1_tb/pool',_type='AVE',kernel=2,stride=2)
        
        self.conv_pelee_block(name='stage2_1', outp=32,expand_factor=0.5,bottom='stage1_tb/pool')
        self.conv_pelee_block(name='stage2_2', outp=32,expand_factor=0.5,bottom='stage2_1/concat')
        self.conv_pelee_block(name='stage2_3', outp=32,expand_factor=0.5,bottom='stage2_2/concat')
        self.conv_pelee_block(name='stage2_4', outp=32,expand_factor=0.5,bottom='stage2_3/concat')
        
        self.conv_bn_relu_with_factor(name="stage2_tb", outp=256, kernel=1, stride=1)
        self.pool(name='stage2_tb/pool',_type='AVE',kernel=2,stride=2)
        
        self.conv_pelee_block(name='stage3_1', outp=64,expand_factor=0.25,bottom='stage2_tb/pool')
        self.conv_pelee_block(name='stage3_2', outp=64,expand_factor=0.25,bottom='stage3_1/concat')
        self.conv_pelee_block(name='stage3_3', outp=64,expand_factor=0.25,bottom='stage3_2/concat')
        self.conv_pelee_block(name='stage3_4', outp=64,expand_factor=0.25,bottom='stage3_3/concat')
        self.conv_pelee_block(name='stage3_5', outp=64,expand_factor=0.25,bottom='stage3_4/concat')
        self.conv_pelee_block(name='stage3_6', outp=64,expand_factor=0.25,bottom='stage3_5/concat')
        self.conv_pelee_block(name='stage3_7', outp=64,expand_factor=0.25,bottom='stage3_6/concat')
        self.conv_pelee_block(name='stage3_8', outp=64,expand_factor=0.25,bottom='stage3_7/concat')
        
        self.conv_bn_relu_with_factor(name="stage3_tb", outp=512, kernel=1, stride=1)
        self.pool(name='stage3_tb/pool',_type='AVE',kernel=2,stride=2)
        
        self.conv_pelee_block(name='stage4_1', outp=64,expand_factor=0.25,bottom='stage3_tb/pool')
        self.conv_pelee_block(name='stage4_2', outp=64,expand_factor=0.25,bottom='stage4_1/concat')
        self.conv_pelee_block(name='stage4_3', outp=64,expand_factor=0.25,bottom='stage4_2/concat')
        self.conv_pelee_block(name='stage4_4', outp=64,expand_factor=0.25,bottom='stage4_3/concat')
        self.conv_pelee_block(name='stage4_5', outp=64,expand_factor=0.25,bottom='stage4_4/concat')
        self.conv_pelee_block(name='stage4_6', outp=64,expand_factor=0.25,bottom='stage4_5/concat')
        
        self.conv_bn_relu_with_factor(name="stage4_tb", outp=704, kernel=1, stride=1)
        
        self.conv_act(name="ext1/fe1_1", out=256, kernel=1, stride=1)
        self.conv_act(name="ext1/fe1_2", out=256, kernel=3, stride=2)
        self.conv_act(name="ext1/fe2_1", out=128, kernel=1, stride=1)
        self.conv_act(name="ext1/fe2_2", out=256, kernel=3, stride=1)
        self.conv_act(name="ext1/fe3_1", out=128, kernel=1, stride=1)
        self.conv_act(name="ext1/fe3_2", out=256, kernel=3, stride=1)
        
        ###-----------------feature--start---------------------------
        self.conv_bn(name="stage4_tb/ext/pm2", num=256, kernel=1, stride=1,bottom='stage3_tb')
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm2/b2a", outp=128, kernel=1, stride=1,bottom='stage3_tb')#feature map 19*19
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm2/b2b", outp=128, kernel=3, stride=1)
        self.conv_bn(name="stage4_tb/ext/pm2/b2c", num=256, kernel=1, stride=1)
        self.shortcut_relu(name='stage4_tb/ext/pm2/res',bottom1='stage4_tb/ext/pm2')
        
        self.conv_bn(name="stage4_tb/ext/pm3", num=256, kernel=1, stride=1,bottom='stage4_tb')
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm3/b2a", outp=128, kernel=1, stride=1,bottom='stage4_tb')#feature map 10*10
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm3/b2b", outp=128, kernel=3, stride=1)
        self.conv_bn(name="stage4_tb/ext/pm3/b2c", num=256, kernel=1, stride=1)
        self.shortcut_relu(name='stage4_tb/ext/pm3/res',bottom1='stage4_tb/ext/pm3')
        
        self.conv_bn(name="stage4_tb/ext/pm4", num=256, kernel=1, stride=1,bottom='ext1/fe1_2')
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm4/b2a", outp=128, kernel=1, stride=1,bottom='ext1/fe1_2')#feature map 5*5
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm4/b2b", outp=128, kernel=3, stride=1)
        self.conv_bn(name="stage4_tb/ext/pm4/b2c", num=256, kernel=1, stride=1)
        self.shortcut_relu(name='stage4_tb/ext/pm4/res',bottom1='stage4_tb/ext/pm4')
        
        self.conv_bn(name="stage4_tb/ext/pm5", num=256, kernel=1, stride=1,bottom='ext1/fe2_2')
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm5/b2a", outp=128, kernel=1, stride=1,bottom='ext1/fe2_2')#feature map 5*5
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm5/b2b", outp=128, kernel=3, stride=1)
        self.conv_bn(name="stage4_tb/ext/pm5/b2c", num=256, kernel=1, stride=1)
        self.shortcut_relu(name='stage4_tb/ext/pm5/res',bottom1='stage4_tb/ext/pm5')
        
        self.conv_bn(name="stage4_tb/ext/pm6", num=256, kernel=1, stride=1,bottom='ext1/fe3_2')
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm6/b2a", outp=128, kernel=1, stride=1,bottom='ext1/fe3_2')#feature map 5*5
        self.conv_bn_relu_with_factor(name="stage4_tb/ext/pm6/b2b", outp=128, kernel=3, stride=1)
        self.conv_bn(name="stage4_tb/ext/pm6/b2c", num=256, kernel=1, stride=1)
        self.shortcut_relu(name='stage4_tb/ext/pm6/res',bottom1='stage4_tb/ext/pm6')
        ###-----------------feature--end---------------------------
        
        ###-----------------ssd--start---------------------------
        self.mbox(name='ext/pm1',bottom="stage4_tb/ext/pm2/res", anchors_num=6)
        self.mbox(name='ext/pm2',bottom="stage4_tb/ext/pm2/res", anchors_num=6)
        self.mbox(name='ext/pm3',bottom="stage4_tb/ext/pm3/res", anchors_num=6)
        self.mbox(name='ext/pm4',bottom="stage4_tb/ext/pm4/res", anchors_num=6)
        self.mbox(name='ext/pm5',bottom="stage4_tb/ext/pm5/res", anchors_num=6)
        self.mbox(name='ext/pm6',bottom="stage4_tb/ext/pm6/res", anchors_num=6)
        
        self.concat_boxes(['ext/pm1', 'ext/pm2', 'ext/pm3', 'ext/pm4', 'ext/pm5', 'ext/pm6'])
        ###-----------------ssd--end---------------------------
        
        if self.stage == "train":
             self.ssd_loss()
        elif self.stage == "deploy":
             self.ssd_predict()
        else:
             self.ssd_test()

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
      default='',
      help='lmdb path'
  )
  parser.add_argument(
      '-class_num','-c',
      type=int,
      default=4,
      help='class num for detect'
  )
  FLAGS, unparsed = parser.parse_known_args()
  gen = Generator()
  gen.generate()
