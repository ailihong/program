//OpenCV 90°旋转 https://blog.csdn.net/tianzhaixing2013/article/details/53037474
#include <iostream>
#include <string>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

void myRotateClockWise90(Mat &src)
{
    if (src.empty())
    {
        return;
    }
    // 矩阵转置
    transpose(src, src); 
    //0: 沿X轴翻转； >0: 沿Y轴翻转； <0: 沿X轴和Y轴翻转
    flip(src, src, 1);
}

void myRotateAntiClockWise90(Mat &src)
{
    if (src.empty())
    {
        return;
    }
    transpose(src, src);
    flip(src, src, 0);
}
