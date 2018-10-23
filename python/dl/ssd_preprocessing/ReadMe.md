step 1:
  通过xml文件形成ImageSets/Main/trainval.txt，test.txt，val.tx，运行createTrainAndTest_xml.py。
  
step 2:
  进入caffe-ssd，修改data/VOC0712/create_list.sh文件
  将root_dir改为自己的路径/path/to/your-data，指定数据集位置,实际位置为/path/to/your-data/VOC2007/
  create_list.sh生成的trainval.txt,，test_size_name.txt，test.txt在caffe-ssd/data/VOC0712/中
  
step 3:
  修改data/VOC0712/create_data.sh文件，将data_root_dir改为自己的路径"/path/to/your-data",指定数据集位置
  修改data/VOC0712/labelmap_voc.prototxt
  生成的lmdb文件位置在/path/to/your-data/VOC0712/lmdb/
 
 step 4:
   打链接到自己想要的位置，开始训练
