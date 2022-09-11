import cv2
import time
import mediapipe as mp
import os

import PoseEstimationModule as PEM

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = PEM.poseDetector()
cap = cv2.VideoCapture('TFOD/PoseEstimation/img/Nadal.mp4')
while True:
    # cap = cv2.VideoCapture('TFOD/PoseEstimation/img/Nadal.mp4')
    detector = PEM.poseDetector()
    success, img = cap.read()
    img = detector.findPose(img)
    # lmList = detector.findPosition(img)

    lmList = detector.findPosition(img, draw=False) #draw=False
    if len(lmList) != 0:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (0,255,0),cv2.FILLED)
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'fps: ' + str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
    cv2.imshow("kekw", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
