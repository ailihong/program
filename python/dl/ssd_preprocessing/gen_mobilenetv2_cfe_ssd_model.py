'''
python3
v0.2
'''
import argparse
FLAGS = None

def create_ssd_anchors(num_layers=6,
                       min_scale=0.2,
                       max_scale=0.95):

  scales = [min_scale + (max_scale - min_scale) * i / (num_layers - 1)
            for i in range(num_layers)] + [1.0]
  return zip(scales[:-1], scales[1:])
  
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
    conf_loss_type: LOGISTIC
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
    def rect_conv(self, name, out, kernel_h,kernel_w,pad_w=0,pad_h=0, stride=1, group=1, bias=False, bottom=None):

      if self.stage == "deploy" and self.nobn: #for deploy, merge bn to bias, so bias must be true
          bias = True

      if bottom is None:
          bottom = self.last
      padstr = ""
      padstr = "\n    pad_w: %d\n    pad_h: %d" % (pad_w,pad_h)
      kernel_str = ""
      kernel_str = "\n    kernel_w: %d\n    kernel_h: %d" % (kernel_w,kernel_h)
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
    num_output: %d%s%s%s%s
    weight_filler {
      type: "msra"
    }%s
  }
}""" % (name, bottom, name, bias_lr_mult, out, biasstr, padstr, kernel_str, stridestr, bias_filler))
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
      self.last = name
    def Up(self, name,outp,bottom=None):
      
      if bottom is not None:
          self.last=bottom
      
      print(
"""layer {
  name: "%s"
  type: "Deconvolution"
  bottom: "%s"
  top: "%s"
  param {
    lr_mult: 1
  }
  convolution_param {
    num_output: %d
    kernel_size: 4
    stride: 2
    pad: 1
    weight_filler: { type: "bilinear" }
  }
}""" % (name, self.last, name,outp))
      self.last = name
    
    def conv_act(self, name, out, kernel, stride=1, group=1, bias=False, bottom=None):
        self.conv(name, out, kernel, stride, group, bias, bottom)
        self.relu(name)
    def conv_bn_relu(self, name, num, kernel, stride=1,bottom=None,pad=None):
      self.conv(name, num, kernel, stride,bottom=bottom,pad=pad)
      self.bn(name)
      self.relu(name)
    def conv_bn_relu_with_factor(self, name, outp, kernel, stride,bottom=None):
      outp = int(outp * self.size)
      self.conv(name, outp, kernel, stride,bottom=bottom)
      self.bn(name)
      self.relu(name)
    def rect_conv_bn_relu_with_factor(self, name, outp, kernel_h,kernel_w, pad_w=0,pad_h=0,stride=1,bottom=None):
      outp = int(outp * self.size)
      self.rect_conv(name=name, out=outp, kernel_h=kernel_h,kernel_w=kernel_w, pad_w=pad_w,pad_h=pad_h,stride=stride,bottom=bottom)
      self.bn(name)
      self.relu(name)
    def conv_ssd(self, name, stage, inp, outp,bottom=None):
      stage = str(stage)
      self.conv_expand(name + '_1_' + stage, inp, int(outp / 2), bottom=bottom)
      self.conv_depthwise(name + '_2_' + stage + '/depthwise', int(outp / 2),kernel=3,stride= 2)
      self.conv_expand(name + '_2_' + stage, int(outp / 2), outp)
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
    def conv_cfe_block(self, name, inp, bottom=None):
      if bottom is not None:
          self.last=bottom
      self.conv_bn_relu_with_factor(name=name+'/branch1/1', outp=int(inp/2), kernel=1, stride=1,bottom=bottom)
      self.rect_conv_bn_relu_with_factor(name=name+'/branch1/2', outp=int(inp/2), kernel_h=1,kernel_w=5, pad_w=2,pad_h=0,stride=1)
      self.rect_conv_bn_relu_with_factor(name=name+'/branch1/3', outp=int(inp/2), kernel_h=5,kernel_w=1, pad_w=0,pad_h=2,stride=1)
      self.conv_bn_relu_with_factor(name=name+'/branch1/4', outp=int(inp/2), kernel=1, stride=1)
      
      self.conv_bn_relu_with_factor(name=name+'/branch2/1', outp=int(inp/2), kernel=1, stride=1,bottom=bottom)
      self.rect_conv_bn_relu_with_factor(name=name+'/branch2/2', outp=int(inp/2), kernel_h=5,kernel_w=1, pad_w=0,pad_h=2,stride=1)
      self.rect_conv_bn_relu_with_factor(name=name+'/branch2/3', outp=int(inp/2), kernel_h=1,kernel_w=5, pad_w=2,pad_h=0,stride=1)
      self.conv_bn_relu_with_factor(name=name+'/branch2/4', outp=int(inp/2), kernel=1, stride=1)
      
      self.concat(name=name+'_cat',bottoms=[name+'/branch1/4',name+'/branch2/4'])
      self.shortcut(name=name,bottom1=bottom)
    def conv_ffb_block(self, name, bottom1,outp1, bottom2,outp2, Up):
        self.conv_bn_relu_with_factor(name=name+'/conv1', outp=outp1, kernel=1, stride=1,bottom=bottom1)
        self.conv_bn_relu_with_factor(name=name+'/conv2', outp=outp2, kernel=1, stride=1,bottom=bottom2)
        if Up:
            self.Up(name=name+'/Up',outp=outp2)
            self.concat(name=name+'_cat',bottoms=[name+'/conv1',name+'/Up'])
        else:
            self.concat(name=name+'_cat',bottoms=[name+'/conv1',name+'/conv2'])
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
    
    def shortcut(self, name,bottom1, bottom2=None):
      _bottom=self.last
      if bottom2 is not None:
        _bottom=bottom2
      print(
"""layer {
  name: "%s/sum"
  type: "Eltwise"
  bottom: "%s"
  bottom: "%s"
  top: "%s/sum"
}""" % (name, bottom1, _bottom, name))
      self.last = name+'/sum'
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
    def mbox_prior(self, name, min_size, max_size, aspect_ratio):
        min_box = self.input_size * min_size
        max_box_str = ""
        aspect_ratio_str = ""
        if max_size is not None:
            max_box = self.input_size * max_size
            max_box_str = "\n    max_size: %.1f" % max_box
        for ar in aspect_ratio:
            aspect_ratio_str += "\n    aspect_ratio: %.1f" % ar
      
        print(
"""layer {
  name: "%s_mbox_priorbox"
  type: "PriorBox"
  bottom: "%s"
  bottom: "data"
  top: "%s_mbox_priorbox"
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
}"""% (name, name, name, float(min_box), max_box_str, aspect_ratio_str))
    def mbox_conf(self, bottom, num):
       name = bottom + "_mbox_conf"
       self.conv(name, num, 3, bias=True, bottom=bottom)
       self.permute(name)
       self.flatten(name)
    def mbox_loc(self, bottom, num):
       name = bottom + "_mbox_loc"
       self.conv(name, num, 3, bias=True, bottom=bottom)
       self.permute(name)
       self.flatten(name)
    def mbox(self, bottom, anchors_num):
       self.mbox_loc(bottom, anchors_num * 4)
       self.mbox_conf(bottom, anchors_num * self.class_num)
       min_size, max_size = self.anchors[0]
       if self.first_prior:
           self.mbox_prior(bottom, min_size, max_size, [2.0,3.0])
           self.first_prior = False
       else:
           self.mbox_prior(bottom, min_size, max_size,[2.0,3.0])
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
        self.input_height=300
        self.input_width=300
        self.input_size = 300
        self.size=1.0
        if self.lmdb == "":
          if stage == "train":
              self.lmdb = "trainval_lmdb"
          elif stage == "test":
              self.lmdb = "test_lmdb"
        self.stage = stage
        self.nobn = nobn
        self.eps = eps
        self.header("mobilenetv2-ssd")
        if self.stage == "train":
          assert(self.lmdb is not None)
          self.data_train_ssd()
        elif self.stage == "test":
          self.data_test_ssd()
        else:
          self.data_deploy()
        
        self.conv_bn_relu_with_factor(name="Conv", outp=32, kernel=3, stride=2)
        self.conv_depthwise(name="conv/depthwise", inp=32, stride=1)
        self.conv_project(name="conv/project", outp=16)
        self.conv_block(name="conv_1", inp=16,  expand_factor=6, outp=24, stride=2, shortcut=False)
        self.conv_block(name="conv_2", inp=24,  expand_factor=6, outp=24, stride=1, shortcut=True)
        self.conv_block(name="conv_3", inp=24,  expand_factor=6, outp=32, stride=2, shortcut=False)
        self.conv_block(name="conv_4", inp=32,  expand_factor=6, outp=32, stride=1, shortcut=True)
        self.conv_block(name="conv_5", inp=32,  expand_factor=6, outp=32, stride=1, shortcut=True)
        
        self.conv_cfe_block(name='CFE1', inp=32, bottom='conv_5/sum')
        
        self.conv_block(name="conv_6", inp=32,  expand_factor=6, outp=64, stride=2, shortcut=False)
        self.conv_block(name="conv_7", inp=64,  expand_factor=6, outp=64, stride=1, shortcut=True)
        self.conv_block(name="conv_8", inp=64,  expand_factor=6, outp=64, stride=1, shortcut=True)
        self.conv_block(name="conv_9", inp=64,  expand_factor=6, outp=64, stride=1, shortcut=True)
        
        self.conv_cfe_block(name='CFE2', inp=64, bottom='conv_9/sum')
        
        self.conv_block(name="conv_10",inp=64,  expand_factor=6, outp=96, stride=1, shortcut=False)
        self.conv_block(name="conv_11", inp=96,  expand_factor=6, outp=96, stride=1, shortcut=True)
        self.conv_block(name="conv_12", inp=96,  expand_factor=6, outp=96, stride=1, shortcut=True)
        self.conv_block(name="conv_13", inp=96,  expand_factor=6, outp=160, stride=2, shortcut=False)
        self.conv_block(name="conv_14", inp=160,  expand_factor=6, outp=160, stride=1, shortcut=True)
        self.conv_block(name="conv_15", inp=160,  expand_factor=6, outp=160, stride=1, shortcut=True)
        self.conv_block(name="conv_16", inp=160,  expand_factor=6, outp=320, stride=1, shortcut=False)
        self.conv_bn_relu_with_factor(name="Conv_1", outp=1280, kernel=1, stride=1)
        
        ###-----------------feature--start---------------------------
        self.conv_ssd(name="layer_19", stage=2, inp=1280, outp=512)
        self.conv_ssd(name="layer_19", stage=3, inp=512, outp=256)
        self.conv_ssd(name="layer_19", stage=4, inp=256, outp=256)
        self.conv_ssd(name="layer_19", stage=5, inp=256, outp=128)
        self.conv_ffb_block(name='FFB1', bottom1='conv_5/sum',outp1=32, bottom2='conv_9/sum',outp2=48, Up=True)
        self.conv_ffb_block(name='FFB2', bottom1='conv_9/sum',outp1=48, bottom2='conv_12/sum',outp2=64, Up=False)
        self.conv_cfe_block(name='CFE3', inp=80, bottom='FFB1_cat')
        self.conv_cfe_block(name='CFE4', inp=112, bottom='FFB2_cat')
        ###-----------------feature--end---------------------------
        
        ###-----------------ssd--start---------------------------
        self.mbox(bottom="CFE3/sum", anchors_num=6)
        self.mbox(bottom="CFE4/sum", anchors_num=6)
        self.mbox(bottom="Conv_1", anchors_num=6)
        self.mbox(bottom="layer_19_2_2", anchors_num=6)
        self.mbox(bottom="layer_19_2_3", anchors_num=6)
        self.mbox(bottom="layer_19_2_5", anchors_num=6)
        self.concat_boxes(['CFE3/sum', 'CFE4/sum', 'Conv_1', 'layer_19_2_2', 'layer_19_2_3', 'layer_19_2_5'])
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
