import cv2
import mediapipe as mp
import time

class faceDetector:
    def __init__(self, minDetectionCons = 0.5):
        self.minDetectionCons = minDetectionCons
        
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(0.75)

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        boundBox = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
            # mpDraw.draw_detection(img, detection)
            # print(id, detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box) #gives us xmin, ymin, width, height
                if draw:
                    bound_box_c = detection.location_data.relative_bounding_box 
                    h,w,c = img.shape
                    bound_box = int(bound_box_c.xmin*w), int(bound_box_c.ymin*h), int(bound_box_c.width*w), int(bound_box_c.height*h)
                    boundBox.append([id, bound_box, detection.score])
                    img = self.customDraw(img, bound_box)

                    cv2.putText(img, f'{int(detection.score[0]*100)}%', (bound_box[0],bound_box[1]-20), cv2.FONT_ITALIC,2,(255,0,0),2)
        return img, boundBox

    def customDraw(self, img ,bound_box, l=30, t=10):
        x,y,w,h = bound_box
        x1,y1 = x+w, y+h
        cv2.rectangle(img, bound_box, (0,0,255), 2)
        cv2.line(img, (x,y), (x+l,y), (255,255,255),t) #top left
        cv2.line(img, (x,y), (x,y+l), (255,255,255),t)

        cv2.line(img, (x1,y1), (x1-l,y1), (255,255,255),t) # bottom right
        cv2.line(img, (x1,y1), (x1,y1-l), (255,255,255),t)

        cv2.line(img, (x,y1), (x,y1-l), (255,255,255),t) #bottom left
        cv2.line(img, (x,y1), (x+l,y1), (255,255,255),t)

        cv2.line(img, (x1,y), (x1,y+l), (255,255,255),t) #top right
        cv2.line(img, (x1,y), (x1-l,y), (255,255,255),t)
        return img
def main():
    cap = cv2.VideoCapture(0)
    detector = faceDetector()
    pTime = 0
    while True:
        success, img = cap.read()
        img, boundBox = detector.findFace(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, 'fps: ' +str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Image', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()