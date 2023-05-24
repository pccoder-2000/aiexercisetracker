import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture('C:/Users/Priya/Downloads/situps.mp4')

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        # Right Side
        r_shoulder_angle = detector.findAngle(img, 12, 14, 16)
        r_elbow_angle = detector.findAngle(img, 14, 16, 18)
        r_knee_angle = detector.findAngle(img, 24, 26, 28)
        per_r_shoulder = np.interp(r_shoulder_angle, (170, 220), (0, 100))
        per_r_elbow = np.interp(r_elbow_angle, (40, 170), (100, 0))
        per_r_knee = np.interp(r_knee_angle, (170, 220), (0, 100))

        # Check for situps
        color = (255, 0, 255)
        if per_r_shoulder >= 70 and per_r_elbow >= 70 and per_r_knee <= 20:
            color = (0, 255, 0)
            if dir == 0:
                count += 1
                dir = 1
        if per_r_shoulder <= 30 and per_r_elbow <= 30 and per_r_knee >= 160:
            color = (0, 255, 0)
            if dir == 1:
                dir = 0

        # Draw Situp Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
    
    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
