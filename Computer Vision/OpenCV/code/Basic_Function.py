import numpy as np
import cv2

# img = cv2.imread('My_Projects/OpenCV/image/Nadal.jpeg')

# Gray image, Blur, Edge detector (Canny), Dilation

# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # image convention is usually RGB, but in opencv is BGR
# imgBlur = cv2.GaussianBlur(imgGray,(7,7),0) #kernel size (7,7)... has to be odd numbers... SigmaX is 0
# imgCanny = cv2.Canny(img, 100,100)

# kernel = np.ones((5,5),np.uint8) #type is unsigned integer ranging from 0 to 255 for 8 bit
# imgDialation = cv2.dilate(imgCanny, kernel, iterations=1) #iteration is how much thickness we need
# imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

# cv2.imshow('Gray Image', imgGray)
# cv2.imshow('Blur Image', imgBlur)
# cv2.imshow('Canny Image', imgCanny)
# cv2.imshow('Dialation Image', imgDialation)
# cv2.imshow('Erosion Image', imgEroded)
# cv2.waitKey(0)


# RESIZING
# print(img.shape)
# imgResize = cv2.resize(img, (1000,715)) #width first, then height
# cv2.imshow('Image',img)
# cv2.imshow('Resized Image',imgResize)
# cv2.waitKey(0)


# CROPPING
# imgCrop = img[0:200, 200:500] #Height first, then width
# cv2.imshow('Image Cropped', imgCrop)
# cv2.waitKey(0)


# DRAWING LINES/SHAPES/TEXTS
# img1 = np.zeros((512,512,3),np.uint8)
# print(img.shape)
# img1[:] = 255,0,0 # Everything blue
# img1[200:300, 100:300] = 255,0,0 #Rectangle fill blue on black pixels

# cv2.line(img1, (0,0),(300,300),(0,255,0),3) # img, starting point, end point, color channel dimension
# cv2.line(img1, (0,0),(img.shape[1], img.shape[0]), (0,0,255),3)

# cv2.rectangle(img1, (0,0),(250,350),(0,255,255), 2) # Can replace the thickness by filled if you want the area filled

# cv2.circle(img1, (400,50), 30, (255,255,0),5) # Drawing circles

# cv2.putText(img1, ' KEKERSW123 ', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1 ,(255,250,255),1) # Putting texts

# cv2.imshow('Image',img1)
# cv2.waitKey(0)



# WARP PERSPECTIVE
# img = cv2.imread('My_Projects/OpenCV/image/RTX3090_img.jpg')
# width, height = 1400,800
# pts1 = np.float32([[269,179], [936,55], [269,621], [937,454]])
# pts2 = np.float32([[0,0],[width,0],[0,height],[width, height]])
# matrix = cv2.getPerspectiveTransform(pts1, pts2)
# imgOutput = cv2.warpPerspective(img, matrix,(width,height))


# cv2.imshow('Image', img)
# cv2.imshow('Output',imgOutput)
# cv2.waitKey(0)


# JOINING IMAGE
# img = cv2.imread('My_Projects/OpenCV/image/Nadal.jpeg')

# imgHor = np.hstack((img, img)) Can't stack if different color channel
# imgVer = np.vstack(img, img)

# def stackImages(scale,imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range ( 0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank]*rows
#         hor_con = [imageBlank]*rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
#             if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor= np.hstack(imgArray)
#         ver = hor
#     return ver
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# imgStack = stackImages(0.25,([img,imgGray,img],[img,img,img]))
# cv2.imshow('Horizontal',imgHor)
# cv2.imshow('Vertical',imgVer)
# cv2.imshow('Stacked',imgStack)
# cv2.waitKey(0)

