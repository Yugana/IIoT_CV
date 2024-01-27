import requests
import cv2
import time
from threading import Thread
import numpy as np

def get_image():
    url = "http://192.168.1.153:8088/shot.jpg?rnd={}"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print("Error getting image")

def display_image(img):
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', img)
    cv2.waitKey(1)

if __name__ == "__main__":
    t = Thread(target=get_image)
    t.daemon = True
    t.start()

    while True:
        img = cv2.imdecode(np.fromstring(get_image(), dtype=np.uint8), -1)
        display_image(img)
        time.sleep(1)
