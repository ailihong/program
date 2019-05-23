//
// This script converts selfdefine data to the leveldb format used
// by caffe to train siamese network.
// This file should be caffe/examples/siamese/,after compile bin file in caffe/build/example/siamese/
// edit by baijun in 2019.05.23
#include <fstream>  // NOLINT(readability/streams)
#include <string>
#include <vector>

#include "glog/logging.h"
#include "google/protobuf/text_format.h"
#include "stdint.h"

#include "caffe/proto/caffe.pb.h"
#include "caffe/util/format.hpp"
#include "caffe/util/math_functions.hpp"
#define USE_LEVELDB
#ifdef USE_LEVELDB
#include "leveldb/db.h"

#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
void SplitString(const std::string& s, std::vector<std::string>& v, const std::string& c){
  std::string::size_type pos1, pos2;
  pos2 = s.find(c);
  pos1 = 0;
  v.clear();
  while(std::string::npos != pos2)
  {
    v.push_back(s.substr(pos1, pos2-pos1));
 
    pos1 = pos2 + c.size();
    pos2 = s.find(c, pos1);
  }
  if(pos1 != s.length())
    v.push_back(s.substr(pos1));
}
int read_pair_image(string filename1, string filename2,
        uint32_t rows, uint32_t cols,
        char* pixels) {
      int ret = 0;
      cv::Mat image = cv::imread(filename1);
      cv::Mat image2 = cv::imread(filename2);
      do{
          if(rows != image.rows || cols != image.cols || rows != image2.rows || cols != image2.cols || image.empty() || image2.empty()){
            ret = 1;
            break;
          }
          uint32_t image_buffer_plane_size = rows * cols;
          //interleave 2 planar
          for(int i=0;i<rows;i++){
              for(int j=0;j<cols;j++){
                  pixels[2*image_buffer_plane_size+i*cols+j]=image.data[(i*cols+j)*3+2];
                  pixels[1*image_buffer_plane_size+i*cols+j]=image.data[(i*cols+j)*3+1];
                  pixels[0*image_buffer_plane_size+i*cols+j]=image.data[(i*cols+j)*3+0];

                  pixels[image_buffer_plane_size*3+2*image_buffer_plane_size+i*cols+j]=image2.data[(i*cols+j)*3+2];
                  pixels[image_buffer_plane_size*3+1*image_buffer_plane_size+i*cols+j]=image2.data[(i*cols+j)*3+1];
                  pixels[image_buffer_plane_size*3+0*image_buffer_plane_size+i*cols+j]=image2.data[(i*cols+j)*3+0];
              }
          }
      }while(0);
      return ret;
}
typedef struct pair_image_t{
    string filename1;
    string filename2;
    int label;
}pair_image;

void convert_dataset(const char* list_filename,
        const char* db_filename) {
  // Open file
  std::ifstream f1(list_filename, std::ios::in);
  vector<pair_image>pairImageList;
  pair_image pairImage;
  string line;
  vector<string>words;
  
  while(getline(f1,line))//without \n
  {
      //printf("str line:%s\n",line.c_str());
      SplitString(line,words," ");
      CHECK_EQ(words.size(), 3) << "pair image size mismatch.";
      pairImage.filename1 = words[0];
      pairImage.filename2 = words[1];
      pairImage.label = atoi(words[2].c_str());
      // printf("read in:%s,%s,%d\n",pairImage.filename1.c_str(),pairImage.filename2.c_str(),pairImage.label);
      pairImageList.push_back(pairImage);
  }
  // Open leveldb
  leveldb::DB* db;
  leveldb::Options options;
  options.create_if_missing = true;
  options.error_if_exists = true;
  leveldb::Status status = leveldb::DB::Open(
      options, db_filename, &db);
  CHECK(status.ok()) << "Failed to open leveldb " << db_filename
      << ". Is it already existing?";

  uint32_t rows=112;
  uint32_t cols=112;

  char* pixels = new char[6 * rows * cols];
  std::string value;

  // Read image
  uint32_t num_items=pairImageList.size();
  
  caffe::Datum datum;
  datum.set_channels(6);  // three channel for each image in the pair
  datum.set_height(rows);
  datum.set_width(cols);
  printf("Total:%d,rows:%d,cols:%d\n",num_items,rows,cols);
  LOG(INFO) << "A total of " << num_items << " items.";
  LOG(INFO) << "Rows: " << rows << " Cols: " << cols;
  int ret=0,badNum=0;
  for (int itemid = 0; itemid < num_items; ++itemid) {
    string filename1 = pairImageList[itemid].filename1;
    string filename2 = pairImageList[itemid].filename2;
    int label = pairImageList[itemid].label;
    ret = read_pair_image(filename1, filename2, rows, cols, pixels);
    if(ret){
      badNum++;
      printf("error in read %s:%s,bad image num:%d\n",filename1,filename2,badNum);
      continue;
    }
    datum.set_data(pixels, 6*rows*cols);
    datum.set_label(label);
    
    datum.SerializeToString(&value);
    std::string key_str = caffe::format_int(itemid, 8);
    db->Put(leveldb::WriteOptions(), key_str, value);
  }

  delete db;
  delete [] pixels;
}

int main(int argc, char** argv) {
  if (argc != 3) {
    printf("This script converts myself dataset to the leveldb format used\n"
           "by caffe to train a siamese network.\n"
           "Usage:\n"
           "    convert_mnist_data_bj input_list_file\n"
           "output_db_file\n"
           "one line in input_list_file should like this:image_path1 image_path2 0/1\n"
           "the image shape is 3,112,112\n"
           );
  } else {
    google::InitGoogleLogging(argv[0]);
    convert_dataset(argv[1], argv[2]);
  }
  return 0;
}
#else
int main(int argc, char** argv) {
  LOG(FATAL) << "This example requires LevelDB; compile with USE_LEVELDB.";
}
#endif  // USE_LEVELDB
