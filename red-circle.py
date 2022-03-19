#Bahadır Bolat
import cv2
import numpy as np
import time
import math

print(cv2.__version__)
def nothing(nothing):
    # any operation
    pass

dispW=640
dispH=480
flip=2

#Kamera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=640 , height=480 , format=(string)NV12, framerate=20/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap= cv2.VideoCapture(camSet)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

def kirmiziTanimla(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel)
    mask = cv2.GaussianBlur(mask,(3,3),0)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt,True)

        if perimeter == 0:
            break
        circularity = 4*math.pi*(area/(perimeter*perimeter))
        
        if 0.7 < circularity <1.2:
            if area>300:
                (x, y), radius = cv2.minEnclosingCircle (cnt)
                center = (int (x), int (y))
                radius = int (radius)
                circle = cv2.circle (frame, center, radius , (0,0,255), 2)
                cv2.drawContours (frame, [cnt], 0, (255, 255, 10), 2)
                print("area:",area)
                print(x,y,radius)
                print("circularity=",circularity)
                return 1
    return 0

while True:
    _, frame = cap.read()
    kirmizi = kirmiziTanimla(frame)
    cv2.imshow ('Contours', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
