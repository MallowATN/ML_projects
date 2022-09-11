import cv2
import time
import mediapipe as mp
import os

# os.chdir(r'C:\Users\antho\Desktop\VSC')
import HandTrackModule as htm
pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.find_hands(img) #draw = false inside
    lmList = detector.find_position(img)
    if len(lmList) != 0:
        print(lmList[4])        
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, 'fps: ' +str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    cv2.imshow('Image', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break