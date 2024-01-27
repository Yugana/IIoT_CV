import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import requests
from ultralytics import YOLO
from PIL import Image
from time import sleep
from datetime import datetime
import os
import logging

class RedBoxDetector:
    MIN_AREA_THRESHOLD = 1_000  # Minimum area threshold in pixels

    def __init__(self):
        # Initialize video capture object
        self.url = "http://192.168.1.153:8088/shot.jpg?rnd={}"
        self.objectIsVisible_Flag = [False, False]
        self.objectCoordinates = [0, 0, 0]
        #Отсчитываем начало эксперемента (будет занванием файла логав)
        self.TimeOfExperementStart = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        print(self.TimeOfExperementStart)

    def writeLogsInFile(self):

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if self.objectIsVisible_Flag[1]:
            print("Объект появился", current_time)
        else:
            print("Объект пропал", current_time)

        # Создаем директорию, если она не существует
        directory = "ResultLogs"
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Создаем файл
        file_path = os.path.join('ResultLogs', f'{self.TimeOfExperementStart}.txt')
        if not os.path.isfile(file_path):
            with open(file_path, 'w'): pass
        with open(f'ResultLogs/{self.TimeOfExperementStart}.txt', 'a') as file:
            file.write(f'{int(self.objectIsVisible_Flag[1] == True)},{self.objectCoordinates},{current_time}\n')
        file.close()

    def checkFlagIsChanged(self):

        # В случае изменения состояния видимость, инииируется запись в лог
        if self.objectIsVisible_Flag[0] != self.objectIsVisible_Flag[1]:
           self.writeLogsInFile()
        self.objectIsVisible_Flag[0] = self.objectIsVisible_Flag[1]



    def get_image(self):
        while True:
            response = requests.get(self.url)
            if response.status_code == 200:
                return response.content
            else:
                print("Error getting image")

    def detect(self):
        while True:
            # Read frame from video stream

            # new code block
            # screenshot = pyautogui.screenshot(region=(self.w.left, self.w.top, self.w.width, self.w.height))
            img_bytes = self.get_image()
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            frame = np.array(img)


            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define lower and upper bounds for red color
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([5, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red = np.array([175, 100, 100])
            upper_red = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red, upper_red)

            # Combine the masks
            mask = mask1 + mask2

            # Apply morphological opening to remove noise
            kernel = np.ones((5, 5), np.uint8)
            mask_opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Find contours in the mask
            contours, hierarchy = cv2.findContours(mask_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Draw bounding boxes around the detected objects
            for c in contours:
                area = cv2.contourArea(c)
                if area > self.MIN_AREA_THRESHOLD:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # print("Object at ({}, {})-({},{})".format(x, y, x + w, y + h))
                    self.objectIsVisible_Flag[1] = True

            #Меняем текущее состояние на видимое
            if not contours:
                self.objectIsVisible_Flag[1] = False
            self.checkFlagIsChanged()


            # Show the output frame
            cv2.imshow('Red Box Detector', frame)

            # Quit if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break

            # Release the resources and close the window
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # detector = YOLOv5Detector('yolov8n.pt')
    # detector.detect()

    detector = RedBoxDetector()
    detector.detect()