import cv2
import mediapipe as mp
import time

class poseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, upper_body=False, smooth_lm=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.upper_body = upper_body
        self.smooth_lm = smooth_lm
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.upper_body, self.smooth_lm, self.detectionCon, self.trackCon)
    
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255,255,0),cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture('TFOD/PoseEstimation/img/Nadal.mp4')
    detector = poseDetector()
    pTime = 0
    while True:
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
        if cv2.waitKey(50) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()