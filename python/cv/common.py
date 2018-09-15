img = cv2.imread(fn)
sp = img.shape
sz1 = sp[0]#height(rows) of image
sz2 = sp[1]#width(colums) of image
sz3 = sp[2]#channels
    
Size dsize = Size(width, height);

res=cv2.resize(image,(32,32),interpolation=cv2.INTER_CUBIC)

# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
 
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
 
    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
 
    # 返回旋转后的图像
    return rotated
