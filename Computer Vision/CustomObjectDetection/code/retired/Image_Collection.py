# pip install opencv-python
import cv2
import uuid #give unique identifier, name our image uniquely
import os #make sure we have file path
import time

################################################################################
labels = ['thumbsup','thumbsdown','thankyou','livelong']
# labels = ['thumbsup'] #in case I want to add more images for this category
number_img = 5
count = 0

#################################################################################


IMAGES_PATH = os.path.join('TFOD','Tensorflow','workspace','images','collectedimages')
if not os.path.exists(IMAGES_PATH):
    if os.name == 'nt':
        os.makedirs(IMAGES_PATH)
for label in labels:
    path = os.path.join(IMAGES_PATH,label)
    if not os.path.exists(path):
        os.makedirs(path)


for label in labels:
    cap = cv2.VideoCapture(1)
    print('Collecting images for {}'.format(label))
    time.sleep(5)
    for imgnum in range(number_img):
        print('Collecting image {}'.format(imgnum))
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH, label, label+'.' +'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame',frame)
        time.sleep(2)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
cap.release()
cv2.destroyAllWindows