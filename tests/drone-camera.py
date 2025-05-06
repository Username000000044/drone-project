#workdamnit
from djitellopy import Tello
import cv2
import time
import threading

tello = Tello()
tello.connect()
tello.streamon()

battery_level = tello.get_battery()

print(f"Battery level: {battery_level}%")


frame_read = tello.get_frame_read()

def show_video():
    while True:
        frame = frame_read.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Tello Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_thread = threading.Thread(target= show_video)

video_thread.start()
time.sleep(2)

tello.takeoff()
time.sleep(3)

tello.land()
time.sleep(2)

video_thread.join()
tello.streamoff()
cv2.destroyAllWindows()
