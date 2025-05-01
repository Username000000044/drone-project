from djitellopy import Tello
import time
import cv2
import threading
import sys
import os
import logging



tello = Tello() #imports tello and is where I will define everything for now
print("connecting to drone")
tello.connect()
battery = tello.get_battery()
print("Tello Connected")
print(f"Battery percentage {battery}")
#connects to tello and displays the battery



def video_stream():
    while True:
        frame = tello.get_frame_read().frame 
        frame = cv2.resize(frame, (1920, 1080))
        cv2.imshow("tello video stream", frame)
        if cv2.waitkey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

tello.streamon()

tello.get_frame_read()



tello.streamoff()


tello.takeoff()
time.sleep(5)

time.sleep(5)
tello.land()
