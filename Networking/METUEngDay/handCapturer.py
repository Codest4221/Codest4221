import cv2 
import mediapipe as mp
import numpy as np
def handCapturer(self):
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()

    point = {}
    pointlist = []
    oldarea = 0
    while True:
        success, image = cap.read()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)
        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks: # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 20 or id == 16 or id == 12 or id == 8 or id == 4 or id == 0 :
                        point[id] = [cx,cy]
                        pointlist.append((cx,cy))
        if len(pointlist) != 0:
            area = cv2.contourArea(np.array(pointlist))
            if area < oldarea/20:
                print("hello")
            oldarea = area
        point = {}
        pointlist = []