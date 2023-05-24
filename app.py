
import streamlit as st
import cv2
import numpy as np
import time
import PoseModule as pm

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
st.title("Webcam Live Feed")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

# Define the importance of each exercise
exercise_importance = {
    'curls': 'Curls are a great way to build bicep strength and size, which can help improve your overall upper body strength and fitness level.',
    'push ups': 'Push ups are a classic exercise that can help strengthen your chest, shoulders, triceps, and core muscles. They are a great way to build overall upper body strength and endurance.',
    'Squat': 'Squats are one of the best exercises for building leg strength and size, as well as improving your overall lower body fitness. They also help improve core strength and stability.'
}

# Exercise options
easy_exercises = ('curls', 'push ups', 'Squat')
medium_exercises = ('Lunges', 'Side planks', 'Sit ups')
hard_exercises = ('Burpees', 'High knees', 'Jumping jacks', 'Pull ups')

# Difficulty level dropdown
difficulty = st.selectbox('Select difficulty level', ('Easy', 'Medium', 'Hard'))

if difficulty == 'Easy':
    exercise_options = easy_exercises
elif difficulty == 'Medium':
    exercise_options = medium_exercises
else:
    exercise_options = hard_exercises

# Exercise selection dropdown
option = st.selectbox('Select exercise', exercise_options)
st.write('You selected:', option)


# Display the importance of the selected exercise
if option in exercise_importance:
    st.write('Importance:', exercise_importance[option])
    
    
#option = st.selectbox(
     #'Exercise',
     #('curls', 'push ups', 'Squat', 'Lunges', 'Burpees', 'Side_planks', 'Sit_ups', 'High_knees', 'Jumping_jack', 'Pull_ups'))
#st.write('You selected:', option)

while run:
    _, img = camera.read()
    img = cv2.resize(img, (1280, 720))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        if option =="curls":
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))
        elif option =="push ups":
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)

            # print(angle, per)
            # legs
            angle = detector.findAngle(img, 24, 26, 28)
            angle = detector.findAngle(img, 23, 25, 27)

            # # Left Arm
            angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (60, 130), (0, 100))
            bar = np.interp(angle, (60, 130), (650, 100))
        # print(angle, per)
        elif option == "Squat":
            angle = detector.findAngle(img, 12, 24, 28)
            per = np.interp(angle, (100, 170), (0, 100))
            bar = np.interp(angle, (100, 170), (650, 100))

        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    FRAME_WINDOW.image(img)
else:
    st.write('Stopped')