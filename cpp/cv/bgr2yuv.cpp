cvtColor(frame, frame_yuv, COLOR_BGR2YUV_I420);            
//imshow("src", frame_yuv);
//waitKey(1);
memcpy(buf, frame_yuv.data, 640*480*1.5);

Mat myuv(img->height + img->height / 2, img->width, CV_8UC1, img->img);
cvtColor(myuv, bgr, CV_YUV2BGR_I420, 0);
