import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('C:/Users/Priya/Downloads/side_planks.mp4')

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Left Side
        l_shoulder_angle = detector.findAngle(img, 11, 13, 15)
        l_hip_angle = detector.findAngle(img, 23, 25, 27)
        l_knee_angle = detector.findAngle(img, 25, 27, 29)
        per_l_shoulder = np.interp(l_shoulder_angle, (170, 220), (0, 100))
        per_l_hip = np.interp(l_hip_angle, (150, 220), (0, 100))
        per_l_knee = np.interp(l_knee_angle, (150, 220), (0, 100))
        # print(l_shoulder_angle, l_hip_angle, l_knee_angle, per_l_shoulder, per_l_hip, per_l_knee)

        # Check for the side planks
        color = (255, 0, 255)
        if per_l_shoulder >= 70 and per_l_hip >= 70 and per_l_knee <= 20:
            color = (0, 255, 0)
            if dir == 0:
                count += 1
                dir = 1
        if per_l_shoulder <= 30 and per_l_hip <= 30 and per_l_knee >= 160:
            color = (0, 255, 0)
            if dir == 1:
                dir = 0
        # print(count)
        # Draw Side Plank Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
    ##cTime = time.time()
    #fps = 1 / (cTime - pTime)
    #pTime = cTime
    #cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
    #            (255, 0, 0), 5)
    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
