//opencv cpp 包含头文件，常见操作
#include <opencv2/highgui/highgui.hpp>

cv::imshow( "Frame", frame );
cv::waitKey(20);//一定要加这个，要不然显示不了

//给mat赋值
cv::Mat frame( mHeight, mWidth, CV_8UC3 );
memcpy( frame.data, map.data, map.size );
