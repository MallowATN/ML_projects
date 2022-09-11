import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
mpDraw = mp.solutions.drawing_utils
# drawSpec = mpDraw.DrawingSpec()
# drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=5)


while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for lms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, lms, mpFaceMesh.FACEMESH_TESSELATION)
            # mpDraw.draw_landmarks(img, lms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
            for id, lm in enumerate(lms.landmark):
                # print(lm)
                h,w,c = img.shape
                x,y = int(lm.x*w), int(lm.y*h)
                print(id,x,y)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, 'fps: ' + str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.imshow('Image', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break