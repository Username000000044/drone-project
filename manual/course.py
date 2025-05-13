from djitellopy import Tello
import time

def run_path():
    try:
        tello = Tello() # regular

        tello.connect()

        # battery = tello.get_battery()
        # print(f"{battery}%")

        # 1st
        tello.takeoff()
        tello.move_up(75)
        time.sleep(2)
        tello.move_forward(80)
        time.sleep(2)
        
        # 2nd
        tello.move_up(50)
        time.sleep(2)
        tello.move_forward(100)
        tello.rotate_clockwise(90)
        tello.move_down(50)

        #3rd
        tello.move_forward(145)
        tello.rotate_counter_clockwise(90)
        tello.move_up(51)

        #4th
        tello.move_forward(85)

        #5th
        tello.rotate_counter_clockwise(40)
        tello.move_down(40)
        tello.move_forward(290)
        
        #6th
        tello.rotate_clockwise(20)
        tello.move_up(50)
        tello.move_forward(67)
        tello.rotate_clockwise(90)
        tello.flip_forward()
        time.sleep(5)
        tello.land()
    except Exception as e:
        print(f"Error: {e}")

        try:
            tello.land()
        except:
            pass # Avoid crash if connection already lost
    finally:
        tello.end()

if __name__ == "__main__": # ensuring the file is only executed when the file is run as the main program
    run_path()
