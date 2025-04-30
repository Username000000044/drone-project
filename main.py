from djitellopy import Tello
import time

tello = Tello() # regular

tello.connect()

# battery = tello.get_battery()
# print(f"{battery}%")

# 1st
tello.takeoff()
tello.move_up(75)
tello.move_forward(65)

# 2nd
tello.move_up(50)
tello.move_forward(50)
tello.rotate_clockwise(90)
tello.move_down(50)

#3rd
tello.move_forward(100)
tello.rotate_counter_clockwise(90)
tello.move_up(50)

#4th
tello.move_forward(50)
tello.flip(2)
time.sleep(5)
tello.land()

tello.end()