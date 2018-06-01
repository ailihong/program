#RGB,[high,weight,channels] --> BGR,[channels,high,weight],imagesize(244,244)
def imagePrecess(img):
    img = img[0:250, :, :]
    img = imresize(img, [224, 224])
    img = img - [129.18628, 104.76238, 93.59396]
    #RGB-->BGR
    img = img[:, :, (2, 1, 0)]
    #[high,weight,channels] --> [channels,high,weight]
    img = img.transpose(2,0,1)
    return img
