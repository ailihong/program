//opencv cpp 包含头文件，常见操作
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>

cv::imshow( "Frame", frame );
cv::waitKey(20);//一定要加这个，要不然显示不了

//给mat赋值
cv::Mat frame( mHeight, mWidth, CV_8UC3 );
memcpy( frame.data, map.data, map.size );

//open camera
VideoCapture capture("D:/videos/PetsD2TeC2.avi");  
//检测是否正常打开:成功打开时，isOpened返回ture  
if(!capture.isOpened())  
  cout<<"fail to open!"<<endl;
//读取下一帧  
//cap >> frame; //读取方式二 
if(!capture.read(frame))  
{  
   cout<<"读取视频失败"<<endl;  
}  
          
imshow("frame",frame); 
