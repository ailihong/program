img = cv2.imread("models/face1.png")
img_ = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#while True:
cv2.imwrite("test.bmp", img_)
#不管是灰度图还是彩色图，保存为jpg都是三通道的，如果灰度图保存为bmp，则是单通道的
