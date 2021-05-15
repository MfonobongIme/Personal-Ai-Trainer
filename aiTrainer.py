#import libraries

import cv2
import numpy as np
import time
import mediapipe as mp
import poseEstimationModule as pm

detector = pm.poseDetector() #import pose module

cap = cv2.VideoCapture('pexels2.mp4') #read video

count = 0 #initialize count
dir = 0 #direction of coil (coil goes from 1 to 0 to complete)
pTime = 0


while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720)) #resize image

    #img = cv2.imread('bicep2.jpg') #read image

    img = detector.findPose(img, False) #find pose
    lmList = detector.findPosition(img, False) #find position of landmarks
    #print(lmList)

    #we need to have a list for the pose detected to avoid errors
    if len(lmList) != 0:
        #right arm
        angle = detector.findAngle(img, 24, 12, 14)

        # left arm
        angle = detector.findAngle(img, 23, 11, 13)

        #to know the percentage of coils
        per = np.interp(angle, (230, 300), (0, 100)) #convert the angle range to be btw 0-100

        #for bar
        bar = np.interp(angle, (230, 300), (650, 100))

        #print(angle, per)

        #color
        color = (255, 255, 255)

        #check for the count of dumbbell curls
        if per == 100: #if percentage equals 100
            color = (0, 0, 255)
            if dir == 0: #if direction goes up
                count += 0.5 #count it as 0.5
                dir = 1 #change direction

        if per == 0: #if percentage equals 0
            color = (0, 0, 255)
            if dir == 1: #if direction goes down
                count += 0.5 #count it as 0.5
                dir = 0 #change direction
        print(count)


        #create rectangle for our bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color,
                    4)  # put the text on image

        #put our curl count in a box
        cv2.rectangle(img, (0, 450), (250, 720), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25) #put the count on image

        done = 'Good Job!'
        almost = 'Almost there'
        encourage = 'Come on!'


        if per == 100:
            cv2.putText(img, 'Jarvis: {}'.format(done), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 5)
        else:
            cv2.putText(img, 'Jarvis: {}'.format(encourage), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 55), 5)



    #for framerate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime



    cv2.imshow('image', img)
    cv2.waitKey(1)