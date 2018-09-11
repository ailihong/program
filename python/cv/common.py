img = cv2.imread(fn)
sp = img.shape
sz1 = sp[0]#height(rows) of image
sz2 = sp[1]#width(colums) of image
sz3 = sp[2]#channels
    
Size dsize = Size(width, height);

res=cv2.resize(image,(32,32),interpolation=cv2.INTER_CUBIC)
