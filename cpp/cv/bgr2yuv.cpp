cvtColor(frame, frame_yuv, COLOR_BGR2YUV_I420);            
//imshow("src", frame_yuv);
//waitKey(1);
memcpy(buf, frame_yuv.data, 640*480*1.5);
