分类参考

step1:将图片数据分多个文件夹放好

step2:运行list_all.py

step3:split_trainval_txt.py切分

step4:caffe/build/tool/convert_imageset path1 [path2/to]txt path/to/lmdb;path1+path2能找到txt中的图片文件即可

step5:如果需要计算均值的话，执行caffe/build/tool/compute_image_mean path/to/lmdb mean.binaryproto

step6:编写solver.prototxt,设计网络，开始训练
