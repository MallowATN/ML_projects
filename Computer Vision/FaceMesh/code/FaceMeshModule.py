import cv2
import mediapipe as mp
import time


class faceMeshDetect:
    def __init__(self,mode=False, max_face=2, rlm=False, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.max_face = max_face
        self.rlm = rlm
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.mode, self.max_face, self.rlm, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=5)

    def findFaceMesh(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        if self.results.multi_face_landmarks:
            for self.lms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.lms, self.mpFaceMesh.FACEMESH_TESSELATION)
                    # self.mpDraw.draw_landmarks(img, self.lms, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
        return img

    def getPosition(self, img, draw=True):
        lmList = []
        if self.results.multi_face_landmarks:
            for id, lm in enumerate(self.lms.landmark):
                h,w,c = img.shape
                x,y = int(lm.x*w), int(lm.y*h)
                cv2.putText(img, str(id), (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),1)
                lmList.append([id, x, y])
        return lmList

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = faceMeshDetect()
    while True:
        success, img = cap.read()
        img = detector.findFaceMesh(img)#can mark as False if you don't want to draw
        lmList = detector.getPosition(img)
        # if len(lmList) != 0:
            # print(lmList[14])
            # cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (0,255,0),cv2.FILLED)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, 'fps: ' + str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Image', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()