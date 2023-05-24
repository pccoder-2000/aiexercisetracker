import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('C:/Users/Priya/Downloads/burpees.mp4')

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1000, 720))    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Leg
        r_knee_angle = detector.findAngle(img, 24, 26, 28)
        r_ankle_angle = detector.findAngle(img, 26, 28, 30)
        # Left Leg
        l_knee_angle = detector.findAngle(img, 23, 25, 27)
        l_ankle_angle = detector.findAngle(img, 25, 27, 29)
        per_r = np.interp(r_knee_angle, (150, 220), (0, 100))
        per_l = np.interp(l_knee_angle, (150, 220), (0, 100))
        per_r_ankle = np.interp(r_ankle_angle, (170, 220), (0, 100))
        per_l_ankle = np.interp(l_ankle_angle, (170, 220), (0, 100))
        # print(r_knee_angle, l_knee_angle, per_r, per_l)

        # Check for the burpees
        color = (255, 0, 255)
        if per_r >= 60 and per_l >= 60 and per_r_ankle >= 70 and per_l_ankle >= 70:
            color = (0, 255, 0)
            if dir == 0:
                count += 1
                dir = 1
        if per_r <= 20 and per_l <= 20 and per_r_ankle <= 20 and per_l_ankle <= 20:
            color = (0, 255, 0)
            if dir == 1:
                dir = 0
        # print(count)
        # Draw Lunge Count
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
