from djitellopy import Tello
import time

class PIDController:
    def __init__(self, kp, ki, kd, integral_limit=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit = integral_limit

        self.prev_error = 0
        self.integral = 0

    def calculate(self, error):
        self.integral += error
        self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)  # Clamp
        derivative = error - self.prev_error
        self.prev_error = error

        return int(self.kp * error + self.ki * self.integral + self.kd * derivative)

class DroneController:
    def __init__(self, settings):
        self.tello = Tello()
        self.tello.connect()

        self.forward_speed = settings.get("forward_speed", 20)
        self.center_threshold = settings.get("center_threshold", 50)
        self.radius_threshold = settings.get("radius_threshold", 70)

        self.yaw_pid = PIDController(kp=0.3, ki=0.0, kd=0.2)
        self.up_pid = PIDController(kp=0.3, ki=0.0, kd=0.2)

        self.state = "align"
        self.last_state_change = time.time()

        self.target_radius = settings.get("target_radius", 90)  # Radius size when hoop is "close"

    def takeoff(self):
        self.tello.takeoff()
        print("🚁 Drone took off")

    def land(self):
        self.tello.land()
        print("🛬 Drone landed")

    def update(self, centroid, circle_center, frame_center):
        """
        Controls the drone based on the hoop detection status.
        Uses a state machine to manage movement phases:
        - align: rotate to center the hoop
        - center: adjust vertically
        - forward: fly forward through the hoop
        """

        if not centroid:
            print("❓ No hoop detected. Searching...")
            self.tello.rotate_clockwise(20)
            return

        error_x = centroid[0] - frame_center[0]
        error_y = centroid[1] - frame_center[1]

        yaw_correction = self.yaw_pid.calculate(error_x)
        up_correction = self.up_pid.calculate(-error_y)

        # FSM logic
        if self.state == "align":
            if abs(error_x) > self.center_threshold:
                self.tello.send_rc_control(0, 0, 0, yaw_correction)
                print(f"🧭 Aligning... error_x={error_x}, yaw_correction={yaw_correction}")
            else:
                self.tello.send_rc_control(0, 0, 0, 0)
                self.state = "center"
                print("🎯 Hoop horizontally aligned")

        elif self.state == "center":
            if abs(error_y) > self.center_threshold:
                self.tello.send_rc_control(0, 0, up_correction, 0)
                print(f"🎢 Adjusting height... error_y={error_y}, up_correction={up_correction}")
            else:
                self.tello.send_rc_control(0, 0, 0, 0)
                self.state = "forward"
                print("📐 Hoop centered vertically")

        elif self.state == "forward":
            if circle_center:  # Only if a valid hoop is visible
                (x, y), radius = circle_center, None
                if radius and radius >= self.target_radius:
                    print("📏 Close enough. Passing through hoop")
                    self.tello.send_rc_control(0, self.forward_speed, 0, 0)
                    time.sleep(2)  # Fly through
                    self.tello.send_rc_control(0, 0, 0, 0)
                    self.state = "align"  # Prepare for next hoop
                else:
                    print("🚀 Moving forward slowly")
                    self.tello.send_rc_control(0, self.forward_speed, 0, 0)
            else:
                self.tello.send_rc_control(0, self.forward_speed, 0, 0)

    def emergency_stop(self):
        self.tello.send_rc_control(0, 0, 0, 0)
        print("⛔ Emergency stop called.")
