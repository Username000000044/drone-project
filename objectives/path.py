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