import cv2
import mediapipe as mp
import time

cTime = 0
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture('TFOD/PoseEstimation/img/Nadal.mp4')

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            # print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 3, (255,255,0),cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'fps: ' + str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
    cv2.imshow("kekw", img)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()


# success, img = imgs.read()
# imgs = cv2.imread('TFOD/PoseEstimation/img/Nadal.jpg')
# imgRGB = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
# results = pose.process(imgRGB)
# print(results.pose_landmarks)
# if results.pose_landmarks:
#     mpDraw.draw_landmarks(imgs, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
# cv2.imshow("kekw", imgs)
# cv2.waitKey(0)