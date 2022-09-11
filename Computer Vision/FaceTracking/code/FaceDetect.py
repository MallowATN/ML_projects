import cv2
import mediapipe as mp
import time
#############
pTime = 0
cTime = 0
#############

cap = cv2.VideoCapture(0)

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    # print(results)
    if results.detections:
        for id, detection in enumerate(results.detections):
            # mpDraw.draw_detection(img, detection)
            # print(id, detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box) #gives us xmin, ymin, width, height
            bound_box_c = detection.location_data.relative_bounding_box 
            h,w,c = img.shape
            bound_box = int(bound_box_c.xmin*w), int(bound_box_c.ymin*h), int(bound_box_c.width*w), int(bound_box_c.height*h)
            cv2.rectangle(img, bound_box, (0,255,255), 2)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bound_box[0],bound_box[1]-20), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, 'fps: ' +str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.imshow('Image', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break