from djitellopy import Tello, TelloSwarm
import time

tello = Tello() # regular

tello.connect()

tello.takeoff()
time.sleep(5)
tello.land()
