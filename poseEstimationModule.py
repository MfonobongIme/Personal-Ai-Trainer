#import libraries
import cv2
import mediapipe as mp
import time
import math

class poseDetector():

    def __init__(self, mode = False, upBody = False, smooth = True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode

        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose #create our model
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                self.detectionCon, self.trackCon) #create pose object
        self.mpDraw = mp.solutions.drawing_utils #for drawing detected landmarks

    #find pose funtion
    def findPose(self, img, draw = True): #draw = True because we want to draw it on the image


        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #conver to rgb for our pose model
        self.results = self.pose.process(imgRGB) #send image to our model

        #print(results.pose_landmarks) # prints detected landmarks results
        if self.results.pose_landmarks: #if landmarks are detected, we go in
            if draw:  # if draw is True
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS) #draw the detected landmarks
        return img

#get position of points
    def findPosition(self, img, draw = True):

        # put them in list
        self.lmList = []

        #if results are available
        if self.results.pose_landmarks:

            #extract id of all landmarks
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape #get the height, width and center of image
                #print(id, lm)

                #get actual pixel value
                cx, cy = int(lm.x*w), int(lm.y*h) #convert to integer and store in cx and cy variable
                self.lmList.append([id, cx, cy]) #append id, and the x and y positions
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED) #draw circle on landmark
        return self.lmList

    #find angle between 3 points
    def findAngle(self, img, p1, p2, p3, draw = True):
        #get the landmarks
        x1, y1 = self.lmList[p1][1:] #slice it so we get the x and y values
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        #calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 -x2) - math.atan2(y1 -y2, x1 - x2)) #gives us angle in radiants converted to degrees

        #for negative angle values problem
        if angle < 0:
            angle += 360 #add 360 to solve the problem

        print(angle)


        #we draw to make sure we are getting the correct points
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 255), 2)
            cv2.putText(img, str(int(angle)),(x2 -20, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)#put angle on image
        return angle







def main():
    cap = cv2.VideoCapture('everything_9.mp4')  # capture video
    pTime = 0  # define previous time

    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw = False)
        if len(lmList) != 0:

            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (255, 255, 0), cv2.FILLED)  # draw circle on landmark

        cTime = time.time()  # current time

        fps = 1 / (cTime - pTime)  # frame rate
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)  # put text for frame rate

        cv2.imshow('Image', img)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()
