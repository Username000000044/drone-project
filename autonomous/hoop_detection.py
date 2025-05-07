from multiprocessing import Process
import cv2 as cv
import numpy as np

class HoopDetection(Process):
    def __init__(self, frame_queue, product_queue, color_ranges, sequence):
        super().__init__() # allows me to use functions from Process parent class

        self.frame_queue = frame_queue
        self.product_queue = product_queue
        self.color_ranges = color_ranges
        self.sequence = sequence

        self.current_color_index = 0
        self.hoops_detected = 0
        self.recently_seen_hoop = False
        self.cooldown_frames = 20
        self.cooldown_counter = 0
    
    def run(self):
        while True:
            frame = self.frame_queue.get()
            if frame is None:
                break #?Stop process when no frames are received
            
            self.detect_hoop(frame)

    def detect_hoop_color(self, frame, color_name):
        lower = np.array(self.color_ranges[color_name]["lower"])
        upper = np.array(self.color_ranges[color_name]["upper"])
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        return cv.inRange(hsv, lower, upper)
    
    def detect_hoop(self, frame):
        current_color = self.sequence[self.current_color_index]
        color_mask = self.detect_hoop_color(frame, current_color)

        # reduces noise and helps for detection
        clean_mask = cv.morphologyEx(color_mask, cv.MORPH_OPEN, np.ones((5, 5), np.uint8))

        # Find contours and detect circles
        contours, _ = cv.findContours(clean_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        hoop_found = False
        center = None
        radius = 0

        if not contours:
            return None, None
        
        # Largest countour area is most likely the hoop
        largest = max(contours, key=cv.contourArea)
        
        
        if cv.contourArea(largest) > 500: # ? Adjust as needed. 100px
            ((x, y), radius) = cv.minEnclosingCircle(largest)
            center = (int(x), int(y))
            radius = int(radius)

            hoop_found = True

        if hoop_found and not self.recently_seen_hoop:
            self.hoops_detected += 1
            self.recently_seen_hoop = True
            self.cooldown_counter = self.cooldown_frames
            print(f"🪝 Detected Hoop #{self.hoops_detected} for color {current_color}")
        
        if self.hoops_detected >= 2 and self.current_color_index < len(self.sequence) - 1:
            self.current_color_index += 1
            self.hoops_detected = 0
            print(f"🎯 Now looking for: {self.sequence[self.current_color_index]} ")

        if self.recently_seen_hoop:
            self.cooldown_counter -= 1
            if self.cooldown_counter <= 0:
                self.recently_seen_hoop = False

        self.product_queue.put((center, radius if hoop_found else None))

        