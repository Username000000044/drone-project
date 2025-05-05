from djitellopy import Tello

class TelloController:

    # Auto run function
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        print(f"🔋 Battery: {self.tello.get_battery()}%")

    def takeoff(self):
        self.tello.takeoff()
        print("🚁 Drone took off.")

    def land(self):
        self.tello.land()
        print("🛬 Drone landed.")

    # Receives x_offset and y_offset which describe how far the detected ring is from the cetner of the frame.
    # x_offset = horizonal distance, positive = right, negative = left
    # y_offset = vertical distance, positive = down, negative = up
    def move_towards(self, x_offset, y_offset):
        
        # Only move left or right if the ring is significantly off-center horizonatally, more than 20 pixels.
        # prevents jittery or overly frequent movements from small changes.
        if abs(x_offset) > 20:

            # if the ring is to the right of frame's center move right by 20cm
            if x_offset > 0:
                self.tello.move_right(20)

            # if the ring is to the left of frame's center move left by 20cm
            else:
                self.tello.move_left(20)

        # Only move up or down if the ring is significantly off-center vertically, more than 20 pixels.
        # prevents jittery or overly frequent movements from small changes.
        if abs(y_offset) > 20:

            # if the ring is bellow of frame's center move the drone down by 20cm
            if y_offset > 0:
                self.tello.move_down(20)

            # if the ring is above of frame's center move the upwards down by 20cm
            else:
                self.tello.move_up(20)

        print(f"📍 Adjusted position by ({x_offset}, {y_offset})")

    def fly_forward(self, distance=30):
        self.tello.move_forward(distance)
        print(f"➡️ Moved forward {distance}cm.")