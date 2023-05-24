import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture('C:/Users/Priya/Downloads/jumping_jacks.mp4')

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        # Check for jumping jacks
        left_shoulder = lmList[11][1:]
        right_shoulder = lmList[12][1:]
        left_hip = lmList[23][1:]
        right_hip = lmList[24][1:]

        left_arm_angle = detector.findAngle(img, 11, 13, 15)
        right_arm_angle = detector.findAngle(img, 12, 14, 16)
        leg_angle = detector.findAngle(img, 23, 25, 27)
        
        # Check if arms are up and legs are out
        if left_arm_angle > 160 and right_arm_angle > 160 and leg_angle > 100:
            if dir == 0:
                count += 1
                dir = 1
        else:
            dir = 0

        # Draw Count
        cv2.rectangle(img, (0, 0), (250, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(count), (50, 70), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
