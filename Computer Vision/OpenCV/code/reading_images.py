import cv2
# IMAGES
# img = cv2.imread('My_Projects/OpenCV/Nadal.jpeg')
# cv2.imshow('Output',img)
# cv2.waitKey(0)

# GIF
import imageio
import urllib.request
import time
url = 'https://c.tenor.com/o656qFKDzeUAAAAC/rick-astley-never-gonna-give-you-up.gif'
file_name = 'Rick_Dance.gif'
## Read the gif from the web, save to the disk
imdata = urllib.request.urlopen(url).read()
imbytes = bytearray(imdata)
open(file_name,"wb+").write(imdata)
cv2.imshow
## Read the gif from disk to `RGB`s using `imageio.miread` 
gif = imageio.mimread(file_name)
nums = len(gif)
print("Total {} frames in the gif!".format(nums))
# convert form RGB to BGR 
imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
## Display the gif
i = 0
while True:
    cv2.imshow("gif", imgs[i])
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    i = (i+1)%nums
cv2.destroyAllWindows()

# VIDEO
# cap = cv2.VideoCapture('My_Projects/OpenCV/image/Persona5.mp4')
# while True:
#     success, img = cap.read()
#     cv2.imshow('video',img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.waitKey(0)


# FOR WEBCAM: either 0 for back cam or 1 for front cam for surface book 3
# If computer doesn't have webcam, can just use phone and download something like camo...
# cap = cv2.VideoCapture(0)
# cap.set(3,640) #width
# cap.set(4,480) #height
# while True:
#     success, img = cap.read()
#     cv2.imshow('video',img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break