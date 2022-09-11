import cv2
import numpy as np

path = 'My_Projects/OpenCV/image/SB3.jpg'
img = cv2.imread(path)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

# Trackbar
def empty(a):
    pass

cv2.namedWindow('TrackBars') #these two needs to be the same
cv2.resizeWindow('TrackBars', 640,240)#these two needs to be the same
cv2.createTrackbar('Hue Min','TrackBars',75,179,empty) #Max 179 hue values in OpenCV... usually has max of 360 though
cv2.createTrackbar('Hue Max','TrackBars',179,179,empty)
cv2.createTrackbar('Sat Min','TrackBars',0,255,empty)
cv2.createTrackbar('Sat Max','TrackBars',255,255,empty)
cv2.createTrackbar('Val Min','TrackBars',177,255,empty)
cv2.createTrackbar('Val Max','TrackBars',255,255,empty)


while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgResize = cv2.resize(imgHSV,(1000,715))
    imgOriginal = cv2.resize(img, (1000,715))
    h_min = cv2.getTrackbarPos('Hue Min','TrackBars')
    h_max = cv2.getTrackbarPos('Hue Max','TrackBars')
    s_min = cv2.getTrackbarPos('Sat Min','TrackBars')
    s_max = cv2.getTrackbarPos('Sat Max','TrackBars')
    v_min = cv2.getTrackbarPos('Val Min','TrackBars')
    v_max = cv2.getTrackbarPos('Val Max','TrackBars')
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgResize, lower, upper) #filter out image of the color

    img_result = cv2.bitwise_and(imgOriginal,imgOriginal,mask=mask) # add 2 images together to create a new image


    # cv2.imshow('HSV',imgResize)
    # cv2.imshow('Mask',mask)
    # cv2.imshow('Result',img_result)
    # cv2.waitKey(1)

    imgStack = stackImages(0.6, ([imgOriginal, imgHSV],[mask, img_result]))
    cv2.imshow('Stacked Images',imgStack)
    cv2.waitKey(1)


# Hue, saturation plays with real time
# imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# imgResize = cv2.resize(imgHSV,(1000,715))
# cv2.imshow('HSV',imgResize)
# cv2.waitKey(0)