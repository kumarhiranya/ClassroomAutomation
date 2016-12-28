import cv2
import time
import sys
import os
import RPi.GPIO as gpio

gpio.setup (2, gpio.OUT)
gpio.setup (3, gpio.OUT)
gpio.setup (4, gpio.OUT)
gpio.setup (17, gpio.OUT)
gpio.setup (27, gpio.OUT)

f=[2,3,4,17,27]

def dist(w):
	
	d=10*0.36/(w*0.00012336)
	return(d)

os.system("raspistill -o tempimg.jpg")
cascPath1 = "/home/pi/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade1 = cv2.CascadeClassifier(cascPath1)
path= '/home/pi/tempimg.jpg'
img=[]
dis=[]
fan=[100, 300, 500, 700, 1000]
fflag=[0,0,0,0,0]
i=0
nframe = cv2.imread(path)

newx,newy = nframe.shape[1]/4,nframe.shape[0]/4
frame = cv2.resize(nframe,(newx,newy))


gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


faces = faceCascade1.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100,100),
    flags=cv2.cv.CV_HAAR_DO_CANNY_PRUNING
)

nfaces=len(faces)
    
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0),2)
    if i<nfaces:
        img.append([w,h])
        i=i+1

for (w,h) in img:
    dis.append(dist(w))

if nfaces>0 and nfaces<6:
	for d in dis:
		if abs(d-fan[0])<=100:
			fflag[0]=1
		else:
			fflag[0]=0

		if abs(d-fan[1])<=100:
			fflag[1]=1
		else:
			fflag[1]=0

		if abs(d-fan[2])<=100:
			fflag[2]=1
		else:
			fflag[2]=0

		if abs(d-fan[3])<=100:
			fflag[3]=1
		else:
			fflag[3]=0

if nfaces>5:
	fflag=[1, 1, 1, 1, 1]

	

if fflag[0]==1:
	gpio.output(f[0], True)
else:
	gpio.output(f[0],False)

if fflag[1]==1:
	gpio.output(f[1], True)
else:
	gpio.output(f[1],False)


if fflag[2]==1:
	gpio.output(f[2], True)
else:
	gpio.output(f[2],False)


if fflag[3]==1:
	gpio.output(f[3], True)
else:
	gpio.output(f[3],False)


if fflag[4]==1:
	gpio.output(f[4], True)
else:
	gpio.output(f[4],False)

		


print dis
print img    
#cv2.rectangle(frame, (0, 0), (200, 200), (0, 0, 0),2)
cv2.imshow('OUTPUT', frame)
print faces  
print fflag 

while cv2.waitKey(1) & 0xFF != ord('q'):
    time.sleep(0.1)

cv2.destroyAllWindows()
