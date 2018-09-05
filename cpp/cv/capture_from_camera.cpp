
#include <iostream>
#include <time.h>
#include <string>
#include <vector>
#include <fstream>
extern "C"{
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>
    #include <errno.h>
    #include <dirent.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
}

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std; 
using namespace cv;

int main(int argc, char** argv) 
{   

    VideoCapture cap(0);
    printf("width = %.2f\n",cap.get(CV_CAP_PROP_FRAME_WIDTH));
    printf("height = %.2f\n",cap.get(CV_CAP_PROP_FRAME_HEIGHT));
    int cnt = 0;
    string name;
    char option;
    while(1)
    {
        Mat frame;
        
        cap.read(frame);
        if (frame.empty())
        {
            cout << " image is empty" << endl;
            continue;
        }
        
        imshow("camera", frame);
        option = waitKey(50);
        if(option=='s')
        {
            cnt++;
            name = "baijun_"+to_string(cnt)+".jpg";
            imwrite(name,frame);
        }
        else if(option == 'q')
        {
            break;
        }
    }

    return 0;
    
}
