import cv2

print("[INFO] starting video stream...")
#cap = cv2.VideoCapture('rtsp://192.168.168.143:6668/test')
cap = cv2.VideoCapture(2)
while True:

	ret,frame = cap.read()
        if ret == False:
            break

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
	    break
# do a bit of cleanup
cv2.destroyAllWindows()
